from automatic_contract_creation.scr.connectors.connectors import Connector
from trino.dbapi import connect
from trino.auth import BasicAuthentication
from typing import Optional
import polars as pl
import pandas as pd
import re
import os

class TrinoConnector(Connector):
    def connect(self, **creds):
        if self.connection:     self.connection.close()
        self.connection = connect(
                                    host=self.creds['host'],
                                    user=self.creds['user'],
                                    port=self.creds['port'],
                                    auth=BasicAuthentication(self.creds['user'], self.creds['password']),
                                    http_scheme='https',
                                    catalog = self.creds['catalog'],
                                    schema = self.creds['schema']
                                    )

        print('Sucsesfully connected to Trino')

    @Connector.call_origin_dtypes
    def read_data(self, query: str, parameters: Optional[list] = None):
        cur = self.connection.cursor()
        cur.execute(query, parameters)

        limit_match = re.search(r'limit\s+(\d+)', query)
        len_lazy = int(limit_match.group(1)) if limit_match else None

        lazyframe = pl.LazyFrame(cur.fetchall(), infer_schema_length=len_lazy)
        col_names = [desc[0] for desc in cur.description]
        lazyframe = lazyframe.select(*[
            pl.col(name).alias(new_name) for name, new_name in zip(lazyframe.columns, col_names)
                                    ])
        cur.close()
        self.connection.close()

        return lazyframe


    def get_origin_dtypes(self):
        CUR_DIR = os.path.abspath(os.path.dirname(__file__))
        with open(f'{CUR_DIR}/trino_dtypes.sql', 'r') as file:
            query_dtypes = file.read()

        table_name = re.search(r'from\s+(?:[\w\-\."])+\.(\w+)\b', self.query).group(1)
        query_dtypes = query_dtypes.format(catalog=self.creds['catalog'],
                                           schema=self.creds['schema'],
                                           tablename=table_name)
        cur = self.connection.cursor()

        cur.execute(query_dtypes)
        df_dtypes = pd.DataFrame(cur.fetchall())
        df_dtypes.columns = [desc[0] for desc in cur.description]

        cur.close()
        self.connection.close()

        self.origin_dtypes =  df_dtypes









