import csv
import math
from dataclasses import dataclass
from typing import Optional

import boto3
import click
import pandas as pd
import pyarrow.fs
import pyarrow.orc
import s3fs
from fastparquet import ParquetFile
from gable.helpers.data_asset_s3.logger import log_debug
from gable.helpers.data_asset_s3.native_s3_converter import NativeS3Converter
from gable.helpers.data_asset_s3.path_pattern_manager import SUPPORTED_FILE_TYPES
from gable.helpers.data_asset_s3.schema_profiler import (
    get_data_asset_field_profiles_for_data_asset,
)
from gable.openapi import DataAssetFieldsToProfilesMapping, SamplingParameters
from loguru import logger

DEFAULT_NUM_ROWS_TO_SAMPLE = 1000
CHUNK_SIZE = 100
sniffer = csv.Sniffer()


@dataclass
class S3DetectionResult:
    schema: dict
    data_asset_fields_to_profiles_map: Optional[DataAssetFieldsToProfilesMapping] = None


@dataclass
class S3ReadResult:
    df: pd.DataFrame
    has_schema: bool


def read_s3_files(
    s3_urls: list[str],
    row_sample_count: int,
    s3_opts: Optional[dict] = None,
) -> dict[str, S3ReadResult]:
    """
    Read data from given S3 file urls (only CSV, JSON, and parquet currently supported) and return pandas DataFrames.
    Args:
        s3_urls (list[str]): List of S3 URLs.
        row_sample_count (int): Number of rows to sample per S3 file.
        s3_opts (dict): S3 storage options. - only needed for tests using moto mocking
    Returns:
        dict[str, S3ReadResult]: Dict of file url to pandas DataFrames and a boolean indicating if the DataFrame has a predefined schema.
    """
    result: dict[str, S3ReadResult] = {}
    for url in s3_urls:
        if df := read_s3_file(url, row_sample_count, s3_opts):
            result[url] = df
    return result


def read_s3_file(
    url: str, num_rows_to_sample: int, s3_opts: Optional[dict] = None
) -> Optional[S3ReadResult]:
    """
    Returns a tuple of pandas DataFrame and a boolean indicating if the DataFrame has a predefined schema.
    """
    try:
        if url.endswith(SUPPORTED_FILE_TYPES.CSV.value):
            log_debug(f"Reading {num_rows_to_sample} rows from S3 file: {url}")
            return S3ReadResult(get_csv_df(url, num_rows_to_sample, s3_opts), False)
        elif url.endswith(SUPPORTED_FILE_TYPES.JSON.value):
            log_debug(f"Reading {num_rows_to_sample} rows from S3 file: {url}")
            df = pd.concat(
                pd.read_json(
                    url,
                    lines=True,
                    chunksize=CHUNK_SIZE,
                    nrows=num_rows_to_sample,
                    storage_options=s3_opts,
                ),
                ignore_index=True,
            )
            return S3ReadResult(flatten_json(df), False)
        elif url.endswith(SUPPORTED_FILE_TYPES.PARQUET.value):
            log_debug(f"Reading {num_rows_to_sample} rows from S3 file: {url}")
            return S3ReadResult(get_parquet_df(url, num_rows_to_sample, s3_opts), True)
        elif url.endswith(SUPPORTED_FILE_TYPES.ORC.value) or url.endswith(
            SUPPORTED_FILE_TYPES.ORC_SNAPPY.value
        ):
            log_debug(f"Reading {num_rows_to_sample} rows from S3 file: {url}")
            return S3ReadResult(get_orc_df(url, num_rows_to_sample, s3_opts), True)
        else:
            log_debug(f"Unsupported file format: {url}")
            return None
    except Exception as e:
        # Swallowing exceptions to avoid failing processing other files
        logger.opt(exception=e).error(f"Error reading file {url}: {e}")
        return None


