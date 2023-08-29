# This file adheres to the "black" code formatting style.
# More information about black: https://github.com/psf/black
from EdmModel.primitives import primitives


class ODataEdmBuilder:
    def __init__(self, namespace: str, service_name: str):
        """
        Initialize an ODataEdmBuilder instance to create an EDM (Entity Data Model) metadata.

        Args:
            namespace (str): The namespace for the EDM model.
            service_name (str): The name of the service associated with the EDM model.
        """
        self.namespace = namespace
        self.service_name = service_name
        self.schemas = []
        self.metadata = ""

    def clear(self):
        """
        Clears the ODataEdmMetadataBuilder object of all information
        """
        self.namespace = ""
        self.service_name = ""
        self.schemas = []
        self.metadata = ""

    def add_schema(
        self,
        schema_name: str,
        alias: str = "",
    ) -> dict:
        """
        Add a schema with the specified name to the ODataEdmBuilder object.

        Args:
            schema_name (str): The name of the schema.
            alias (str, optional): An alias for the given schema.

        Returns:
            dict: The dictionary representing the added schema.
        """
        schema = {"Namespace": schema_name, "EntityTypes": [], "EntityContainers": []}
        if alias:
            schema["Alias"] = alias
        self.schemas.append(schema)
        return schema

    def get_schema_by_name(self, schema_name: str) -> dict:
        """
        Returns a schema dict by name or alias (str)

        Args:
            schema_name (str): Name or Alias of schema to find

        Raises:
            ValueError: If Name or Alias does not exist as schema in model

        Returns:
            schema: schema dictionary by Name or Alias
        """
        for schema in self.schemas:
            if schema["Namespace"] == schema_name:
                return schema
            elif "Alias" in schema.keys():
                if schema["Alias"] == schema_name:
                    return schema
            else:
                raise ValueError(
                    f"Schema with Name or Alias {schema_name} does not exist"
                )

    def add_entity_container(self, schema: dict | str, container_name: str) -> dict:
        """
        Add an entity container to the ODataEdmBuilder object within the specified schema.

        Args:
            schema (dict | str): The schema dictionary or its name.
            container_name (str): The name of the entity container.

        Returns:
            dict: The dictionary representing the added entity container.
        """
        entity_container = {"Name": container_name, "EntitySets": []}
        if isinstance(schema, str):
            schema = self.get_schema_by_name(schema)

        schema["EntityContainers"].append(entity_container)
        return entity_container

    def add_entity_set(
        self, entity_container: dict, entity_set_name: str, entity_type_name: str
    ) -> dict:
        """
        Add an entity set with a specified name and associated entity type to an entity container.

        Args:
            entity_container (dict): The entity container to which the entity set will be added.
            entity_set_name (str): The name of the entity set.
            entity_type_name (str): The name of the associated entity type.

        Returns:
            dict: The dictionary representing the added entity set.
        """
        entity_set = {"Name": entity_set_name, "EntityType": entity_type_name}
        entity_container["EntitySets"].append(entity_set)
        return entity_set

    def get_entity_type_by_name(
        self, schema: dict | str, entity_type_name: str
    ) -> dict:
        """
        Retrieve the entity type dictionary with the specified name from the given schema.

        Args:
            schema (dict | str): The schema dictionary or its name.
            entity_type_name (str): The name of the entity type to find.

        Returns:
            dict: The entity type dictionary.

        Raises:
            KeyError: If the entity type with the specified name is not found.
        """
        if isinstance(schema, str):
            schema = self.get_schema_by_name(schema)

        for entity_type in schema["EntityTypes"]:
            if entity_type["Name"] == entity_type_name:
                return entity_type

        raise KeyError(
            f"""Entity type '{entity_type_name}' not found in the given schema.
            Note: An entity type cannot introduce an inheritance cycle via the base type attribute."""
        )

    def add_entity_type(
        self,
        schema: dict | str,
        entity_type_name: str,
        base_type: str | dict = "",
        summary: str = "",
        long_description: str = "",
    ) -> dict:
        """
        Add an entity type with a specified name and base type to a schema.

        Args:
            schema (dict): The schema to which the entity type will be added.
            entity_type_name (str): The name of the entity type.
            base_type (str|dict, optional): The base type from which the entity type inherits (if any).
            summary (str, optional): A summary for the entity type.
            long_description (str, optional): A long description for the entity type.

        Returns:
            dict: The dictionary representing the added entity type.
        """
        entity_type = {
            "Name": entity_type_name,
            "Properties": [],
            "NavigationProperties": [],
        }
        if isinstance(schema, str):
            schema = self.get_schema_by_name(schema)

        if base_type:
            # Rule: An entity type MUST contain exactly one Key element or specify a value for
            # the BaseType attribute, but not both.
            if "Keys" in entity_type:
                raise ValueError(
                    "An entity type with a base type must not declare a key."
                )
            entity_type["BaseType"] = (
                base_type["Name"]
                if isinstance(base_type, dict)
                else self.get_entity_type_by_name(schema, base_type)["Name"]
            )
        else:
            entity_type["Keys"] = []

        # Documentation tag with Summary and LongDescription if added.
        documentation = {}
        if summary:
            documentation["Summary"] = summary
        if long_description:
            documentation["LongDescription"] = long_description
        entity_type["Documentation"] = documentation

        schema["EntityTypes"].append(entity_type)
        return entity_type

    def add_key(self, entity_type: dict, property_name: str, property_type: str):
        """
        Add keys with a specified property name to entity types as PropertyRef in an ODataEdmBuilder.

        Args:
            entity_type (dict): The entity type to which the key will be added.
            property_name (str): The name of the property to be added.
            property_type (str): The type of the property to be added.

        Raises:
            ValueError: If the entity type has a base type, it must not declare a key.
            ValueError: If the property type is not of valid primitive type for a PropertyRef Key.
        """
        if "BaseType" in entity_type:
            raise ValueError("An entity type with a base type must not declare a key.")

        # PropertyRef keys can only be of primitive types
        if property_type in primitives:
            entity_type["Keys"].append(property_name)
        else:
            raise ValueError(
                f"{property_type} not a valid property type as a PropertyRef Key, because it is not a primitive type."
            )

    def add_property(
        self,
        entity_type: dict,
        property_name: str,
        property_type: str,
        nullable: bool = True,
    ) -> dict:
        """
        Add a property with a specified name, type, and nullable setting to an entity type.

        Args:
            entity_type (dict): The entity type to which the property will be added.
            property_name (str): The name of the property.
            property_type (str): The type of the property.
            nullable (bool): Whether the property is nullable (defaults to True).

        Returns:
        dict: The dictionary representing the added property
        """
        prop = {"Name": property_name, "Type": property_type, "Nullable": nullable}
        # because Key is added as a property as well, check if property_name is not already in existing properties
        existing_property_names = [prop["Name"] for prop in entity_type["Properties"]]
        existing_navigation_property_names = [
            prop["Name"] for prop in entity_type["NavigationProperties"]
        ]
        if (
            property_name not in existing_property_names
            and property_name not in existing_navigation_property_names
        ):
            entity_type["Properties"].append(prop)
        return prop

    def generate_metadata(self) -> str:
        """
        Generates edmx metadata document on the ODataEdmBuilder object

        Returns:
            str: Odata metadata document
        """
        metadata = '<?xml version="1.0" encoding="utf-8"?>\n'
        metadata += '<edmx:Edmx xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx" Version="4.0">\n'
        metadata += "\t<edmx:DataServices>\n"

        for schema in self.schemas:
            if "Alias" in schema.keys():
                metadata += '\t\t<Schema Namespace="{0}" Alias="{1}" xmlns="http://docs.oasis-open.org/odata/ns/edm">\n'.format(
                    schema["Namespace"], schema["Alias"]
                )
            else:
                metadata += '\t\t<Schema Namespace="{0}" xmlns="http://docs.oasis-open.org/odata/ns/edm">\n'.format(
                    schema["Namespace"]
                )

            for entity_type in schema["EntityTypes"]:
                metadata += '\t\t\t<EntityType Name="{0}"'.format(entity_type["Name"])

                if "BaseType" in entity_type:
                    metadata += ' BaseType="Self.{0}">'.format(entity_type["BaseType"])
                else:
                    metadata += ">"

                # Add documentation if available
                if len(entity_type["Documentation"]) > 0:
                    metadata += "\n\t\t\t\t<Documentation>\n"
                    if "Summary" in entity_type["Documentation"]:
                        metadata += "\t\t\t\t\t<Summary>{}</Summary>\n".format(
                            entity_type["Documentation"]["Summary"]
                        )
                    if "LongDescription" in entity_type["Documentation"]:
                        metadata += (
                            "\t\t\t\t\t<LongDescription>{}</LongDescription>\n".format(
                                entity_type["Documentation"]["LongDescription"]
                            )
                        )
                    metadata += "\t\t\t\t</Documentation>\n"

                if "Keys" in entity_type and len(entity_type["Keys"]) > 0:
                    metadata += "\n\t\t\t\t<Key>\n"
                    for key in entity_type["Keys"]:
                        metadata += '\t\t\t\t\t<PropertyRef Name="{0}" />\n'.format(key)
                    metadata += "\t\t\t\t</Key>"
                metadata += "\n"

                for prop in entity_type["Properties"]:
                    metadata += '\t\t\t\t<Property Name="{0}" Type="{1}" Nullable="{2}" />\n'.format(
                        prop["Name"], prop["Type"], str(prop["Nullable"]).lower()
                    )
                if len(entity_type["NavigationProperties"]) > 0:
                    for nav_prop in entity_type["NavigationProperties"]:
                        metadata += '\t\t\t\t<NavigationProperty Name="{0}" Type="{1}" Nullable="{2}" />\n'.format(
                            nav_prop["Name"],
                            schema["Namespace"] + "." + nav_prop["Type"],
                            str(nav_prop["Nullable"]).lower(),
                        )
                metadata += "\t\t\t</EntityType>\n"

            for entity_container in schema["EntityContainers"]:
                metadata += '\t\t\t<EntityContainer Name="{0}">\n'.format(
                    entity_container["Name"]
                )

                for entity_set in entity_container["EntitySets"]:
                    metadata += (
                        '\t\t\t\t<EntitySet Name="{0}" EntityType="{1}" />\n'.format(
                            entity_set["Name"], entity_set["EntityType"]
                        )
                    )

                metadata += "\t\t\t</EntityContainer>\n"

            metadata += "\t\t</Schema>\n"

        metadata += "\t</edmx:DataServices>\n"
        metadata += "</edmx:Edmx>"
        self.metadata = metadata
        return metadata

    def validate_entity_type(self, entity_type: dict):
        """
        This method checks if the entity type adheres to the following rule:

        If no base type is specified, the edm:EntityType element MUST contain one or more
        edm:Property elements describing the properties of the entity type.

        Args:
            entity_type (dict): The entity type dictionary or entity type name to be validated.

        Raises:
            ValueError: If the entity type violates any of the specified rules.
        """
        # Rule 1
        if "BaseType" not in entity_type and len(entity_type["Properties"]) == 0:
            raise ValueError(
                "An entity type with no base type must contain at least one Property element."
            )

    # def add_navigation_property(
    #     self, entity_type: dict, name: str, type_attr: str, is_nullable: bool = True
    # ):
    #     for schema in self.schemas:
    #         try:
    #             type_attr = self.get_entity_type_by_name(schema, type_attr)
    #         except:
    #             continue
    #     if type_attr == entity_type["Name"]:
    #         raise ValueError("A NavigationProperty cannot point to itself.")

    #     navigation_property = {
    #         "Name": name,
    #         "Type": type_attr["Name"],
    #         "Nullable": is_nullable,
    #     }
    #     entity_type["NavigationProperties"].append(navigation_property)

    # if is_collection:
    #     navigation_property["Collection"] = "true"

    # if partner_property_name:
    #     navigation_property["Partner"] = partner_property_name

    # if contains_target:
    #     navigation_property["ContainsTarget"] = "true"

    # entity_type["NavigationProperties"].append(navigation_property)
