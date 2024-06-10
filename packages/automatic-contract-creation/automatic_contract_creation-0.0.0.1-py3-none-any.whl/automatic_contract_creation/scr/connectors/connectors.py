import abc
from typing import Optional

class Connector(abc.ABC):
    def __init__(self, connection_name: str, **creds):
        self.connection_name = connection_name
        self.creds = creds if creds else None
        self.connection = None
        self.query = None

    def call_origin_dtypes(func):
        def wrapper(self, query, parameters=None):
            self.query = query
            self.get_origin_dtypes()
            return func(self, query, parameters)

        return wrapper



    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    @call_origin_dtypes
    def read_data(self, query: str, parameters: Optional[dict] = None):
        pass


    @abc.abstractmethod
    def get_origin_dtypes(self):
        pass






