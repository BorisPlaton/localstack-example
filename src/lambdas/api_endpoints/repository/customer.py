from contextlib import contextmanager
from typing import NamedTuple, ContextManager

from psycopg2 import connect
from psycopg2._psycopg import connection, cursor

from settings import DatabaseSettings


class CustomerRecord(NamedTuple):
    id: int
    first_name: str
    last_name: str


class CustomerSQLRepository:

    def __init__(
        self,
        database_settings: DatabaseSettings,
    ) -> None:
        self._database_settings = database_settings

    def save(
        self,
        first_name: str,
        last_name: str,
    ) -> None:
        cur: cursor

        with self._connect() as cur:
            cur.execute(
                "INSERT INTO customer (first_name, last_name) VALUES (%s, %s)",
                (first_name, last_name)
            )

    def get_by_id(
        self,
        id_: int,
    ) -> CustomerRecord | None:
        cur: cursor

        with self._connect() as cur:
            cur.execute(
                "SELECT id, first_name, last_name FROM customer WHERE id = %s;",
                (id_,)
            )
            customer = cur.fetchone()

        return CustomerRecord(*customer) if customer else None

    def get_all(self) -> list[CustomerRecord]:
        cur: cursor

        with self._connect() as cur:
            cur.execute("SELECT id, first_name, last_name FROM customer;")
            customers = cur.fetchall()

        return [CustomerRecord(*customer) for customer in customers]

    @contextmanager
    def _connect(self) -> ContextManager[connection]:
        with connect(
            database=self._database_settings.DATABASE,
            user=self._database_settings.USER,
            password=self._database_settings.PASSWORD,
            host=self._database_settings.HOST,
            port=self._database_settings.PORT,
        ) as conn:
            with conn.cursor() as cur:
                yield cur
