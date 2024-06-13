'''Database interaction'''

import psycopg2 as _psycopg2
from psycopg2 import sql

class PostgreSQL:
    '''Connection with a PostgreSQL database'''
    def __init__(self, database: str, host: str, user: str, password: str) -> None:        
        self._connection = _psycopg2.connect(database=database,
                                host=host,
                                user=user,
                                password=password)

        self._cursor = self._connection.cursor()

    def get_query_string(self, query: sql.SQL):
        return query.as_string(self._connection)
    
    def execute(self, query: sql.SQL, data: dict[str, any] = None):
        return self._cursor.execute(query, data)
    
    def commit(self):
        self._connection.commit()

    def insert(self, schema: str, table: str, data: dict[str, any], commit: bool = True, return_fields: list[str] = []):
        '''
        Inserts a row into a specified table within a PostgreSQL database.

        :param schema: The schema name where the table resides.
        :param table: The name of the table to insert data into.
        :param data: A dictionary where keys are column names and values are the data to insert.
        :param commit: Whether to commit the transaction after the insert. Defaults to True.
        :param return_fields: A list of fields to return after the insert. Defaults to an empty list.

        :returns: If `return_fields` is specified, returns a tuple containing the values of the requested fields. 
                    Otherwise, returns None.

        :notes: 
            - The `data` dictionary keys must match the column names of the table.
            - If `commit` is False, the changes must be committed manually using the connection's `commit` method.
        '''
        
        if len(return_fields) > 0:
            base_query = 'INSERT INTO {schema}.{table}({fields}) VALUES({values}) RETURNING {return_fields}'
        else:
            base_query = 'INSERT INTO {schema}.{table}({fields}) VALUES({values})'

        query = sql.SQL(base_query).format(
            schema=sql.Identifier(schema),
            table=sql.Identifier(table),
            fields=sql.SQL(',').join([sql.Identifier(key) for key in data.keys()]),
            values=sql.SQL(',').join([sql.Placeholder(key) for key in data.keys()]),
            return_fields=sql.SQL(',').join([sql.Identifier(key) for key in return_fields])
        )

        self.execute(query, data)

        return_value = None
        if len(return_fields) > 0:
            return_value = self._cursor.fetchone()

        if commit:
            self.commit()

        return return_value
