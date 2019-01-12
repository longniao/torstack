# coding: utf-8
from sqlalchemy import CHAR, Column, INTEGER, text
from sqlalchemy.dialects.mysql.types import TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SqlalchemyModel(Base):
    __tablename__ = ''

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}