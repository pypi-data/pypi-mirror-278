import json
import os
import pandas as pd
import mysql.connector
from clickhouse_driver import Client
from google.cloud import bigquery
from sqlalchemy import create_engine

# Load configuration
config_path = os.path.expanduser("~/Desktop/rgwml.config")
with open(config_path, "r") as file:
    config = json.load(file)

# Example usage
def query_to_df(preset_name, query_str):

    # Get MSSQL connection URL from config
    def get_mssql_connection_url(preset):
        driver = preset.get("driver", "ODBC Driver 17 for SQL Server")
        server = preset["host"]
        port = 1433
        database = preset["database"]
        username = preset["username"]
        password = preset["password"]

        # Constructing the DB URL
        db_url = f"mssql+pyodbc://{username}:{password}@{server}:{port}/{database}?driver={{{driver}}}&TrustServerCertificate=yes"

        return db_url

    # Functions to handle each database type
    def get_mssql_connection(preset):
        engine = create_engine(get_mssql_connection_url(preset))
        conn = engine.connect()
        return conn

    def get_mysql_connection(preset):
        return mysql.connector.connect(
            host=preset["host"],
            user=preset["username"],
            password=preset["password"],
            database=preset["database"]
        )

    def get_clickhouse_connection(preset):
        return Client(
            host=preset["host"],
            user=preset["username"],
            password=preset["password"],
            database=preset["database"]
        )

    def get_bigquery_client(preset):
        return bigquery.Client.from_service_account_json(preset["json_file_path"])

    # Function to execute query and return DataFrame
    def execute_query(preset_name, query):
        preset = next((p for p in config["db_presets"] if p["name"] == preset_name), None)
        if not preset:
            raise ValueError(f"No preset found with name {preset_name}")

        if preset["db_type"] == "mssql":
            conn = get_mssql_connection(preset)
            df = pd.read_sql(query, conn)
            conn.close()
        elif preset["db_type"] == "mysql":
            conn = get_mysql_connection(preset)
            df = pd.read_sql(query, conn)
            conn.close()
        elif preset["db_type"] == "clickhouse":
            client = get_clickhouse_connection(preset)
            df = pd.DataFrame(client.execute(query))
        elif preset["db_type"] == "bigquery":
            client = get_bigquery_client(preset)
            query_job = client.query(query)
            df = query_job.to_dataframe()
        else:
            raise ValueError(f"Unsupported database type: {preset['db_type']}")

        return df

    return execute_query(preset_name, query_str)

