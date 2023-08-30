import unittest
from EdmModelBuilder.EdmModel import ODataEdmBuilder


class TestODataEdmBuilder(unittest.TestCase):
    def setUp(self):
        # Create an instance of ODataEdmBuilder for testing
        self.builder = ODataEdmBuilder("TestNamespace", "TestService")

    def tearDown(self):
        # Clean up resources after each test (if needed)
        pass

    def test_add_schema(self):
        schema = self.builder.add_schema("Schema1")
        self.assertEqual(schema["Namespace"], "Schema1")

    def test_get_schema_by_name(self):
        schema = self.builder.add_schema("Schema1")
        found_schema = self.builder.get_schema_by_name("Schema1")
        self.assertEqual(schema, found_schema)

    def test_add_entity_container(self):
        schema = self.builder.add_schema("Schema1")
        container = self.builder.add_entity_container(schema, "Container1")
        self.assertEqual(container["Name"], "Container1")

    def test_add_entity_set(self):
        schema = self.builder.add_schema("Schema1")
        container = self.builder.add_entity_container(schema, "Container1")
        entity_set = self.builder.add_entity_set(container, "EntitySet1", "EntityType1")
        self.assertEqual(entity_set["Name"], "EntitySet1")
        self.assertEqual(entity_set["EntityType"], "EntityType1")

    def test_get_entity_type_by_name(self):
        schema = self.builder.add_schema("Schema1")
        entity_type = self.builder.add_entity_type(schema, "EntityType1")
        found_entity_type = self.builder.get_entity_type_by_name(schema, "EntityType1")
        self.assertEqual(entity_type, found_entity_type)

    def test_add_entity_type(self):
        schema = self.builder.add_schema("Schema1")
        entity_type = self.builder.add_entity_type(schema, "EntityType1")
        self.assertEqual(entity_type["Name"], "EntityType1")

    def test_add_key(self):
        schema = self.builder.add_schema("Schema1")
        entity_type = self.builder.add_entity_type(schema, "EntityType1")
        self.builder.add_key(entity_type, "KeyProperty", "Edm.String")
        self.assertEqual(entity_type["Keys"], ["KeyProperty"])

    def test_add_property(self):
        schema = self.builder.add_schema("Schema1")
        entity_type = self.builder.add_entity_type(schema, "EntityType1")
        prop = self.builder.add_property(entity_type, "PropertyName", "Edm.String")
        self.assertEqual(prop["Name"], "PropertyName")
        self.assertEqual(prop["Type"], "Edm.String")
        self.assertTrue(prop["Nullable"])

    def test_generate_metadata(self):
        schema = self.builder.add_schema("Schema1")
        entity_type = self.builder.add_entity_type(schema, "EntityType1")
        self.builder.add_property(entity_type, "PropertyName", "Edm.String")
        metadata = self.builder.generate_metadata()
        self.assertIn('<Schema Namespace="Schema1"', metadata)
        self.assertIn('<EntityType Name="EntityType1"', metadata)
        self.assertIn('<Property Name="PropertyName" Type="Edm.String" Nullable="true" />', metadata)

    def test_validate_entity_type(self):
        schema = self.builder.add_schema("Schema1")
        entity_type = self.builder.add_entity_type(schema, "EntityType1")
        # breaks rule #1 If no base type is specified, the edm:EntityType element MUST contain one or more properties
        self.assertRaises(ValueError, self.builder.validate_entity_type, entity_type)
        # does not raise any error / passing case
        self.builder.add_property(entity_type, "PropertyName", "Edm.String")
        self.builder.validate_entity_type(entity_type)
        # breaks rule that you cant add a base_type and a key to same entity
        entity_type2 = self.builder.add_entity_type(schema, "EntityType2", base_type="EntityType1")
        self.assertRaises(ValueError, self.builder.add_key, entity_type2, "PropertyName1", "Edm.String")
        # breaks rule that you can add base_type of itself
        self.assertRaises(KeyError, self.builder.add_entity_type, schema, "EntityType4", base_type="EntityType4")


if __name__ == "__main__":
    unittest.main()
