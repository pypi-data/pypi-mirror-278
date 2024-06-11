def show_docs():
    """Prints out all methods and classes in rgwml package with their signatures."""
    items = [
        "get_preset(example)",
        "execute_query(example)",
        "mssql_to_df(example)",
        "bigquery_to_df(example)",
        "__init__(example)",
        "connect(example)",
        "class DBPreset",
        "class Config",
        "class DatabaseManager",
        "class DataManager",
        "class BigQueryManager",
    ]
    for item in items:
        print(item)
