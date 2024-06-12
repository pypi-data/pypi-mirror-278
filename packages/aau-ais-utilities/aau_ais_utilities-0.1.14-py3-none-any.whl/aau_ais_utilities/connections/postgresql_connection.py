"""PostgreSQLConnection class to run sql queries on a given SQL database."""
from pathlib import Path

from jinjasql import JinjaSql
from sqlalchemy import text, Engine, CursorResult
from sqlalchemy.orm import sessionmaker


class PostgreSQLConnection:
    """Run sql queries on a given SQL database."""

    def __init__(self, engine: Engine) -> None:
        """Initialize the SQLRunner class.

        Args:
            engine: The sqlalchemy engine to use for connecting to the SQL database.
        """
        self.engine = engine
        self.session = sessionmaker(bind=self.engine)
        self.jsql = JinjaSql(param_style='named')

    def execute_jinja(self, *, sql: str | Path, params: dict) -> CursorResult:
        """Execute SQL query with jinja templating on the database.

        Function avoids SQL injection attacks by using jinjasql templating.

        Args:
            sql: The sql query to run or the path to a file containing the query, with jinja templating.
            params: A dictionary of parameters to pass to the sql query.
        """
        sql = self._validate_and_process_sql(sql)

        sql_query, bind_params = self.jsql.prepare_query(sql, params)

        return self._executing_session(text(sql_query), bind_params)

    def execute_raw(self, *, sql: str | Path, params: dict = None) -> CursorResult:
        """Execute a raw SQL query on the database.

        Warnings:
            This is not recommended for production use as it can lead to SQL injection attacks.

        Args:
            sql: The sql query to run or the path to a file containing the query.
            params: A dictionary of parameters to pass to the sql query. Defaults to None.
        """
        sql_query = self._validate_and_process_sql(sql)

        return self._executing_session(text(sql_query), params)

    @staticmethod
    def _validate_and_process_sql(sql: str | Path) -> str:
        """Validate the sql query and process it into a string.

        Args:
            sql: The sql query to validate and process.

        Raises:
            ValueError: If the sql query is not a string or a path to a file containing the query.
        """
        if isinstance(sql, Path):
            with open(sql, 'r') as sql_file:
                sql = sql_file.read()
        if not isinstance(sql, str):
            raise ValueError('The sql query must be a string or a path to a file containing the query.')
        return sql

    def _executing_session(self, sql_query: text, params: dict = None) -> CursorResult:
        """Execute SQL query on the database.

        Args:
            sql_query: The sql query to run.
            params: A dictionary of parameters to pass to the sql query. Defaults to None.

        Raises:
            Exception: If an error occurs during the execution of the SQL query.
        """
        session = self.session()

        try:
            result = session.connection().execute(sql_query, params)
            session.commit()

        except Exception as e:
            raise e

        finally:
            session.close()

        return result
