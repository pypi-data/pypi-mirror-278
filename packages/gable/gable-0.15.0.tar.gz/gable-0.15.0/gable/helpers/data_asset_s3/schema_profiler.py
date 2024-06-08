from typing import Optional

import numpy as np
import pandas as pd
from gable.helpers.data_asset_s3.logger import log_error
from gable.helpers.data_asset_s3.path_pattern_manager import (
    UUID_REGEX_V1,
    UUID_REGEX_V3,
    UUID_REGEX_V4,
    UUID_REGEX_V5,
)
from gable.openapi import (
    DataAssetFieldProfile,
    DataAssetFieldProfileBoolean,
    DataAssetFieldProfileList,
    DataAssetFieldProfileNumber,
    DataAssetFieldProfileOther,
    DataAssetFieldProfileString,
    DataAssetFieldProfileTemporal,
    DataAssetFieldProfileUnion,
    DataAssetFieldProfileUUID,
    DataAssetFieldsToProfilesMapping,
    SamplingParameters,
)
from loguru import logger


def get_data_asset_field_profiles_for_data_asset(
    recap_schema: dict,
    file_to_df: dict[str, pd.DataFrame],
    event_name: str,
    sampling_params: SamplingParameters,
) -> Optional[DataAssetFieldsToProfilesMapping]:
    """
    given a mapping of column name to pandas dataframe, return a mapping of column names to data asset field profiles
    """
    logger.debug(f"Attempting to compute data asset profile for asset: {event_name}")

    try:
        df = pd.concat(file_to_df.values())
        file_list = list(file_to_df.keys())
        result: dict[str, DataAssetFieldProfile] = {}

        column_name_to_schema: dict[str, dict] = {}
        _populate_column_schemas(recap_schema, column_name_to_schema)
        for column_name, column_schema in column_name_to_schema.items():
            if column_name not in df.columns:
                log_error(
                    f"column {column_name} not found in data - skipping in data asset profile"
                )
            else:
                try:
                    result[column_name] = _get_data_asset_field_profile_for_column(
                        column_schema, df[column_name], file_list, sampling_params  # type: ignore
                    )
                except Exception as e:
                    log_error(
                        f"Error computing data asset profile for column {column_name} in asset {event_name}: {e}"
                    )

        return DataAssetFieldsToProfilesMapping(__root__=result)
    except Exception as e:
        log_error(f"Error computing data asset profiles for asset {event_name}: {e}")


def _populate_column_schemas(
    recap_schema: dict, map: dict[str, dict], prefix: str = ""
):
    for column_schema in recap_schema["fields"]:
        column_name = column_schema["name"]
        if "fields" in column_schema:
            # If the schema is a struct type, we need to go into the nested level
            _populate_column_schemas(column_schema, map, prefix + column_name + ".")
        else:
            map[prefix + column_name] = column_schema


def _get_data_asset_field_profile_for_column(
    schema: dict,
    column: pd.Series,
    file_list: list[str],
    sampling_params: SamplingParameters,
    nullable: bool = False,
) -> DataAssetFieldProfile:
    """
    given a column name and a pandas series, return a data asset field profile
    """
    res = None
    null_count = None
    sampled_records_count = len(column)
    if schema["type"] == "union":
        non_null_schemas = [
            field for field in schema["types"] if field["type"] != "null"
        ]
        if (
            len(non_null_schemas) == 1
        ):  # it not a proper union, it's just representing a nullable field
            nullable = True
            schema = non_null_schemas[0]
        else:
            non_null_profiles: list[DataAssetFieldProfile] = [
                _get_data_asset_field_profile_for_column(
                    schema, column, file_list, sampling_params, nullable
                )
                for schema in non_null_schemas
            ]
            res = DataAssetFieldProfileUnion(
                profileType="union",
                sampledRecordsCount=sampled_records_count,
                nullable=False,
                profiles=non_null_profiles,
                sampledFiles=file_list,
                samplingParameters=sampling_params,
            )

    null_count = column.isnull().sum() if nullable else None
    column_without_empty_null = column.replace("", np.nan).dropna()
    if schema["type"] == "boolean":
        res = DataAssetFieldProfileBoolean(
            profileType="boolean",
            sampledRecordsCount=sampled_records_count,
            nullable=nullable,
            nullCount=null_count,
            trueCount=column_without_empty_null.sum(),
            falseCount=sampled_records_count - column_without_empty_null.sum(),
            sampledFiles=file_list,
            samplingParameters=sampling_params,
        )
    elif schema["type"] in ("int", "float"):
        if schema["type"] == "int" and any(
            [
                schema.get("logical", None) == logical
                for logical in ["Timestamp", "Date"]
            ]
        ):
            res = DataAssetFieldProfileTemporal(
                profileType="temporal",
                sampledRecordsCount=sampled_records_count,
                nullable=nullable,
                nullCount=null_count,
                min=column_without_empty_null.min(),
                max=column_without_empty_null.max(),
                format="",  # TODO: revisit how to support with MM, DD, YY notation
                sampledFiles=file_list,
                samplingParameters=sampling_params,
            )
        else:
            res = DataAssetFieldProfileNumber(
                profileType="number",
                sampledRecordsCount=sampled_records_count,
                nullable=nullable,
                nullCount=null_count,
                uniqueCount=column_without_empty_null.nunique(),
                min=column_without_empty_null.min(),
                max=column_without_empty_null.max(),
                sampledFiles=file_list,
                samplingParameters=sampling_params,
            )
    elif schema["type"] == "string":
        for version, regex in [
            (1, UUID_REGEX_V1),
            (3, UUID_REGEX_V3),
            (4, UUID_REGEX_V4),
            (5, UUID_REGEX_V5),
        ]:
            if column_without_empty_null.str.fullmatch(rf"^{regex}$", case=False).all():
                res = DataAssetFieldProfileUUID(
                    profileType="uuid",
                    sampledRecordsCount=sampled_records_count,
                    nullable=nullable,
                    nullCount=null_count,
                    uuidVersion=version,
                    emptyCount=(column == "").sum(),
                    uniqueCount=column_without_empty_null.nunique(),
                    maxLength=column_without_empty_null.str.len().max(),
                    minLength=column_without_empty_null.str.len().min(),
                    sampledFiles=file_list,
                    samplingParameters=sampling_params,
                    # TODO - add format
                )
                break
        if res is None:
            res = DataAssetFieldProfileString(
                profileType="string",
                sampledRecordsCount=sampled_records_count,
                nullable=nullable,
                nullCount=null_count,
                emptyCount=(column == "").sum(),
                uniqueCount=column_without_empty_null.nunique(),
                maxLength=column_without_empty_null.str.len().max(),
                minLength=column_without_empty_null.str.len().min(),
                sampledFiles=file_list,
                samplingParameters=sampling_params,
            )
    elif schema["type"] == "list":
        res = DataAssetFieldProfileList(
            profileType="list",
            sampledRecordsCount=sampled_records_count,
            nullable=nullable,
            nullCount=null_count,
            maxLength=column_without_empty_null.str.len().max(),
            minLength=column_without_empty_null.str.len().min(),
            sampledFiles=file_list,
            samplingParameters=sampling_params,
        )
    else:
        res = DataAssetFieldProfileOther(
            profileType="other",
            sampledRecordsCount=sampled_records_count,
            nullable=nullable,
            nullCount=null_count,
            sampledFiles=file_list,
            samplingParameters=sampling_params,
        )
    return DataAssetFieldProfile(__root__=res)
