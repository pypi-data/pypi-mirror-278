import functools
import os
import re
import sys
import traceback
from enum import Enum
from typing import Literal, Optional

import click
from click_option_group import OptionGroup, optgroup
from gable.client import GableCliClient
from gable.helpers.logging import configure_debug_logger, configure_trace_logger
from gable.helpers.multi_option import MultiOption
from loguru import logger

gable_api_endpoint = None
gable_api_key = None


class SourceType(Enum):
    POSTGRES = "postgres"
    MYSQL = "mysql"
    AVRO = "avro"
    PROTOBUF = "protobuf"
    JSON_SCHEMA = "json_schema"
    PYTHON = "python"
    TYPESCRIPT = "typescript"
    PYSPARK = "pyspark"
    S3 = "s3"


ALL_SOURCE_TYPE_VALUES = [source_type.value for source_type in SourceType]
DATABASE_SOURCE_TYPE_VALUES = [SourceType.POSTGRES.value, SourceType.MYSQL.value]
FILE_SOURCE_TYPE_VALUES = [
    SourceType.AVRO.value,
    SourceType.PROTOBUF.value,
    SourceType.JSON_SCHEMA.value,
]
STATIC_CODE_ANALYSIS_SOURCE_TYPE_VALUES = [
    SourceType.PYTHON.value,
    SourceType.TYPESCRIPT.value,
    SourceType.PYSPARK.value,
    SourceType.S3.value,
]
SCHEMA_SOURCE_TYPE_VALUES = DATABASE_SOURCE_TYPE_VALUES + FILE_SOURCE_TYPE_VALUES


class TypescriptLibrary(Enum):
    BRANDVIEWS = "brandviews"
    SEGMENT = "segment"


ALL_TYPESCRIPT_LIBRARY_VALUES = [library.value for library in TypescriptLibrary]


class Context:
    def __init__(self):
        self.client: Optional[GableCliClient] = None


def create_client_callback(ctx, param, value):
    if param.name == "endpoint":
        global gable_api_endpoint
        gable_api_endpoint = value
    elif param.name == "api_key":
        global gable_api_key
        gable_api_key = value
    if gable_api_endpoint and gable_api_key:
        if ctx.obj is None:
            ctx.obj = Context()
        # Once we've collected both values, create the client
        logger.debug(f"Creating Gable client with endpoint {gable_api_endpoint}")
        ctx.obj.client = GableCliClient(
            endpoint=gable_api_endpoint, api_key=gable_api_key
        )
        # Test the connection to the API
        try:
            ctx.obj.client.get_ping()
        except Exception as e:
            logger.error(f"Failed to connect to Gable API: {e}")
            sys.exit(1)
    return value


