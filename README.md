# ODataEdmBuilder - Readme

The `ODataEdmBuilder` is a Python class that facilitates the construction of Entity Data Model (EDM) metadata for OData services. OData is an open standard protocol that enables the creation and consumption of RESTful APIs for data access and manipulation.
OData is a widely-used protocol for building and consuming RESTful APIs. To expose data through OData, you need to define an Entity Data Model (EDM), which describes the data entities, their properties, and the relationships between them. Manually creating EDM metadata can be complex and error-prone. The OData EDM Builder simplifies this process, allowing you to generate EDM metadata with ease.

## Table of Contents

1. [Overview](#overview)
2. [Dependencies](#dependencies)
3. [Usage](#usage)
4. [Class Methods](#class-methods)
5. [Example](#example)

## 1. Overview <a name="overview"></a>

The `ODataEdmBuilder` class simplifies the creation of metadata for OData services by providing methods to define schemas, entity types, entity containers, properties, and keys. The resulting metadata is represented in EDMX format, which is an XML-based representation of the OData service metadata.

The class includes the following main features:
- Defining namespaces and service names for the OData service.
- Adding schemas with optional aliases.
- Creating entity types with properties, including support for inheritance.
- Defining keys for entity types.
- Constructing entity containers with entity sets.
- Generating EDMX metadata document.

## 1.1. Getting Started
Odata data type mapping is different depending on the source, in the config/template.json file you can find the already defined Odata data type mappings available. In the config/settings.json you can change the source of your data to correctly get the mapping from the template file. If your data source is not yet present in the template file, add it manually as a dict in a dict. 

## Code Formatting

This project follows the "black" code formatting style. "black" is an opinionated code formatter that automatically formats Python code to ensure consistent style and readability. To learn more about "black," visit the [official repository](https://github.com/psf/black).

## 2. Dependencies <a name="dependencies"></a>
To install the needed dependencies please run:
```pip install -r requirements.txt```


## 3. Usage <a name="usage"></a>

To use the `ODataEdmBuilder` class, follow these steps:

1. Create an instance of the `ODataEdmBuilder` by providing the `namespace` and `service_name` parameters.

2. Use the provided methods to define schemas, entity types, keys, properties, and entity containers.

3. Call the `generate_metadata()` method to generate the EDMX metadata document as a string.

4. Optionally, you can call the `clear()` method to reset the `ODataEdmBuilder` object 

## 4. Class Methods <a name="class-methods"></a>

The `ODataEdmBuilder` class includes the following methods:

### 4.1 Constructor

```python
def __init__(self, namespace: str, service_name: str)
```

The constructor initializes the `ODataEdmBuilder` object with the specified `namespace` and `service_name`.

### 4.2 Schema Methods

```python
def add_schema(self, schema_name: str, alias: str = "") -> dict
```

Adds a schema with the given `schema_name` to the `ODataEdmBuilder` object. Optionally, you can provide an `alias` for the schema.

```python
def get_schema_by_name(self, schema_name: str)
```

Retrieves a schema dictionary by its `schema_name` or `alias`.

### 4.3 Entity Container Methods

```python
def add_entity_container(self, schema: dict | str, container_name: str) -> dict
```

Adds an entity container with the given `container_name` to the `ODataEdmBuilder` object under the specified `schema`.

### 4.4 Entity Set Methods

```python
def add_entity_set(self, entity_container: dict, entity_set_name: str, entity_type_name: str) -> dict
```

Adds an entity set with the given `entity_set_name` and `entity_type_name` to the specified `entity_container` in the `ODataEdmBuilder` object.

### 4.5 Entity Type Methods

```python
def add_entity_type(self, schema: dict | str, entity_type_name: str, base_type: str = "", summary: str = "", long_description: str = "") -> dict
```

Adds an entity type with the given `entity_type_name` and optional `base_type` to the specified `schema` in the `ODataEdmBuilder` object. Optionally, you can include a `summary` and `long_description` for documentation purposes.

```python
def add_key(self, entity_type: dict, property_name: str, property_type: str)
```

Adds keys with a property name to the specified `entity_type` as PropertyRef.

```python
def add_property(self, entity_type: dict, property_name: str, property_type: str, nullable: bool = True) -> dict
```

Adds properties with a `property_name`, `property_type`, and `nullable` setting to the specified `entity_type` in the `ODataEdmBuilder` object.

### 4.6 Metadata Generation

```python
def generate_metadata(self) -> str
```

Generates the EDMX metadata document based on the configurations set in the `ODataEdmBuilder` object and returns it as a string.

## 5. Example <a name="example"></a>

Here is an example of how to use the `ODataEdmBuilder` class to create EDMX metadata:

```python
# Create an instance of ODataEdmBuilder
odata_builder = ODataEdmBuilder(namespace="MyNamespace", service_name="MyODataService")

# Add a schema with alias
schema = odata_builder.add_schema(schema_name="MySchema", alias="ms")

# Add an entity type with properties and keys
person_type = odata_builder.add_entity_type(
    schema=schema,
    entity_type_name="Person",
    summary="Represents a person entity.",
    long_description="This entity represents information about a person.",
)
odata_builder.add_property(person_type, "Id", "Edm.Int32")
odata_builder.add_key(person_type, "Id", "Edm.Int32")
odata_builder.add_property(person_type, "Name", "Edm.String")
odata_builder.add_property(person_type, "Age", "Edm.Int32")

# Add an entity container and entity set
container = odata_builder.add_entity_container(schema=schema, container_name="MyContainer")
odata_builder.add_entity_set(container, entity_set_name="People", entity_type_name="MySchema.Person")

# Generate and print the EDMX metadata document
metadata = odata_builder.generate_metadata()
print(metadata)
```

## License
This project is licensed under the GNU 3 License. See the LICENSE file for details.
