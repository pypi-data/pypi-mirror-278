from sqlalchemy import create_engine, Table, MetaData, select, desc, asc, and_, insert, delete, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, Any, Optional, List, ContextManager
import contextlib
import logging
from .config import env


__all__ = ["DatabaseSession", "DatabaseQuery"]
DB_URL_TEMPLATE = "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4"
DB_PREFIX = env("DB_PREFIX")
DB_USER = env("DB_USER")
DB_PASSWORD = env("DB_PASSWORD")
DB_HOST = env("DB_HOST")
DB_NAME = env("DB_NAME")

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class DatabaseQuery:
    def __init__(self, session, table):
        self.session = session
        self.table = table
        self._where_conditions = None
        self._order_by = None
        self._limit = None

    def where(self, conditions: Dict[str, Any]):
        self._where_conditions = conditions
        return self

    def order_by(self, *order_by_columns: str, descending: bool = False):
        self._order_by = [desc(col) if descending else asc(col) for col in order_by_columns]
        return self

    def limit(self, limit: int):
        self._limit = limit
        return self

    def _build_select_statement(self):
        stmt = select(self.table)
        if self._where_conditions:
            conditions = and_(*(getattr(self.table.c, k) == v for k, v in self._where_conditions.items()))
            stmt = stmt.where(conditions)
        if self._order_by:
            stmt = stmt.order_by(*self._order_by)
        if self._limit:
            stmt = stmt.limit(self._limit)
        return stmt

    def select(self) -> List[Dict[str, Any]]:
        try:
            stmt = self._build_select_statement()
            result = self.session.execute(stmt).fetchall()
            return [dict(row._mapping) for row in result]
        except SQLAlchemyError as e:
            logger.error(f"Error occurred while executing select query: {e}")
            raise

    def find(self) -> Optional[Dict[str, Any]]:
        try:
            stmt = self._build_select_statement()
            result = self.session.execute(stmt).first()
            return dict(result._mapping) if result else None
        except SQLAlchemyError as e:
            logger.error(f"Error occurred while executing find query: {e}")
            raise

    def insert(self, data: Dict[str, Any]):
        try:
            statement = insert(self.table).values(**data)
            self.session.execute(statement)
            self.session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Error occurred while executing insert query: {e}")
            self.session.rollback()
            raise

    def update(self, data: Dict[str, Any]):
        try:
            if not self._where_conditions:
                raise ValueError("Where conditions are required for update operation")
            conditions = and_(*(getattr(self.table.c, k) == v for k, v in self._where_conditions.items()))
            statement = update(self.table).values(**data).where(conditions)
            self.session.execute(statement)
            self.session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Error occurred while executing update query: {e}")
            self.session.rollback()
            raise

    def delete(self):
        try:
            if not self._where_conditions:
                raise ValueError("Where conditions are required for delete operation")
            conditions = and_(*(getattr(self.table.c, k) == v for k, v in self._where_conditions.items()))
            statement = delete(self.table).where(conditions)
            self.session.execute(statement)
            self.session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Error occurred while executing delete query: {e}")
            self.session.rollback()
            raise


class DatabaseSession:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseSession, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if not self.__initialized:
            self.__initialized = True
            self.engine = create_engine(DB_URL_TEMPLATE.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME))
            self.Session = sessionmaker(bind=self.engine)

    @contextlib.contextmanager
    def get_session(self) -> ContextManager:
        session = self.Session()
        try:
            yield session
        finally:
            session.close()

    @staticmethod
    def db(table_name: str) -> DatabaseQuery:
        instance = DatabaseSession()
        table = get_table(table_name, instance.engine)
        with instance.get_session() as session:
            return DatabaseQuery(session, table)


def get_table(table_name: str, engine) -> Table:
    metadata = MetaData()
    table_name = f"{DB_PREFIX}{table_name}"
    return Table(table_name, metadata, autoload_with=engine)
