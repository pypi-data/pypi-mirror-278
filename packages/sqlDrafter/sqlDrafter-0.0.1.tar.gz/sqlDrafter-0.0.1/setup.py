import os
from setuptools import find_packages, setup

extras = {
    "postgres": ["psycopg2-binary"],
    "mysql": ["mysql-connector-python"],
    "snowflake": ["snowflake-connector-python"],
    "bigquery": ["google-cloud-bigquery"],
    "redshift": ["psycopg2-binary"],
    "databricks": ["databricks-sql-connector"],
}


def package_files(directory):
    paths = []
    for path, directories, filenames in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    return paths




setup(
    name="sqlDrafter",
    packages=find_packages(),
    version="0.0.1",
    description="sqldrafter is a Python library that helps you generate data queries from natural language questions.",
    author="yanQiao",
    license="Apache License,Version 2.0",
    install_requires=[
        "requests>=2.28.2",
        "psycopg2-binary>=2.9.5",
        "prompt-toolkit>=3.0.38",
        "fastapi",
        "uvicorn",
        "tqdm",
        "pwinput",
    ],

    author_email="xiaoyan@sqldrafter.com",
    url="https://www.sqldrafter.com",
    long_description="sqldrafter is a Python library that helps you generate data queries from natural language questions.",
    long_description_content_type="text/markdown",
    extras_require=extras,
)
