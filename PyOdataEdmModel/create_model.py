# This file adheres to the "black" code formatting style.
# More information about black: https://github.com/psf/black
import json
import os
from collections import defaultdict

import pandas as pd

from PyOdataEdmModel.EdmModel import ODataEdmBuilder
from PyOdataEdmModel.odata_mapper import OdataConverter


def load_configuration():
    """
    Load configuration data from settings.json and template.json files.

    Returns:
        dict: A dictionary containing configuration data.
    """
    # Get the path of the directory containing this module
    module_dir = os.path.dirname(__file__)
    settings_file_path = os.path.join(module_dir, "config", "settings.json")
    template_file_path = os.path.join(module_dir, "config", "template.json")

    with open(settings_file_path, "r") as settings_file:
        settings_data = json.load(settings_file)
    return settings_data, template_file_path


settings_data, template_data = load_configuration()
database_client = settings_data["database_client"]
OdataConverter = OdataConverter(template_data, database_client)


def create_model_from_table_info(
    builder, schema: dict, container: dict, namespace_name: str, table_info: dict
):
    """
    Creates an Odata EDM model from a dictionary containing all needed metadata information.

    Args:
        builder (_type_): EDM Odata builder class instance
        schema (dict): The schema to add the EDM infomation to.
        container (dict): The entity container to add entitysets to.
        namespace_name (str): The namespace for the EDM model.
        table_info (dict): Contains all metadata from the extracted tables.
    Returns:
        ODataEdmMetadataBuilder: An instance of the ODataEdmBuilder class
                                containing the generated EDM model.
    """
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
        ODataEdmBuilder: An instance of the ODataEdmBuilder class
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
    return create_model_from_table_info(
        builder, schema, container, namespace_name, table_info
    )


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
        ODataEdmBuilder: An instance of the ODataEdmBuilder class
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
    return create_model_from_table_info(
        builder, schema, container, namespace_name, table_info
    )