def get_orc_df(
    url: str, num_rows_to_sample: int, s3_opts: Optional[dict] = None
) -> pd.DataFrame:
    """
    Read ORC file from S3 and return a pandas DataFrame.
    """
    endpoint_override = (
        s3_opts.get("client_kwargs", {}).get("endpoint_url") if s3_opts else None
    )
    session = boto3.Session()
    credentials = session.get_credentials()
    if not credentials:
        raise click.ClickException("No AWS credentials found")
    filesystem = pyarrow.fs.S3FileSystem(
        endpoint_override=endpoint_override,
        access_key=credentials.access_key,
        secret_key=credentials.secret_key,
        session_token=credentials.token,
        region=boto3.Session().region_name,
    )
    bucket_and_path = strip_s3_bucket_prefix(url)
    with filesystem.open_input_file(bucket_and_path) as f:
        orcfile = pyarrow.orc.ORCFile(f)
        rows_per_stripe = orcfile.nrows / orcfile.nstripes
        stripes_to_sample = min(
            math.ceil(num_rows_to_sample / rows_per_stripe), orcfile.nstripes
        )
        log_debug(
            f"Reading {stripes_to_sample} stripes from {url} (total rows: {orcfile.nrows}, total stripes: {orcfile.nstripes})"
        )
        return pyarrow.Table.from_batches(
            [orcfile.read_stripe(i) for i in range(stripes_to_sample)]
        ).to_pandas()


def get_parquet_df(
    url: str, num_rows_to_sample: int, s3_opts: Optional[dict] = None
) -> pd.DataFrame:
    """
    Read Parquet file from S3 and return an empty pandas DataFrame with the schema.
    """
    parquet_file = ParquetFile(url, fs=s3fs.S3FileSystem(**(s3_opts or {})))
    # read default sample size rows in order to compute profile. Only 1 row is needed to compute schema
    return parquet_file.head(num_rows_to_sample)


def get_csv_df(
    url: str, num_rows_to_sample: int, s3_opts: Optional[dict] = None
) -> pd.DataFrame:
    """
    Read CSV file from S3 and return a pandas DataFrame. Special handling for CSV files with and without headers.
    """
    # Sample a small part of the CSV file to determine if there is a header
    sample_csv = pd.read_csv(url, nrows=10, storage_options=s3_opts).to_csv(index=False)
    has_header = sniffer.has_header(sample_csv)

    if has_header:
        df = pd.concat(
            pd.read_csv(
                url,
                chunksize=CHUNK_SIZE,
                nrows=num_rows_to_sample,
                storage_options=s3_opts,
            ),
            ignore_index=True,
        )
    else:
        df = pd.concat(
            pd.read_csv(
                url,
                header=None,
                chunksize=CHUNK_SIZE,
                nrows=num_rows_to_sample,
                storage_options=s3_opts,
            ),
            ignore_index=True,
        )
    return df


