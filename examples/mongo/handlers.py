# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import tornado.web
from tornado import gen
from torstack.handler.base import BaseHandler
from torstack.library.encipher import EncipherLibrary
from mongo.user_account_service import UserAccountService
from mongo.models import user_data, user_session_data
import pprint

class AccountHandler(BaseHandler):
    '''
    AccountHandler
    '''
    def initialize(self):
        super(AccountHandler, self).initialize()
        self.db = self.storage['mongodb']

class HomeHandler(AccountHandler):
    '''
    home
    '''
    @tornado.web.authenticated
    def get(self):
        return self.response("account/home.html")

class LoginHandler(AccountHandler):
    '''
    login
    '''

    @gen.coroutine
    def get(self):
        next_url = self.get_argument('next', '/')
        self.response("account/login.html", next_url=next_url)

    @gen.coroutine
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        next_url = self.get_argument('next', '/')

        userData = yield UserAccountService.get_one(self.db, username)
        # pprint.pprint(userData)
        if userData is not None:
            if userData['password'] == EncipherLibrary.encrypt(password, userData['salt']):
                session_data = {x: userData[x] for x in userData if x in user_session_data}
                self.set_session(session_data)
                self.add_message("success", u"Login success, Wellcome back，{0}!".format(username))
                return self.redirect(next_url)
            else:
                self.add_message("danger", u"Login failed, error password")
                return self.redirect("/")
        else:
            self.add_message("danger", u"Login failed, error username")
            return self.redirect("/")

class RegisterHandler(AccountHandler):
    '''
    register
    '''

    @gen.coroutine
    def get(self):

        next_url = self.get_argument('next', '/')
        register_data = dict(
            username='',
            nickname='',
            password='',
            password2='',
            next_url=next_url,
        )

        return self.response("account/register.html", **register_data)

    @gen.coroutine
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        password2 = self.get_argument('password2')
        nickname = self.get_argument('nickname')
        next_url = self.get_argument('next', '/')

        register_data = dict(
            username=username,
            password=password,
            password2=password2,
            nickname=nickname,
            next_url=next_url,
        )

        if password != password2:
            self.add_message("danger", u"Password confirm failed")
            return self.response("account/register.html", **register_data)

        userData = yield UserAccountService.get_one(self.db, username)
        if userData is None:
            result = yield UserAccountService.add_data(self.db, username, password, nickname)
            if result:
                userData = yield UserAccountService.get_one(self.db, username)
                session_data = {x: userData[x] for x in userData if x in user_session_data}
                self.set_session(session_data)
                self.add_message("success", u"Register success, Wellcome，{0}!".format(username))
                return self.redirect(next_url)
            else:
                self.add_message("danger", u"Register failed")
                return self.response("account/register.html", **register_data)
        else:
            self.add_message("danger", u"Register failed, username is exist")
            return self.response("account/register.html", **register_data)

class LogoutHandler(AccountHandler):
    '''
    logout
    '''
    def get(self):
        self.clean_session()
        self.add_message("success", u"Logout success.")
        return self.redirect("/")

class ErrorHandler(AccountHandler):
    '''
    error handler
    '''
    def prepare(self):
        # raise tornado.web.HTTPError(404)
        self.set_status(404)
        self.response("public/404.html")