# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import tornado.web
from tornado import gen
from torstack.handler.base import BaseHandler
from torstack.library.encipher import EncipherLibrary
from account.user_account_service import UserAccountService

class HomeHandler(BaseHandler):
    '''
    home
    '''
    @tornado.web.authenticated
    def get(self):
        return self.response("account/home.html")

class LoginHandler(BaseHandler):
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

        userData = UserAccountService.get_one(self.db, username)
        if userData is not None:
            if userData.password == EncipherLibrary.encrypt(password, userData.salt):
                self.set_session(userData.session_data)
                self.add_message("success", u"Login success, Wellcome back，{0}!".format(username))
                return self.redirect(next_url)
            else:
                self.add_message("danger", u"Login failed, error password")
                return self.redirect("/")
        else:
            self.add_message("danger", u"Login failed, error username")
            return self.redirect("/")

class RegisterHandler(BaseHandler):
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

        userData = UserAccountService.get_one(self.db, username)
        if userData is None:
            result = UserAccountService.add_data(self.db, username, password, nickname)
            if result:
                userData = UserAccountService.get_one(self.db, username)
                self.set_session(userData.session_data)
                self.add_message("success", u"Register success, Wellcome，{0}!".format(username))
                return self.redirect(next_url)
            else:
                self.add_message("danger", u"Register failed")
                return self.response("account/register.html", **register_data)
        else:
            self.add_message("danger", u"Register failed, username is exist")
            return self.response("account/register.html", **register_data)

class LogoutHandler(BaseHandler):
    '''
    logout
    '''
    def get(self):
        self.clean_session()
        self.add_message("success", u"Logout success.")
        return self.redirect("/")