def help_option(func):
    """Re-adds the help option, which fixes the eagerness issue with required parameters... Without this, if a parameter
    is marked as required, <command> --help will fail because the required parameters are not provided.
    """

    @click.help_option(is_eager=True)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def endpoint_options(func, global_option_group: OptionGroup):
    """Decorator that adds global endpoint options to a command. This decorator is added by the below global_options
    decorator, so it should not be used directly"""

    @global_option_group.option(
        "--endpoint",
        default=lambda: os.environ.get("GABLE_API_ENDPOINT", ""),
        required=True,
        # Don't pass these values to the subcommand functions
        expose_value=False,
        callback=create_client_callback,
        help="Customer API endpoint for Gable, in the format https://api.company.gable.ai/. Can also be set with the GABLE_API_ENDPOINT environment variable.",
    )
    @global_option_group.option(
        "--api-key",
        default=lambda: os.environ.get("GABLE_API_KEY", ""),
        required=True,
        # Don't pass these values to the subcommand functions
        expose_value=False,
        callback=create_client_callback,
        help="API Key for Gable. Can also be set with the GABLE_API_KEY environment variable.",
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def logging_options(func, global_option_group: OptionGroup):
    """Decorator that adds global logging options to a command. This decorator is added by the below global_options
    decorator, so it should not be used directly"""

    @global_option_group.option(
        "--debug",
        help="Enable debug logging",
        is_flag=True,
        default=False,
        # Make eager so we can configure logging before the other options are parsed
        is_eager=True,
        # Unintuitive, but we need to set this to true even though we don't actually want to pass this value to the
        # subcommand functions. We need this in the below function wrapper to determine if we should log detailed
        # exception information. This will be stripped out of the kwargs before they are passed to the subcommand
        expose_value=True,
        callback=configure_debug_logger,
    )
    @global_option_group.option(
        "--trace",
        help="Enable trace logging. This is the most verbose logging level and should only be used for debugging.",
        is_flag=True,
        default=False,
        # Make eager so we can configure logging before the other options are parsed
        is_eager=True,
        # Unintuitive, but we need to set this to true even though we don't actually want to pass this value to the
        # subcommand functions. We need this in the below function wrapper to determine if we should log detailed
        # exception information. This will be stripped out of the kwargs before they are passed to the subcommand
        expose_value=True,
        callback=configure_trace_logger,
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Check if debug logging is enabled
        debug_logging_enabled = "debug" in kwargs and kwargs["debug"]
        trace_logging_enabled = "trace" in kwargs and kwargs["trace"]
        # We need to remove the debug/trace flags from the kwargs before passing them to the subcommand functions
        # because they don't expect it
        if "debug" in kwargs:
            del kwargs["debug"]
        if "trace" in kwargs:
            del kwargs["trace"]
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if debug_logging_enabled or trace_logging_enabled:
                # If trace logging is enabled, log the full exception information
                if trace_logging_enabled:
                    logger.exception(traceback.format_exc())
                # Otherwise, just log the exception message
                else:
                    logger.exception(str(e))
                # Then immediately exit to prevent the default click exception handler from printing the exception
                # again. If this is a ClickException, grab the exit code and use that, otherwise use 1
                exit_code = e.exit_code if isinstance(e, click.ClickException) else 1
                # The context should always be available here, but just in case it isn't use sys.exit() instead
                context = click.get_current_context(silent=True)
                if context:
                    context.exit(exit_code)
                sys.exit(exit_code)
            # If debug logging is not enabled, just raise the exception and let the default click exception handler
            # print it
            raise e

    return wrapper


def global_options(add_endpoint_options=True):
    """Decorator that adds global options to a command. This decorator should be applied to all commands to add the
    --debug/--trace options, and conditionally (though almost always) add the --endpoint/--api-key options.
    """

    def decorate(func):
        func = help_option(func)
        global_option_group = OptionGroup("Global Options")
        func = logging_options(func, global_option_group)
        if add_endpoint_options:
            # Return the function unchanged, not decorated.
            func = endpoint_options(func, global_option_group)

        return func

    return decorate


def required_option_callback(ctx, param, value):
    """This callback is used to enforce required options when the option needs to be eager, which can cause problems
    with the --help flag"""
    if not value or str(value).strip() == "":
        raise click.MissingParameter(ctx=ctx, param=param)
    return value


def check_for_empty_string_callback(ctx, param, value):
    """This callback is used to check for optional options that were specified, but might be an empty string"""
    if value != None and str(value).strip() == "":
        raise click.BadParameter("Cannot be an empty string", ctx=ctx, param=param)
    return value


def source_type_dependent_required_option_callback(ctx, param, value):
    """
    This callback is used to conditionally enforce option requirements based on the source type.
    It also checks if the correct number of include patterns is provided when the source type requires historical data comparison.

    Args:
        ctx: Click context, which holds all the parameters and their values.
        param: The parameter currently being processed.
        value: The value of the parameter.

    Raises:
        click.MissingParameter: If a required parameter is missing.
        click.BadParameter: If an unexpected value is processed.
        ValueError: If incorrect number of include patterns are provided for historical analysis.

    Returns:
        The value if no errors are raised.
    """
    source_type: SourceType = ctx.params.get("source_type")

    if source_type in DATABASE_SOURCE_TYPE_VALUES:
        # Only require the options for the database source type
        if param.group.name == "Database Options" and not value:
            raise click.MissingParameter(ctx=ctx, param=param)
    elif source_type in FILE_SOURCE_TYPE_VALUES:
        # Only require the options for the file source type
        if param.group.name == "Protobuf & Avro options" and not value:
            raise click.MissingParameter(ctx=ctx, param=param)
    elif source_type == SourceType.PYTHON.value:
        if param.group.name == "Python Project Options" and not value:
            raise click.MissingParameter(ctx=ctx, param=param)
        python_event_name_key_validator(param, value)
    elif source_type == SourceType.PYSPARK.value:
        if param.group.name == "Pyspark Project Options" and not value:
            raise click.MissingParameter(ctx=ctx, param=param)
    elif source_type == SourceType.TYPESCRIPT.value:
        if param.group.name == "Typescript Project Options" and not value:
            raise click.MissingParameter(ctx=ctx, param=param)
    elif source_type == SourceType.S3.value:
        if param.group.name == "S3 Project Options" and not value:
            raise click.MissingParameter(ctx=ctx, param=param)
        if param.name == "include" and (not value or len(value) != 2):
            raise click.BadParameter(
                "Exactly two include patterns are required for historical data asset detection.",
                ctx=ctx,
                param=param,
            )
    else:
        # Should never happen, but just in case
        raise click.BadParameter("", ctx=ctx, param=param)
    return value


def python_event_name_key_validator(param: click.Parameter, value: str) -> None:
    # Event name key must be a valid access path:
    # 1. The string can start with a word (letters, digits, underscores), *, [*], or [<index>].
    # 2. If there is a dot separator, it should be followed by a word, [*], or [<index>]. This process can repeat (zero or more times).
    # 3. The string must end with a word.
    if param.opts[0] == "--event-name-key" and not re.match(
        r"^(\w+|\*|\[\*\]|\[-?[0-9]+\])(\.(\w+|\[\*\]|\[-?[0-9]+\]))*\w+$", value
    ):
        raise click.BadParameter(value + " must be valid event name access path")


@logger.catch()
def python_project_options(
    option_group_help_text: str, action: Literal["register", "check"]
):
    """Decorator that adds Python project related options to a command like 'data-asset register'.

    The 'action' option is used to tweak the help text depending on the command being run. If a new value is
    added, make sure it works as {action}ed and {action}ing (e.g. registered and registering, checked and checking)
    """

    def decorator(func):
        @optgroup.group(
            "Python Project Options",
            help=option_group_help_text,
        )
        @optgroup.option(
            "--project-root",
            help="This should be the directory location of the Python project that will be analyzed.",
            callback=source_type_dependent_required_option_callback,
            type=str,
        )
        @optgroup.option(
            "--emitter-function",
            help="Name of the emitter function",
            callback=source_type_dependent_required_option_callback,
            type=str,
        )
        @optgroup.option(
            "--emitter-payload-parameter",
            help="Name of the parameter representing the event payload",
            callback=source_type_dependent_required_option_callback,
            type=str,
        )
        @optgroup.option(
            "--event-name-key",
            help="Input must be a \".\" delimited list of field property access directives or array indexes to the event name key field. The field property access directive is a valid dictionary key, or the wildcard character *. The array index is square brackets[] with either a digit in it (targeting a specific element of the array), or * (targeting all elements in the array).\n\nExample: \"fieldName.[0].eventName\" describes the access pay to the event name in: {'fieldName': [{'eventName': 'event_one'}]}.",
            callback=source_type_dependent_required_option_callback,
            type=str,
        )
        @optgroup.option(
            "--emitter-file-path",
            help="Relative path from the root of the project to the file that contains the emitter function",
            callback=source_type_dependent_required_option_callback,
            type=str,
        )
        @optgroup.option(
            "--exclude",
            help="Comma separated list of paths to be excluded from the analysis, with support for glob patterns. Gable automatically excludes '**/node_modules, **/__pycache__, **/.*'. Example: '**/tests,docs/*'",
            type=str,
        )
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


@logger.catch()
def pyspark_project_options(
    option_group_help_text: str, action: Literal["register", "check"]
):
    """Decorator that adds Pyspark project related options to a command like 'data-asset register'.

    The 'action' option is used to tweak the help text depending on the command being run. If a new value is
    added, make sure it works as {action}ed and {action}ing (e.g. registered and registering, checked and checking)
    """

    def decorator(func):
        @optgroup.group(
            "Pyspark Project Options",
            help=option_group_help_text,
        )
        @optgroup.option(
            "--project-root",
            help="This should be the directory location of the project containing the Pyspark job that will analyzed.",
            callback=source_type_dependent_required_option_callback,
            type=str,
        )
        @optgroup.option(
            "--spark-job-entrypoint",
            help='Entrypoint to execute spark job, starting with python file and including any arguments. Example: "main.py --arg1 value1 --arg2 value2"',
            callback=source_type_dependent_required_option_callback,
            type=str,
        )
        @optgroup.option(
            "--connection-string",
            help="Connection string to the Hive metastore",
            type=str,
            default=None,
        )
        @optgroup.option(
            "--csv-schema-file",
            help="Path to the CSV schema file",
            type=str,
            default=None,
        )
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


@logger.catch()
def file_source_type_options(
    option_group_help_text: str, action: Literal["register", "check"]
):
    """Decorator that adds file source type (protobuf, avro, etc) related options to a command like 'data-asset register'.

    The 'action' option is used to tweak the help text depending on the command being run. If a new value is
    added, make sure it works as {action}ed and {action}ing (e.g. registered and registering, checked and checking)
    """

    def decorator(func):
        @optgroup.group(
            "Protobuf & Avro options",
            help=option_group_help_text,
        )
        @optgroup.option(
            "--files",
            help=f"Space delimited path(s) to the contracts to {action}, with support for glob patterns.",
            type=tuple,
            callback=source_type_dependent_required_option_callback,
            cls=MultiOption,
        )
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


@logger.catch()
def typescript_project_options(
    option_group_help_text: str, action: Literal["register", "check"]
):
    """Decorator that adds Typescript project related options to a command like 'data-asset register'.

    The 'action' option is used to tweak the help text depending on the command being run. If a new value is
    added, make sure it works as {action}ed and {action}ing (e.g. registered and registering, checked and checking)
    """

    def decorator(func):
        @optgroup.group(
            "Typescript Project Options",
            help=option_group_help_text,
        )
        @optgroup.option(
            "--library",
            help="This should indicate the library emitting the events you want detected as data assets.",
            callback=source_type_dependent_required_option_callback,
            type=click.Choice(ALL_TYPESCRIPT_LIBRARY_VALUES),
        )
        @optgroup.option(
            "--project-root",
            help="This should be the directory location of the Typescript project that will be analyzed.",
            callback=source_type_dependent_required_option_callback,
            type=str,
        )
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


def proxy_database_options(
    option_group_help_text: str, action: Literal["register", "check"]
):
    """Decorator that adds database + proxy database related options to a command like 'data-asset register'.

    The 'action' option is used to tweak the help text depending on the command being run. If a new value is
    added, make sure it works as {action}ed and {action}ing (e.g. registered and registering, checked and checking)
    """

    def decorator(func):
        @optgroup.group(
            "Database Options",
            help=option_group_help_text,
        )
        @optgroup.option(
            "--host",
            "-h",
            type=str,
            callback=source_type_dependent_required_option_callback,
            help="""The host name of the production database, for example 'service-one.xxxxxxxxxxxx.us-east-1.rds.amazonaws.com'.
            Despite not needing to connect to the production database, the host is still needed to generate the unique resource 
            name for the real database tables (data assets).
            """,
        )
        @optgroup.option(
            "--port",
            "-p",
            type=int,
            callback=source_type_dependent_required_option_callback,
            help="""The port of the production database. Despite not needing to connect to the production database, the port is 
            still needed to generate the unique resource name for the real database tables (data assets).
            """,
        )
        @optgroup.option(
            "--db",
            type=str,
            callback=source_type_dependent_required_option_callback,
            help="""The name of the production database. Despite not needing to connect to the production database, the database 
            name is still needed to generate the unique resource name for the real database tables (data assets).
            
            Database naming convention frequently includes the environment (production/development/test/staging) in the 
            database name, so this value may not match the name of the database in the proxy database instance. If this is 
            the case, you can set the --proxy-db value to the name of the database in the proxy instance, but we'll use the 
            value of --db to generate the unique resource name for the data asset.
            
            For example, if your production database is 'prod_service_one', but your test database is 'test_service_one', 
            you would set --db to 'prod_service_one' and --proxy-db to 'test_service_one'.""",
        )
        @optgroup.option(
            "--schema",
            "-s",
            type=str,
            callback=source_type_dependent_required_option_callback,
            help=f"""The schema of the production database containing the table(s) to {action}. Despite not needing to connect to 
            the production database, the schema is still needed to generate the unique resource name for the real database tables
            (data assets).
            
            Database naming convention frequently includes the environment (production/development/test/staging) in the 
            schema name, so this value may not match the name of the schema in the proxy database instance. If this is 
            the case, you can set the --proxy-schema value to the name of the schema in the proxy instance, but we'll use the 
            value of --schema to generate the unique resource name for the data asset.
            
            For example, if your production schema is 'production', but your test database is 'test', 
            you would set --schema to 'production' and --proxy-schema to 'test'.""",
        )
        @optgroup.option(
            "--table",
            "--tables",
            "-t",
            type=str,
            callback=check_for_empty_string_callback,
            default=None,
            help=f"""A comma delimited list of the table(s) to {action}. If no table(s) are specified, all tables within the provided schema will be {action}ed.

            Table names in the proxy database instance must match the table names in the production database instance, even if
            the database or schema names are different.""",
        )
        @optgroup.option(
            "--proxy-host",
            "-ph",
            type=str,
            callback=source_type_dependent_required_option_callback,
            help=f"""The host string of the database instance that serves as the proxy for the production database. This is the 
            database that Gable will connect to when {action}ing tables in the CI/CD workflow. 
            """,
        )
        @optgroup.option(
            "--proxy-port",
            "-pp",
            type=int,
            callback=source_type_dependent_required_option_callback,
            help=f"""The port of the database instance that serves as the proxy for the production database. This is the 
            database that Gable will connect to when {action}ing tables in the CI/CD workflow. 
            """,
        )
        @optgroup.option(
            "--proxy-db",
            "-pdb",
            type=str,
            callback=check_for_empty_string_callback,
            default=None,
            help="""Only needed if the name of the database in the proxy instance is different than the name of the
            production database. If not specified, the value of --db will be used to generate the unique resource name for 
            the data asset. 
            
            For example, if your production database is 'prod_service_one', but your test database is 'test_service_one', 
            you would set --db to 'prod_service_one' and --proxy-db to 'test_service_one'.
            """,
        )
        @optgroup.option(
            "--proxy-schema",
            "-ps",
            type=str,
            callback=check_for_empty_string_callback,
            default=None,
            help="""Only needed if the name of the schema in the proxy instance is different than the name of the schema in the
            production database. If not specified, the value of --schema will be used to generate the unique resource name for 
            the data asset. 
            
            For example, if your production schema is 'production', but your test database is 'test', you would set --schema to
            'production' and --proxy-schema to 'test'.
            """,
        )
        @optgroup.option(
            "--proxy-user",
            "-pu",
            type=str,
            callback=source_type_dependent_required_option_callback,
            help=f"""The user that will be used to connect to the proxy database instance that serves as the proxy for the production 
            database. This is the database that Gable will connect to when {action}ing tables in the CI/CD workflow. 
            """,
        )
        @optgroup.option(
            "--proxy-password",
            "-ppw",
            type=str,
            default=None,
            help=f"""If specified, the password that will be used to connect to the proxy database instance that serves as the proxy for 
            the production database. This is the database that Gable will connect to when {action}ing tables in the CI/CD workflow. 
            """,
        )
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


@logger.catch()
def s3_project_options(
    option_group_help_text: str, action: Literal["register", "check"]
):
    """Decorator that adds S3 related options to a command like 'data-asset register'.

    The 'action' option is used to tweak the help text depending on the command being run. If a new value is
    added, make sure it works as {action}ed and {action}ing (e.g. registered and registering, checked and checking)
    """

    def decorator(func):

        @optgroup.group(
            "S3 Project Options",
            help=option_group_help_text,
        )
        @optgroup.option(
            "--bucket",
            help="This should indicate the S3 bucket containing the files to be analyzed.",
            callback=source_type_dependent_required_option_callback,
            type=str,
        )
        @optgroup.option(
            "--include",
            help="This optional parameter allows you to specify what to include in your S3 bucket. If not specified, all files in the bucket will be analyzed.",
            multiple=True,
        )
        @optgroup.option(
            "--lookback-days",
            type=int,
            default=1,
            help="""Number of days to look back from the latest day in the list of paths, defaults to 1. 
            For example if the latest path is 2024/01/02, and lookback_days is 3, then the paths return
            will have 2024/01/02, 2024/01/01, and 2023/12/31
            """,
        )
        @optgroup.option(
            "--history",
            help="This optional parameter allows you to do a historical analysis of between 2 dates.",
            type=bool,
            is_flag=True,
            default=False,
        )
        @optgroup.option(
            "--skip-profiling",
            help="This optional parameter allows you to turn off data profiling.",
            type=bool,
            is_flag=True,
            default=False,
        )
        @optgroup.option(
            "--row-sample-count",
            type=int,
            default=1000,
            help="""Number of rows of data per file to sample for schema detection and data profiling. Default is 1000.
            Accuracy increases with larger sample size, but processing time and AWS costs also increases.
            """,
        )
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator
