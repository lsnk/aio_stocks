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
