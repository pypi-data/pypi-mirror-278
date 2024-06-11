import pandas as pd
from pandas import DataFrame
from pandas.core.dtypes.common import (
    is_bool_dtype,
    is_datetime64_any_dtype,
    is_float_dtype,
    is_integer_dtype,
    is_string_dtype,
)


class SQLUtils:
    def __init__(self, dataframe: DataFrame, table_name: str) -> None:
        self.dataframe: DataFrame = dataframe
        self.table_name: str = table_name

    def generate_create_table_sql(self) -> str:
        """Generate a CREATE TABLE SQL statement based on the DataFrame schema."""
        columns: list[str] = []
        for col_name, dtype in self.dataframe.dtypes.iteritems():
            if is_integer_dtype(dtype):
                column_sql: str = f"{col_name} INTEGER"
            elif is_float_dtype(dtype):
                column_sql: str = f"{col_name} REAL"
            elif is_bool_dtype(dtype):
                column_sql: str = f"{col_name} BOOLEAN"
            elif is_datetime64_any_dtype(dtype):
                column_sql: str = f"{col_name} TIMESTAMP"
            elif is_string_dtype(dtype):
                column_sql: str = f"{col_name} TEXT"
            else:
                column_sql: str = (
                    f"{col_name} TEXT"  # Default to TEXT if type is unknown
                )
            columns.append(column_sql)
        columns_sql: str = ",\n  ".join(columns)
        return f"CREATE TABLE {self.table_name} (\n  {columns_sql}\n);"

    def generate_insert_sql(self) -> str:
        """Generate INSERT INTO SQL statements for each row in the DataFrame."""
        insert_sql: str = f"INSERT INTO {self.table_name} ({', '.join(self.dataframe.columns)}) VALUES "
        rows: list[str] = []
        for _, row in self.dataframe.iterrows():
            values: list[str] = []
            for item in row:
                if pd.isna(item):
                    value = "NULL"
                elif isinstance(item, str):
                    escaped_item = item.replace("'", "''")
                    value = f"'{escaped_item}'"
                elif isinstance(item, bool):
                    value = str(item).upper()
                elif isinstance(item, (int, float)):
                    value = str(item)
                elif pd.api.types.is_datetime64_any_dtype(item):
                    value = f"'{item.isoformat()}'"
                else:
                    value = f"'{str(item)}'"
                values.append(value)
            row_sql: str = f"({', '.join(values)})"
            rows.append(row_sql)
        all_rows_sql: str = ",\n".join(rows)
        return f"{insert_sql}\n{all_rows_sql};"

    def generate_replace_sql(self) -> dict[str, str]:
        """Generate a CREATE OR REPLACE TABLE SQL statement and INSERT INTO SQL statements."""
        drop_table_sql: str = f"DROP TABLE IF EXISTS {self.table_name};"
        create_table_sql: str = self.generate_create_table_sql()
        insert_sql: str = self.generate_insert_sql()
        return {
            "drop_table_sql": drop_table_sql,
            "create_table_sql": create_table_sql,
            "insert_sql": insert_sql,
        }
