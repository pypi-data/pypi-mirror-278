import contextlib
import os

import pyodbc
import pytest
from dotenv import load_dotenv

from label_tree.diseases_tree import DiseaseTree

load_dotenv(override=True)

# Use environment variables or secure storage for credentials
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DRIVER = "{ODBC Driver 18 for SQL Server}"
ENDPOINT = "127.0.0.1,1433"

# Connect to the MS SQL database using pyodbc
conn_string = (
    f"DRIVER={DRIVER}"  # This driver has to be installed separately!!
    f";SERVER={ENDPOINT};"
    f"UID={DB_USER};"
    f"PWD={DB_PASSWORD};"
    f"DATABASE={DB_NAME};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes"
)


@pytest.fixture
def get_label_list():
    # Establish a connection using a context manager
    with pyodbc.connect(conn_string) as conn:
        # Create a cursor using a context manager
        with conn.cursor() as cursor:
            sql_query = "SELECT name FROM Diagnosis_Options"

            # Execute the query
            try:
                cursor.execute(sql_query)
            except pyodbc.Error as error:
                print(f"Error executing query: {error}")
                exit(1)
            rows = cursor.fetchall()

    return list(rows)


def test_db_labels(get_label_list, label_version):
    query_result = get_label_list
    labels = [e[0] for e in query_result]

    with open(os.devnull, "w") as null_file, contextlib.redirect_stdout(null_file):
        tree = DiseaseTree(skip_comments=False, label_version=label_version)

    for label in labels:
        tree.get_canonial_form(label)
