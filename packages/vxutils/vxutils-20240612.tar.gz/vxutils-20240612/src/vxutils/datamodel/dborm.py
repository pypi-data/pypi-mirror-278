"""数据库ORM抽象"""

import logging
from enum import Enum
from typing import (
    Iterator,
    List,
    Optional,
    Type,
    Union,
    Dict,
    Tuple,
    Any,
    Literal,
    Generator,
)
from functools import singledispatch
from collections import namedtuple
from contextlib import contextmanager
from multiprocessing import Lock
import sqlite3
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Boolean,
    Float,
    Integer,
    LargeBinary,
    Text,
    DateTime,
    Date,
    Time,
    text,
)
from sqlalchemy.engine.base import Connection
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.types import TypeEngine
from datetime import datetime, date, time as dt_time, timedelta
from vxutils.datamodel.core import VXDataModel


SHARED_MEMORY_DATABASE = "file:vxquantdb?mode=memory&cache=shared"

__columns_mapping__: Dict[Any, TypeEngine] = {
    int: Integer,
    float: Float,
    bool: Boolean,
    bytes: LargeBinary,
    Enum: Text(256),
    datetime: DateTime,
    date: Date,
    dt_time: Time,
    timedelta: Float,
}

VXTableInfo = namedtuple("VXTableInfo", ["table", "model", "primary_keys"])


@singledispatch
def db_normalize(value: Any) -> Any:
    """标准化处理数据库数值"""
    return value


@db_normalize.register(Enum)
def _(value: Enum) -> str:
    return value.name