def flatten_json(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flattens any nested JSON data to a single column
    {"customerDetails": {"technicalContact": {"email": "...."}}}" => customerDetails.technicalContact.email
    """
    normalized_df = pd.json_normalize(df.to_dict(orient="records"))
    return drop_null_parents(normalized_df)


def drop_null_parents(df: pd.DataFrame) -> pd.DataFrame:
    # Identify null columns
    null_columns = {col for col in df.columns if df[col].isnull().all()}  # type: ignore

    # Identify nested columns
    parent_columns = {col for col in df.columns if "." in col}

    # For null parent columns, drop them if they will be represented by the nested columns
    columns_to_drop = [
        null_column
        for null_column in null_columns
        for parent_column in parent_columns
        if null_column != parent_column and null_column in parent_column
    ]
    return df.drop(columns=columns_to_drop)


def append_s3_url_prefix(bucket_name: str, url: str) -> str:
    return "s3://" + bucket_name + "/" + url if not url.startswith("s3://") else url


def strip_s3_bucket_prefix(bucket_name: str) -> str:
    return bucket_name.removeprefix("s3://")


def get_schema_from_s3_files(
    bucket: str,
    event_name: str,
    s3_urls: set[str],
    row_sample_count: Optional[int],
    skip_profiling: bool = False,
) -> Optional[S3DetectionResult]:
    """
    Get schema along with data profile from given S3 file urls (only CSV, JSON, and parquet currently supported).
    Args:
        bucket_name (str): S3 bucket name.
        event_name (str): Event name.
        s3_urls (list[str]): List of S3 URLs.
        row_sample_count (int): Number of rows to sample per S3 file.
    Returns:
        S3DetectionResult: Merged schema and data profile if able to be computed.
    """
    actual_row_sample_count = row_sample_count or DEFAULT_NUM_ROWS_TO_SAMPLE
    urls = [append_s3_url_prefix(bucket, url) for url in s3_urls]
    s3_data = read_s3_files(urls, actual_row_sample_count)
    if len(s3_data) > 0:
        schema = merge_schemas(
            [
                NativeS3Converter().to_recap(
                    df_result.df, df_result.has_schema, event_name
                )
                for _, df_result in s3_data.items()
                if len(df_result.df.columns) > 0
            ]
        )
        if skip_profiling:
            log_debug(f"Skipping data profiling for event name: {event_name}")
            return S3DetectionResult(schema)
        else:
            profiles = get_data_asset_field_profiles_for_data_asset(
                schema,
                {file_url: df_data.df for file_url, df_data in s3_data.items()},
                event_name,
                SamplingParameters(rowSampleCount=actual_row_sample_count),
            )
            return S3DetectionResult(schema, profiles)


def merge_schemas(schemas: list[dict]) -> dict:
    """
    Merge multiple schemas into a single schema.
    Args:
        schemas (list[dict]): List of schemas.
    Returns:
        dict: Merged schema.
    """
    # Dictionary of final fields, will be turned into a struct type at the end
    result_dict: dict[str, dict] = {}
    for schema in schemas:
        if "fields" in schema:
            for field in schema["fields"]:
                field_name = field["name"]
                # If the field is not yet in the result, just add it
                if field_name not in result_dict:
                    result_dict[field_name] = field
                elif field != result_dict[field_name]:
                    # If both types are structs, recursively merge them
                    if (
                        field["type"] == "struct"
                        and result_dict[field_name]["type"] == "struct"
                    ):
                        result_dict[field_name] = {
                            "fields": merge_schemas([result_dict[field_name], field])[
                                "fields"
                            ],
                            "name": field_name,
                            "type": "struct",
                        }
                    else:
                        # Merge the two type into a union, taking into account that one or both of them
                        # may already be unions
                        result_types = (
                            result_dict[field_name]["types"]
                            if result_dict[field_name]["type"] == "union"
                            else [result_dict[field_name]]
                        )
                        field_types = (
                            field["types"] if field["type"] == "union" else [field]
                        )
                        result_dict[field_name] = {
                            "type": "union",
                            "types": get_distinct_dictionaries(
                                remove_names(result_types) + remove_names(field_types)
                            ),
                            "name": field_name,
                        }

    return {"fields": list(result_dict.values()), "type": "struct"}


def get_distinct_dictionaries(dictionaries: list[dict]) -> list[dict]:
    """
    Get distinct dictionaries from a list of dictionaries.
    Args:
        dictionaries (list[dict]): List of dictionaries.
    Returns:
        list[dict]: List of distinct dictionaries.
    """
    # Remove duplicates, use a list instead of a set to avoid
    # errors about unhashable types
    distinct = []
    for d in dictionaries:
        if d not in distinct:
            distinct.append(d)
    # Sort for testing so we have deterministic results
    return sorted(
        distinct,
        key=lambda x: x["type"],
    )


def remove_names(list: list[dict]) -> list[dict]:
    """
    Remove names from a list of dictionaries.
    Args:
        list (dict): List of dictionaries.
    Returns:
        dict: List of dictionaries without names.
    """
    for t in list:
        if "name" in t:
            del t["name"]
    return list
