# coding: utf-8
from sqlalchemy import CHAR, Column, INTEGER, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql.types import TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class UserAccount(Base):
    __tablename__ = 'user_account'

    id = Column(INTEGER, primary_key=True)
    username = Column(String(30), nullable=False, index=True, server_default=text("''"))
    nickname = Column(CHAR(36), nullable=False, server_default=text("''"))
    password = Column(CHAR(64), nullable=False, server_default=text("''"))
    salt = Column(CHAR(10), nullable=False, server_default=text("''"))
    must_change_password = Column(TINYINT(2), nullable=False, server_default=text("'0'"))
    banned = Column(TINYINT(2), nullable=False, server_default=text("'0'"))
    suspended = Column(TINYINT(2), nullable=False, server_default=text("'0'"))
    status = Column(TINYINT(2), nullable=False, server_default=text("'0'"))
    created_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    @property
    def session_data(self):
        session = dict()
        columns = ['id', 'username', 'nickname', 'banned', 'suspended', 'status']
        for c in self.__table__.columns:
            if c.name in columns:
                session[c.name] = getattr(self, c.name)
        return session