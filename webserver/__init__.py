# coding: utf-8

from flask import Flask, session
import flask_cors
import os
import requests
from datetime import timedelta


app = Flask(__name__, static_url_path='')
app.config['JSON_AS_ASCII'] = False
# app.secret_key = os.urandom(24)
app.secret_key = 'rZa4i7yh898Dh6BV5xiSaYdvxu0nD6kIH6CZTYuYJCFF469jGhByHap2cHOvB2vA'

# session.permanent = True
app.permanent_session_lifetime = timedelta(minutes=240)

# 跨域访问
# flask_cors.CORS(app)
flask_cors.CORS(app, supports_credentials=True)

# 忽略https警告
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

import api
import user
import model

model.redirect.RedirectDao.deleteAll()

