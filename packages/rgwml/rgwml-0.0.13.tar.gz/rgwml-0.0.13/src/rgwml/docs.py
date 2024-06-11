def show_docs():
    """Prints out all classes and their methods in rgwml package."""
    classes = {
        "DBPreset": [__init__(self, name, db_type, host, username, password, database)],
        "Config": [__init__(self, config_path), get_preset(self, name)],
        "DatabaseManager": [__init__(self, preset), connect(self), execute_query(self, query)],
        "DataManager": [__init__(self, config), mssql_to_df(self, preset_name, query_str), bigquery_to_df(self, preset_name, query_str)],
        "BigQueryManager": [__init__(self, preset), execute_query(self, query, project_id)],
    }
    for class_name, methods in classes.items():
        print(f"Class {class_name}:")
        for method in methods:
            print(f"  {method}")
