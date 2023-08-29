from setuptools import setup, find_packages

setup(
    name='PyOdataEdmModel',
    version='1.0.0',
    author='Wessel Reijngoud',
    author_email='wreijngoud@ilionx.com',
    keywords='odata edmmodel metadata',
    description='The ODataEdmBuilder is a Python class that facilitates the construction of an Entity Data Model (EDM) for OData services.',
    packages=find_packages(),
    install_requires=['pandas==2.0.3'],
)