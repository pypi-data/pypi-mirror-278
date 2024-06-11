from automatic_contract_creation.scr.connectors.connectors import Connector
from automatic_contract_creation.scr.connectors.click_connect import ClickhouseConnector
from automatic_contract_creation.scr.connectors.trino_connector import TrinoConnector


class ConnectionManager:
    connection_classes = {'clickhouse': ClickhouseConnector, 'trino': TrinoConnector}

    def __init__(self, connection_name: str, **creds):
        self.connector = self.get_connector(connection_name, **creds)
        self._delegate_methods()

    def get_connector(self, connection_name: str, **creds) -> Connector:
        connector_class = self.connection_classes.get(connection_name)

        if not connector_class:
            raise Exception('Unknown connection type')
        connector = connector_class(connection_name, **creds)
        connector.connect()
        return connector

    def _delegate_methods(self):
        for method_name in dir(self.connector):
            if not method_name.startswith('_') and callable(getattr(self.connector, method_name)):
                setattr(self, method_name, getattr(self.connector, method_name))


