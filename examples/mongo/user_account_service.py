# -*- coding: utf-8 -*-

import logging

from torstack.library.encipher import EncipherLibrary
from mongo.models import user_data, user_session_data
import pprint
from datetime import datetime

logger = logging.getLogger(__name__)

collection = 'user_account'

class UserAccountService(object):

    @staticmethod
    async def get_one(db_session, username):
        with db_session.session_ctx('test') as db:
            userData = await db[collection].find_one({'username': username})
            return userData

    @staticmethod
    async def add_data(db_session, username, password, nickname):
        try:
            data = user_data.copy()
            data['username'] = username
            data['nickname'] = nickname
            data['salt'] = EncipherLibrary.gen_token(10)
            data['password'] = EncipherLibrary.encrypt(password, data['salt'])
            data['create_time'] = datetime.now()

            with db_session.session_ctx('dbname') as db:
                await db[collection].insert_one(data)
            return data
        except Exception as e:
            logger.exception(e)
        return None

    @staticmethod
    async def update_password(db_session, username, old_password, new_password):
        userData = UserAccountService.get_one(db_session, username)
        if userData:
            if userData.password == EncipherLibrary.encrypt(old_password, userData.salt):
                # 密码正确
                with db_session.session_ctx('dbname') as db:
                    _id = userData['_id']
                    result = await db[collection].update_one({'_id': _id}, {'$set': {"password":new_password}})
                    pprint.pprint(result)
                    if result:
                        return True
        return False

    @staticmethod
    async def get_count(db_session):
        with db_session.session_ctx('dbname') as db:
            count = await db[collection].count_documents({'status':'1'})
            return count

    @staticmethod
    async def list_data(db_session, status=True):
        dataList = []
        if status:
            with db_session.session_ctx('dbname') as db:
                cursor = db[collection].find({'status':'1'}).sort('id')
                for userData in await cursor.to_list(length=100):
                    dataList.append(userData)
                    pprint.pprint(userData)
        else:
            with db_session.session_ctx('dbname') as db:
                cursor = db[collection].find({}).sort('id')
                for userData in await cursor.to_list(length=100):
                    dataList.append(userData)
                    pprint.pprint(userData)

        return dataList

    @staticmethod
    async def check_password(db_session, username, password):
        userData = UserAccountService.get_one(db_session, username)
        if userData:
            if userData['password'] == EncipherLibrary.encrypt(password, userData['salt']):
                return True
        return False