@db_normalize.register(datetime)
def _(value: datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M:%S")


@db_normalize.register(date)
def _(value: date) -> str:
    return value.strftime("%Y-%m-%d")


@db_normalize.register(dt_time)
def _(value: dt_time) -> str:
    return value.strftime("%H:%M:%S")


@db_normalize.register(timedelta)
def _(value: timedelta) -> float:
    return value.total_seconds()


@db_normalize.register(bool)
def _(value: bool) -> int:
    return 1 if value else 0


@db_normalize.register(type(None))
def _(value: None) -> str:
    return ""


class VXDataBase:

    def __init__(self, db_uri: str = "", **kwargs: Any) -> None:

        self._lock = Lock()
        self._metadata = MetaData()
        self._tblmapping: Dict[str, Type[VXDataModel]] = {}

        if not db_uri:
            kwargs["creator"] = lambda: sqlite3.connect(
                SHARED_MEMORY_DATABASE, uri=True
            )
            self._dbengine = create_engine("sqlite:///:memory:", **kwargs)
        else:
            self._dbengine = create_engine(db_uri, **kwargs)

    def create_table(
        self,
        table_name: str,
        primary_keys: List[str],
        vxdatacls: Type[VXDataModel],
        if_exists: Literal["ignore", "replace"] = "ignore",
    ) -> "VXDataBase":
        """创建数据表

        Arguments:
            table_name {str} -- 数据表名称
            primary_keys {List[str]} -- 表格主键
            vxdatacls {_type_} -- 表格数据格式
            if_exists {str} -- 如果table已经存在，若参数为ignore ，则忽略；若参数为 replace，则replace掉已经存在的表格，然后再重新创建

        Returns:
            vxDataBase -- 返回数据表格实例
        """
        column_defs = [
            Column(
                name,
                __columns_mapping__.get(field_info.annotation, Text(256)),
                primary_key=(name in primary_keys),
                nullable=(name in primary_keys),
            )
            for name, field_info in vxdatacls.model_fields.items()
        ]

        if table_name in self._metadata.tables.keys():
            if if_exists == "ignore":
                logging.debug("Table %s already exists", table_name)
                return self
            elif if_exists == "replace":
                tbl = self._metadata.tables[table_name]
                tbl.drop(bind=self._dbengine, checkfirst=True)
                logging.info("Table %s already exists, replace it", table_name)
                self._metadata.remove(self._metadata.tables[table_name])

        tbl = Table(table_name, self._metadata, *column_defs)
        self._tblmapping[table_name] = vxdatacls
        tbl.create(bind=self._dbengine, checkfirst=True)
        logging.debug("Create Table: [%s] ==> %s", table_name, vxdatacls)
        return self

    def drop_table(self, table_name: str) -> "VXDataBase":
        """删除数据表

        Arguments:
            table_name {str} -- 数据表名称

        Returns:
            vxDataBase -- 返回数据表格实例
        """
        if table_name in self._metadata.tables.keys():
            tbl = self._metadata.tables[table_name]
            tbl.drop(bind=self._dbengine, checkfirst=True)
            logging.info("Table %s dropped", table_name)
            self._metadata.remove(self._metadata.tables[table_name])

        if table_name in self._tblmapping.keys():
            self._tblmapping.pop(table_name)

        return self

    def truncate(self, table_name: str) -> "VXDataBase":
        """清空表格

        Arguments:
            table_name {str} -- 待清空的表格名称
        """
        if table_name in self._metadata.tables.keys():
            tbl = self._metadata.tables[table_name]

            with self._dbengine.begin() as conn:
                conn.execute(tbl.delete())
            logging.warning("Table %s truncated", table_name)
        return self

    @contextmanager
    def start_session(self, with_lock: bool = True) -> Generator[Any, Any, Any]:
        """开始session，锁定python线程加锁，保障一致性"""
        if with_lock:
            with self._lock, self._dbengine.begin() as conn:
                yield VXDBSession(conn, self._tblmapping, self._metadata)
        else:
            with self._dbengine.begin() as conn:
                yield VXDBSession(conn, self._tblmapping, self._metadata)

    def get_dbsession(self) -> "VXDBSession":
        """获取一个session"""
        return VXDBSession(self._dbengine.connect(), self._tblmapping, self._metadata)


class VXDBSession:

    def __init__(
        self,
        conn: Connection,
        tblmapping: Dict[str, Type[VXDataModel]],
        metadata: MetaData,
    ) -> None:
        self._conn = conn
        self._tblmapping = tblmapping
        self._metadata = metadata

    def save(self, table_name: str, *vxdataobjs: VXDataModel) -> "VXDBSession":
        """插入数据

        Arguments:
            table_name {str} -- 表格名称
            vxdataobjs {VXDataModel} -- 数据
        """

        tbl = self._metadata.tables[table_name]
        insert_stmt = (
            sqlite_insert(tbl)
            .values(
                [
                    {k: v for k, v in vxdataobj.model_dump().items()}
                    for vxdataobj in vxdataobjs
                ]
            )
            .execution_options()
        ).on_conflict_do_update(
            index_elements=tbl.primary_key,
            set_={
                k: v
                for k, v in vxdataobjs[0].model_dump().items()
                if k not in tbl.primary_key
            },
        )
        self._conn.execute(insert_stmt)
        logging.debug("Table %s saved, %s", table_name, insert_stmt.compile())
        return self

    def remove(self, table_name: str, *vxdataobjs: VXDataModel) -> "VXDBSession":
        """删除数据

        Arguments:
            table_name {str} -- 表格名称
            vxdataobjs {VXDataModel} -- 数据
        """
        tbl = self._metadata.tables[table_name]
        delete_stmt = tbl.delete().where(
            tbl.c[tbl.primary_key.columns.keys()[0]]
            == vxdataobjs[0].model_dump()[tbl.primary_key.columns.keys()[0]]
        )
        self._conn.execute(delete_stmt)
        logging.debug("Table %s deleted, %s", table_name, delete_stmt)
        return self

    def delete(self, table_name: str, *exprs: str, **options: Any) -> "VXDBSession":
        """删除数据

        Arguments:
            table_name {str} -- 表格名称

        Returns:
            Iterator[VXDataModel] -- 返回查询结果
        """
        query = list(exprs)
        if options:
            query.extend(f"{k}={v}" for k, v in options.items())

        delete_stmt = (
            f"delete from {table_name} where {' and '.join(query)};"
            if query
            else f"delete from {table_name} ; "
        )

        result = self._conn.execute(text(delete_stmt))
        logging.debug("Table %s deleted  %s rows", table_name, result.rowcount)
        return self

    def find(
        self,
        table_name: str,
        *exprs: str,
        **options: Any,
    ) -> Iterator[VXDataModel]:
        """查询数据

        Arguments:
            table_name {str} -- 表格名称

        Returns:
            Iterator[VXDataModel] -- 返回查询结果
        """
        query = list(exprs)
        if options:
            query.extend(f"{k}='{v}'" for k, v in options.items())

        query_stmt = text(
            f"select * from {table_name} where {' and '.join(query)};"
            if query
            else f"select * from {table_name};"
        )
        result = self._conn.execute(query_stmt)
        for row in result:
            yield self._tblmapping[table_name](**dict(zip(row._fields, row)))

    def findone(
        self,
        table_name: str,
        *exprs: str,
        **options: Any,
    ) -> Optional[VXDataModel]:
        """查询数据

        Arguments:
            table_name {str} -- 表格名称

        Returns:
            Iterator[VXDataModel] -- 返回查询结果
        """
        query = list(exprs)
        if options:
            query.extend(f"{k}='{v}'" for k, v in options.items())

        query_stmt = text(
            f"select * from {table_name} where {' and '.join(query)};"
            if query
            else f"select * from {table_name};"
        )
        result = self._conn.execute(query_stmt)
        row = result.fetchone()

        return (
            self._tblmapping[table_name](**dict(zip(row._fields, row))) if row else None
        )

    def distinct(self, table_name: str, column: str) -> List[VXDataModel]:
        """查询数据

        Arguments:
            table_name {str} -- 表格名称

        Returns:
            Iterator[VXDataModel] -- 返回查询结果
        """
        query_stmt = text(f"select distinct {column} from {table_name};")
        result = self._conn.execute(query_stmt)
        return [row for row in result]

    def count(self, table_name: str, *exprs: str, **options: Any) -> int:
        """查询数据

        Arguments:
            table_name {str} -- 表格名称

        Returns:
            Iterator[VXDataModel] -- 返回查询结果
        """
        query = list(exprs)
        if options:
            query.extend(f"{k}='{v}'" for k, v in options.items())

        query_stmt = text(
            f"select count(1) as count from {table_name} where {' and '.join(query)};"
            if query
            else f"select count(1) as count from {table_name};"
        )
        row = self._conn.execute(query_stmt).fetchone()
        return row[0]

    def max(self, table_name: str, column: str, *exprs: str, **options: Any) -> Any:
        """查询数据

        Arguments:
            table_name {str} -- 表格名称

        Returns:
            Iterator[VXDataModel] -- 返回查询结果
        """
        query = list(exprs)
        if options:
            query.extend(f"{k}='{v}'" for k, v in options.items())

        query_stmt = text(
            f"select max({column}) as max from {table_name} where {' and '.join(query)};"
            if query
            else f"select max({column}) as max from {table_name};"
        )
        row = self._conn.execute(query_stmt).fetchone()
        return row[0]

    def min(self, table_name: str, column: str, *exprs: str, **options: Any) -> Any:
        """查询数据

        Arguments:
            table_name {str} -- 表格名称

        Returns:
            Iterator[VXDataModel] -- 返回查询结果
        """
        query = list(exprs)
        if options:
            query.extend(f"{k}='{v}'" for k, v in options.items())

        query_stmt = text(
            f"select min({column}) as min from {table_name} where {' and '.join(query)};"
            if query
            else f"select min({column}) as min from {table_name};"
        )
        row = self._conn.execute(query_stmt).fetchone()
        return row[0]

    def mean(self, table_name: str, column: str, *exprs: str, **options: Any) -> Any:
        """查询数据

        Arguments:
            table_name {str} -- 表格名称

        Returns:
            Iterator[VXDataModel] -- 返回查询结果
        """
        query = list(exprs)
        if options:
            query.extend(f"{k}='{v}'" for k, v in options.items())

        query_stmt = text(
            f"select avg({column}) as mean from {table_name} where {' and '.join(query)};"
            if query
            else f"select avg({column}) as mean from {table_name};"
        )
        row = self._conn.execute(query_stmt).fetchone()
        return row[0]

    def execute(
        self, sql: str, params: Optional[Union[Tuple, Dict, List]] = None
    ) -> Any:
        return self._conn.execute(text(sql), params)

    def commit(self) -> Any:
        return self._conn.commit()

    def rollback(self) -> Any:
        return self._conn.rollback()

    def __enter__(self) -> Any:
        pass
