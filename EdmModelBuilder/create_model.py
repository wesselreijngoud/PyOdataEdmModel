# This file adheres to the "black" code formatting style.
# More information about black: https://github.com/psf/black
import json
from collections import defaultdict

import pandas as pd

from EdmModel.EdmModel.EdmModel import ODataEdmBuilder
from EdmModel.EdmModel.odata_mapper import OdataConverter

OdataConverter = OdataConverter("sqlserver", r"EdmModel\EdmModel\template.json")


def create_edm_model_from_sql_result(
    namespace_name: str,
    service_name: str,
    schema_name: str,
    container_name: str,
    json_result: str,
):
    """
    Create an EDM (Entity Data Model) model based on SQL query results.

    This function takes SQL query results in JSON format and generates an EDM model
    using the provided namespace, service name, schema name, and container name.

    Args:
        namespace_name (str): The namespace for the EDM model.
        service_name (str): The name of the service associated with the EDM model.
        schema_name (str): The name of the schema to organize the entities.
        container_name (str): The name of the entity container.
        json_result (str): The SQL query result in JSON format.

    Returns:
        ODataEdmMetadataBuilder: An instance of the ODataEdmMetadataBuilder class
                                containing the generated EDM model.
    """
    try:
        # Parse JSON result into a Python dictionary
        result = json.loads(json_result)
    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON format in json_result") from e
    builder = ODataEdmBuilder(namespace_name, service_name)
    schema = builder.add_schema(schema_name)
    container = builder.add_entity_container(schema, container_name)

    table_info = {}

    for item in result:
        table_name = item["TABLE_NAME"]
        column_name = item["COLUMN_NAME"]
        data_type = item["DATA_TYPE"]
        is_nullable = item["IS_NULLABLE"] == "YES"
        primary_key = [item["COLUMN_NAME"]] if item["IS_PK"] == 1 else []
        foreign_key_col = item["REFERENCING_COLUMN"]
        to_col_fk_ref = item["REFERENCED_COLUMN"]
        to_tbl_fk_ref = item["REFERENCED_TABLE"]
        max_length = item["MaxLength"]
        precision = item["Precision"]
        scale = item["Scale"]
        table_info.setdefault(table_name, []).append(
            (
                column_name,
                data_type,
                primary_key,
                is_nullable,
                foreign_key_col,
                to_col_fk_ref,
                to_tbl_fk_ref,
                max_length,
                precision,
                scale,
            )
        )

    for table, columns in table_info.items():
        entity_type = builder.add_entity_type(schema, table)
        for (
            column,
            data_type,
            primary_key,
            is_nullable,
            foreign_key_col,
            to_col_fk_ref,
            to_tbl_fk_ref,
            max_length,
            precision,
            scale,
        ) in columns:
            for pk in primary_key:
                if pk and not is_nullable:
                    builder.add_key(
                        entity_type, pk, OdataConverter.convert_to_odata(data_type)
                    )
            if foreign_key_col:
                builder.add_navigation_property(
                    entity_type,
                    foreign_key_col,
                    to_col_fk_ref,
                    to_tbl_fk_ref,
                    is_nullable,
                )
            builder.add_property(
                entity_type,
                column,
                OdataConverter.convert_to_odata(data_type),
                is_nullable,
                max_length,
                precision,
                scale,
            )
        builder.add_entity_set(container, table, f"{namespace_name}.{table}")
        builder.validate_entity_type(entity_type)

    builder.generate_metadata()
    return builder


def create_edm_model_from_df_result(
    namespace_name: str,
    service_name: str,
    schema_name: str,
    container_name: str,
    df: pd.DataFrame,
):
    """
    Create an EDM (Entity Data Model) model based on a pandas DataFrame.

    This function takes SQL query results in JSON format and generates an EDM model
    using the provided namespace, service name, schema name, and container name.

    Args:
        namespace_name (str): The namespace for the EDM model.
        service_name (str): The name of the service associated with the EDM model.
        schema_name (str): The name of the schema to organize the entities.
        container_name (str): The name of the entity container.
        df (pd.DataFrame): The SQL query result in dataframe format.

    Returns:
        ODataEdmMetadataBuilder: An instance of the ODataEdmMetadataBuilder class
                                containing the generated EDM model.
    """
    builder = ODataEdmBuilder(namespace_name, service_name)
    schema = builder.add_schema(schema_name)
    container = builder.add_entity_container(schema, container_name)

    table_info = defaultdict(list)

    for index in range(len(df)):
        item = df.iloc[index]
        table_name = item.TABLE_NAME
        data_type = item.DATA_TYPE
        column_name = (
            item.COLUMN_NAME
            if not isinstance(data_type, int)
            else item.COLUMN_NAME.fillna(-1)
        )
        is_nullable = item.IS_NULLABLE == "YES"
        primary_key = [item.COLUMN_NAME] if item.IS_PK == 1 else []
        foreign_key_col = item.REFERENCING_COLUMN
        to_col_fk_ref = item.REFERENCED_COLUMN
        to_tbl_fk_ref = item.REFERENCED_TABLE
        max_length = item.MaxLength
        precision = item.Precision
        scale = item.Scale
        table_info[table_name].append(
            (
                column_name,
                data_type,
                primary_key,
                is_nullable,
                foreign_key_col,
                to_col_fk_ref,
                to_tbl_fk_ref,
                max_length,
                precision,
                scale,
            )
        )

    for table, columns in table_info.items():
        entity_type = builder.add_entity_type(schema, table)
        for (
            column,
            data_type,
            primary_key,
            is_nullable,
            foreign_key_col,
            to_col_fk_ref,
            to_tbl_fk_ref,
            max_length,
            precision,
            scale,
        ) in columns:
            for pk in primary_key:
                if pk and not is_nullable:
                    builder.add_key(
                        entity_type, pk, OdataConverter.convert_to_odata(data_type)
                    )
            if foreign_key_col:
                builder.add_navigation_property(
                    entity_type,
                    foreign_key_col,
                    to_col_fk_ref,
                    to_tbl_fk_ref,
                    is_nullable,
                )
            builder.add_property(
                entity_type,
                column,
                OdataConverter.convert_to_odata(data_type),
                is_nullable,
                max_length,
                precision,
                scale,
            )
        builder.add_entity_set(container, table, f"{namespace_name}.{table}")
        builder.validate_entity_type(entity_type)
    builder.generate_metadata()
    return builder
