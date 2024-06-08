from __future__ import annotations  # Required for type hinting in class methods

from typing import Optional

import mysql.connector
from logger_local.LoggerLocal import Logger
from logger_local.MetaLogger import MetaLogger
from .utils import get_sql_hostname, get_sql_password, get_sql_username, get_sql_port

from .constants import LOGGER_CONNECTOR_CODE_OBJECT
from .cursor import Cursor

logger = Logger.create_logger(object=LOGGER_CONNECTOR_CODE_OBJECT)
connections_pool = {}


# TODO Can we add hostname, IPv4, IPv6, sql statement? Can we have the same message format in all cases?
class Connector(metaclass=MetaLogger, object=LOGGER_CONNECTOR_CODE_OBJECT):
    @staticmethod
    def connect(schema_name: str) -> Connector:
        if (schema_name in connections_pool and
                connections_pool[schema_name] and
                connections_pool[schema_name].connection):
            if connections_pool[schema_name].connection.is_connected():

                return connections_pool[schema_name]
            else:
                # reconnect
                connections_pool[schema_name].connection.reconnect()
                # TODO We should develop retry mechanism to support password rotation and small network issues.
                if connections_pool[schema_name].connection.is_connected():

                    return connections_pool[schema_name]
                else:
                    connector = Connector(schema_name)
                    logger.warning("Reconnect failed, returning a new connection",
                                   object={'connections_pool': str(connections_pool[schema_name])})

                    return connector
        else:
            connector = Connector(schema_name)

            return connector

    def __init__(self, schema_name: str,
                 host: str = get_sql_hostname(),
                 user: str = get_sql_username(),
                 password: str = get_sql_password(),
                 port: str = get_sql_port()) -> None:
        self.host = host
        self.schema = schema_name
        self.user = user
        self.password = password
        self.port = port

        # Checking host suffix
        # TODO: move to sdk.get_sql_hostname
        if not (self.host.endswith("circ.zone") or self.host.endswith("circlez.ai")):
            logger.warning(
                f"Your RDS_HOSTNAME={self.host} which is not what is expected")
        self.connection: mysql.connector = None
        self._cursor: Optional[Cursor] = None
        self._connect_to_db()
        connections_pool[schema_name] = self

    def reconnect(self) -> None:
        self.connection.reconnect()
        # TODO Is it good for performance?
        self._cursor = self.cursor(close_previous=True)
        self.set_schema(self.schema)

    def _connect_to_db(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.schema,
            port=self.port
            # TODO port= to suport SSH Tunneling https://stackoverflow.com/questions/21903411/enable-python-to-connect-to-mysql-via-ssh-tunnelling
        )
        self._cursor = self.cursor()
        self.set_schema(self.schema)

    def database_info(self):
        return f"host={self.host}, user={self.user}, schema={self.schema}"

    def close(self) -> None:
        try:
            if self._cursor:
                self._cursor.close()
                logger.info(f"Cursor closed successfully for schema: {self.schema}")
        except Exception as exception:
            logger.error(f"connection.py close() {self.database_info()}", object={"exception": exception})
        connections_pool.pop(self.schema, None)
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Connection closed successfully.")

    def cursor(self, *, close_previous: bool = True, cache_previous: bool = False, dictionary: bool = None,
               buffered: bool = None, raw: bool = None,
               prepared: bool = None, named_tuple: bool = None, cursor_class=None) -> Cursor:
        # if cache_previous and self._cursor:
        #     cursor_instance = self._cursor
        #     return cursor_instance
        # if close_previous and self._cursor:
        #     self._cursor.close()

        cursor_instance = Cursor(self.connection.cursor(
            dictionary=dictionary, buffered=buffered, raw=raw, prepared=prepared,
            named_tuple=named_tuple, cursor_class=cursor_class))

        # self._cursor = cursor_instance
        return cursor_instance

    def commit(self) -> None:
        self.connection.commit()

    def set_schema(self, new_schema: Optional[str]) -> None:
        if not new_schema:
            return
        if self.schema == new_schema:
            return

        if self._cursor and self.connection and self.connection.is_connected():
            use_query = f"USE `{new_schema}`;"
            self._cursor.execute(use_query)
            connections_pool[new_schema] = self
            connections_pool.pop(self.schema, None)
            self.schema = new_schema
            logger.info(f"Switched to schema: {new_schema}")
        else:
            raise Exception(
                "Connection is not established. The database will be used on the next connect.")

    def rollback(self):
        self.connection.rollback()

    def start_transaction(self):
        self.connection.start_transaction()
