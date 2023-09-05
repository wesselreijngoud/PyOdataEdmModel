# This file adheres to the "black" code formatting style.
# More information about black: https://github.com/psf/black
template = {
    "int": "Edm.Int32",
    "bigint": "Edm.Int64",
    "smallint": "Edm.Int16",
    "tinyint": "Edm.Byte",
    "bit": "Edm.Boolean",
    "float": "Edm.Double",
    "real": "Edm.Single",
    "decimal": "Edm.Decimal",
    "numeric": "Edm.Decimal",
    "money": "Edm.Decimal",
    "smallmoney": "Edm.Decimal",
    "datetime": "Edm.DateTimeOffset",
    "smalldatetime": "Edm.DateTimeOffset",
    "date": "Edm.Date",
    "time": "Edm.TimeOfDay",
    "char": "Edm.String",
    "varchar": "Edm.String",
    "text": "Edm.String",
    "nchar": "Edm.String",
    "nvarchar": "Edm.String",
    "ntext": "Edm.String",
    "binary": "Edm.Binary",
    "varbinary": "Edm.Binary",
    "image": "Edm.Binary",
    "uniqueidentifier": "Edm.Guid"
}


def convert_to_odata(data_type: str) -> str:
    """
    Takes a SQL Server data type as input, converts it to lowercase,
    and looks up the corresponding OData data type in the mapping dictionary.
    If no mapping is found, it defaults to 'Edm.String'.

    Args:
        sql_data_type (str): sql server datatype

    Returns:
        str: corresponding odata datatype (returns Edm.String if no match found)
    """
    return template.get(data_type.lower(), 'Edm.String')
