import os
from typing import Generator
import pyodbc

# Configure connection via environment variable `MSSQL_CONN` or default to a trusted local server.
# Example env value:
# DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-8UQUVJ2;DATABASE=sql_app;Trusted_Connection=yes;TrustServerCertificate=Yes;

CONN_STR = os.getenv(
    "MSSQL_CONN",
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-8UQUVJ2;DATABASE=sql_app;Trusted_Connection=yes;TrustServerCertificate=Yes;",
)

def get_db() -> Generator[pyodbc.Connection, None, None]:
    """FastAPI dependency that yields a pyodbc connection.

    The connection is opened for each request and closed after the request finishes.
    Configure the connection string with the `MSSQL_CONN` environment variable when deploying.
    """
    conn = pyodbc.connect(CONN_STR)
    try:
        yield conn
    finally:
        try:
            conn.close()
        except Exception:
            pass
