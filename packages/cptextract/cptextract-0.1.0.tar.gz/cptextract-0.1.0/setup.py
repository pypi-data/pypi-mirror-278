from setuptools import setup, find_packages

setup(
    name= 'cptextract',
    version= '0.1.0',
    packages= find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "python-ags4",
        "openpyxl",
        "xlrd",
        "pyexcel",
    ]
)