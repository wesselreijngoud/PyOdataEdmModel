from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="PyOdataEdmModel",
    version="1.0.4",
    author="Wessel Reijngoud",
    author_email="wreijngoud@ilionx.com",
    keywords="odata edmmodel metadata",
    description="The ODataEdmBuilder is a Python class that facilitates the construction of an Entity Data Model (EDM) for OData services.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    data_files=[
        (
            "config",
            [
                "PyOdataEdmModel/config/template.json",
                "PyOdataEdmModel/config/settings.json",
            ],
        )
    ],
    include_package_data=True,
    install_requires=["pandas==2.1.1"],
    project_urls={"Source": "https://github.com/wesselreijngoud/PyOdataEdmModel"},
)
