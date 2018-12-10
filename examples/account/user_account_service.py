# -*- coding: utf-8 -*-

import logging

from torstack.library.encipher import EncipherLibrary
from account.models import UserAccount

logger = logging.getLogger(__name__)

dbname = 'test'

class UserAccountService(object):

    @staticmethod
    def get_one(db_session, username):
        with db_session.session_ctx(dbname) as session:
            return session.query(UserAccount).filter(UserAccount.username == username).first()

    @staticmethod
    def add_data(db_session, username, password, nickname):
        try:
            data = {
                'username': username,
                'nickname': nickname,
                'status': '1',
            }
            data['salt'] = EncipherLibrary.gen_token(10)
            data['password'] = EncipherLibrary.encrypt(password, data['salt'])

            data_to_save = UserAccount(**data)

            with db_session.session_ctx('dbname') as session:
                session.add(data_to_save)
                session.commit()
            return data_to_save
        except Exception as e:
            logger.exception(e)
        return None

    @staticmethod
    def update_password(db_session, username, old_password, new_password):
        userData = UserAccountService.get_one(username)
        if userData:
            if userData.password == EncipherLibrary.encrypt(old_password, userData.salt):
                # 密码正确
                with db_session.session_ctx('dbname') as session:
                    count = session.query(UserAccount).filter(UserAccount.username == username).update({"password":new_password})
                    if count:
                        session.commit()
                        return True
        return False

    @staticmethod
    def get_count(db_session):
        with db_session.session_ctx('dbname') as session:
            return session.query(UserAccount).count()

    @staticmethod
    def list_data(db_session, status=True):
        if status:
            with db_session.session_ctx('dbname') as session:
                dataList = session.query(UserAccount).filter(UserAccount.status == '1').order_by(UserAccount.id.asc()).all()
        else:
            with db_session.session_ctx('dbname') as session:
                dataList = session.query(UserAccount).order_by(UserAccount.id.asc()).all()

        return dataList

    @staticmethod
    def check_password(db_session, username, password):
        userData = UserAccountService.get_one(username)
        if userData:
            if userData.password == EncipherLibrary.encrypt(password, userData.salt):
                return True
        return False