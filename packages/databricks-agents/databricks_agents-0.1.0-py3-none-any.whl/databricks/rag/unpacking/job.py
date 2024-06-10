import argparse
from typing import Tuple
from dbruntime import UserNamespaceInitializer
from databricks.rag.unpacking.unpack import (
    unpack_and_split_payloads,
    TraceSchemaVersion,
)
from databricks.rag.unpacking.entities import UnityCatalogTable
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import catalog
from databricks.sdk.errors.platform import ResourceDoesNotExist
import json
from pyspark.sql import functions as F
from pyspark.sql.types import Row
from databricks.rag.unpacking.schemas import MLFLOW_TRACE_SCHEMA_VERSION


def _get_checkpoint_table_name(table: UnityCatalogTable):
    return f"{table.table_name}_checkpoints"


def _get_checkpoint_table_full_name(table: UnityCatalogTable):
    return f"{table.full_name(escape=False)}_checkpoints"


def _get_checkpoint_volume_path(table: UnityCatalogTable):
    return f"/Volumes/{table.catalog_name}/{table.schema_name}/{_get_checkpoint_table_name(table)}/"


def _get_unpacked_tables(
    full_table_name: str,
) -> Tuple[UnityCatalogTable, UnityCatalogTable, UnityCatalogTable]:
    try:
        catalog, schema, table_name = full_table_name.split(".")
    except ValueError:
        raise ValueError(
            f"Table Name {full_table_name} has to be off the format catalog_name.schema_name.table_name"
        )

    return (
        UnityCatalogTable(catalog, schema, table_name),
        UnityCatalogTable(catalog, schema, table_name + "_request_logs"),
        UnityCatalogTable(catalog, schema, table_name + "_assessment_logs"),
    )


def _create_checkpoint_volume_if_not_exists(table: UnityCatalogTable):
    w = WorkspaceClient()

    # Try to read workspace
    try:
        w.volumes.read(_get_checkpoint_table_full_name(table))
    except ResourceDoesNotExist:
        # Create if it does not exist
        w.volumes.create(
            catalog_name=table.catalog_name,
            schema_name=table.schema_name,
            name=_get_checkpoint_table_name(table),
            volume_type=catalog.VolumeType.MANAGED,
        )


def get_request_log_first_row(table: UnityCatalogTable):
    user_namespace_initializer = UserNamespaceInitializer.getOrCreate()
    spark = user_namespace_initializer.namespace_globals["spark"]

    df = spark.read.table(table.full_name())
    request_payloads = df.filter(F.expr("response:predictions IS NULL"))
    first_row = request_payloads.head()
    return first_row


def run_stream(
    inference_log_table: UnityCatalogTable,
    request_logs_table: UnityCatalogTable,
    assessment_logs_table: UnityCatalogTable,
    first_row: Row,
):
    # Spark is not available by default inside the whl job, so we have to grab
    # it from the user namespace in order to set up our DatabricksContext
    user_namespace_initializer = UserNamespaceInitializer.getOrCreate()
    spark = user_namespace_initializer.namespace_globals["spark"]

    # Read from the Inference Log Table
    df = spark.readStream.table(inference_log_table.full_name())

    request_logs, assessment_logs = unpack_and_split_payloads(df, first_row)

    # Starting a stream with checkpoints to write Request Logs to the table
    (
        request_logs.writeStream.option(
            "checkpointLocation",
            _get_checkpoint_volume_path(request_logs_table),
        )
        .option("mergeSchema", "true")
        .format("delta")
        .outputMode("append")
        .trigger(availableNow=True)
        .toTable(request_logs_table.full_name())
    )
    # Starting a stream with checkpoints to write Assessment Logs to the table
    (
        assessment_logs.writeStream.option(
            "checkpointLocation", _get_checkpoint_volume_path(assessment_logs_table)
        )
        .option("mergeSchema", "true")
        .format("delta")
        .outputMode("append")
        .trigger(availableNow=True)
        .toTable(assessment_logs_table.full_name())
    )


def process_data(inference_log_full_table_name: str):
    table, request_logs_table, assessment_logs_table = _get_unpacked_tables(
        inference_log_full_table_name
    )
    # In the job, we get the first row and pass it into unpack_and_split_payloads.
    # Unpack and split payloads will use this to deduce trace version and unpack request logs.
    # We cannot get first row of a spark streaming dataframe. So we need this extra method to get the row.

    first_row = get_request_log_first_row(table)

    # No data yet
    if first_row is None:
        return

    _create_checkpoint_volume_if_not_exists(request_logs_table)
    _create_checkpoint_volume_if_not_exists(assessment_logs_table)

    run_stream(table, request_logs_table, assessment_logs_table, first_row)


def main():
    parser = argparse.ArgumentParser(description="Unpacking Job Argument Parser")
    parser.add_argument(
        "--inference_log_table_name",
        help="Name of Inference Log Table of format {catalog_name}.{schema_name}.{table_name}",
    )

    args = parser.parse_args()
    process_data(args.inference_log_table_name)


if __name__ == "__main__":
    main()
