import ujson
from asyncpgsa import pg
from asyncpgsa.connection import get_dialect
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

import settings


Base = declarative_base()


class Security(Base):
    __tablename__ = 'securities'

    isin = Column(String, primary_key=True)
    data = Column(JSON)
    last_updated = Column(DateTime, nullable=False)


if __name__ == '__main__':
    engine = create_engine(
        settings.DB_URI,
        connect_args={"options": "-c timezone=utc"},
    )
    Base.metadata.create_all(engine)


async def set_db_json_charset(connection):
    await connection.set_type_codec(
        'json',
        encoder=ujson.dumps,
        decoder=ujson.loads,
        schema='pg_catalog',
    )


async def connect_db():
    await pg.init(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,

        init=set_db_json_charset,
    )


async def disconnect_db():
    await pg.pool.close()
