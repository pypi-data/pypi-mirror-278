from typing import Optional
import polars as pl
from  automatic_contract_creation.scr.connectors.connectors import Connector
import clickhouse_connect
import pandas as pd
import re
import os


class ClickhouseConnector(Connector):
    def connect(self):
        self.connection  = clickhouse_connect.get_client(
                                        host=self.creds['host'],
                                        port=self.creds['port'],
                                        user=self.creds['user'],
                                        password=self.creds['password'],

                                    )

        print('Sucsesfully connected to Clickhouse')

    @Connector.call_origin_dtypes
    def read_data(self, query: str, parameters: Optional[dict] = None):
        lazyframe = pl.LazyFrame(self.connection.query_df(query, parameters=parameters))
        return lazyframe


    def get_origin_dtypes(self):
        with open('./click_dtypes.sql', 'r') as file:
            query_dtypes = file.read()

        table_name = re.search(r'from\s+(?:[\w\-\."])+\.(\w+)\b', self.query).group(1)
        query_dtypes = query_dtypes.format(schema=self.creds['db_name'], tablename=table_name)
        df_dtypes = pd.DataFrame(self.connection.query_df(query_dtypes))

        self.origin_dtypes = df_dtypes







