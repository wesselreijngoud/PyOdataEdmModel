import unittest
from unittest.mock import mock_open, patch
from PyOdataEdmModel.odata_mapper import OdataConverter


class TestOdataConverter(unittest.TestCase):
    def test_load_json_data_success(self):
        # Test if JSON data is loaded successfully
        with patch(
            "builtins.open", mock_open(read_data='{"sqlserver": {"int": "Edm.Int32"}}')
        ):
            converter = OdataConverter("data.json", "SQLServer")
            self.assertEqual(converter.json_data, {"int": "Edm.Int32"})

    def test_load_json_data_missing_client(self):
        # Test if ValueError is raised when database client is not present in JSON data
        with self.assertRaises(ValueError):
            with patch(
                "builtins.open", mock_open(read_data='{"mysql": {"int": "Edm.Int32"}}')
            ):
                OdataConverter("data.json", "SQLServer")

    def test_convert_to_odata_found(self):
        # Test if convert_to_odata returns correct OData equivalent for a valid data type
        with patch(
            "builtins.open", mock_open(read_data='{"sqlserver": {"int": "Edm.Int32"}}')
        ):
            converter = OdataConverter("data.json", "SQLServer")
            odata_type = converter.convert_to_odata("int")
            # int matches Edm.Int32
            self.assertEqual(odata_type, "Edm.Int32")

    def test_convert_to_odata_not_found(self):
        # Test if convert_to_odata returns "Edm.String" for an invalid data type
        with patch(
            "builtins.open", mock_open(read_data='{"sqlserver": {"int": "Edm.Int32"}}')
        ):
            converter = OdataConverter("data.json", "SQLServer")
            odata_type = converter.convert_to_odata("float")
            # float not in Json so it returns string.
            self.assertEqual(odata_type, "Edm.String")


if __name__ == "__main__":
    unittest.main()
