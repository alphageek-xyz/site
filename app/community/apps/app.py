# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import include
from django.conf.urls import url
from machina.app import BoardApp

from community.apps.auth.app import application as auth_app

class AGCSForumApp(BoardApp):
    name = None
    auth_app = auth_app

    def get_urls(self):
        urls = super(AGCSForumApp, self).get_urls()
        return urls + [
            url(r'^account/', include(self.auth_app.urls)),
        ]


application = AGCSForumApp()
