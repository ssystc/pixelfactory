# coding: utf-8

import requests
import uuid
import flask
import base64
import json
import functools
import config
import M2Crypto
import time
from model.logininfo import LoginInfoDao, LoginInfo
from model.redirect import RedirectDao, Redirect
from webserver import app
from common.const import ErrorCode
import traceback
import socket
from common.userserver import getTokenByuserid


def decrypt(access_token):
    bio = M2Crypto.BIO.MemoryBuffer(config.PUBLIC_KEY)
    pkey = M2Crypto.RSA.load_pub_key_bio(bio)
    token = pkey.public_decrypt(base64.decodestring(
        access_token),M2Crypto.RSA.no_padding)
    return token.strip('\x00')



@app.route('/user/login', methods=['GET'])
def login():

    if config.DEBUG_STATUS:
        uid = 'aaaaa'
    else:
        uid = uuid.uuid4().hex
        
    flask.session.permanent = True
    flask.session['uid'] = uid
    
    config.Log.info('*********************step 1, uid = %s******************' % flask.session['uid'])
    
    if 'redirect' in flask.request.args:
        prams = ['%s=%s' % (arg, flask.request.args[arg]) for arg in flask.request.args if arg != 'redirect']
        if prams:
            rurl = '%s&%s' % (flask.request.args['redirect'], '&'.join(prams))
        else:
            rurl = flask.request.args['redirect']

        redirect = Redirect(uid, rurl)
        RedirectDao.add(redirect)

    loginurl = 'https://%s%s' % (config.OAUTH_URL, config.OAUTH_LOGIN_URL %
                                 (config.CLIENT_ID, config.OAUTH_REDIRECT_URL, uid))
    config.Log.info('loginurl : %s' % loginurl)
    # loginurl = "https://192.168.4.225:8443/user_oauth/oauth-server-idp/oauth2/authorize?client_id=200010035116400&redirect_uri=http://127.0.0.1:8888/user/logincallback/%s&response_type=code" % uid
    return flask.redirect(loginurl)



@app.route('/user/logincallback/<uid>')
def autho(uid):
    try:
        code = flask.request.args['code']

        config.Log.info('line 63, uid = %s' % code)

        rep = requests.post('https://%s%s' % (config.OAUTH_URL, config.OAUTH_REQUIRE_TOKEN_URL),
                    data={'client_id': config.CLIENT_ID, 'code': code, 'grant_type': 'authorization_code',
                          'ip': config.WEB_SERVER_IP},
                    verify=False)

        repmessage = json.loads(rep.content)
        token_nodecrypt = repmessage['access_token']
        refresh_token_nodecrypt = repmessage['refresh_token']
        token_crypt = decrypt(token_nodecrypt)

        verifyrep = requests.post('https://%s%s' % (config.OAUTH_URL, config.OAUTH_VARIFY_URL),
                                  data={'client_id': config.CLIENT_ID, 'token': token_crypt},
                                  verify=False)

        verifymessage = json.loads(verifyrep.content)
        roles = json.loads(verifymessage['roles'])['role']
        if 'errors_cede' not in verifymessage and config.OAUTH_FACTORY_ROLE in roles:
            user_id = verifymessage['userID']
            user_name = verifymessage['username']
            LoginInfoDao.deleteByuserid(user_id)
            login_info = LoginInfo(uid, token_nodecrypt, refresh_token_nodecrypt, user_id, user_name, time.time())
            LoginInfoDao.add(login_info)
            '''
            test = LoginInfoDao.queryByuserid(user_id)
            config.Log.info('SendLoginInfo=%s' % user_id)
            config.Log.info(test)
            url = 'http://%s/SendLoginInfo' % (config.TEZHENGDIAN_HOST)
            req = requests.post(url, data={'uid': test.uid,
                                      'token': test.token,
                                      'username':test.username,
                                      'userid':test.userid}
                                )
            '''
            url = RedirectDao.pop(uid) or config.INDEX_PAGE
            return flask.redirect(url)
        if 'errors_cede' not in verifymessage and config.OAUTH_FACTORY_ROLE not in roles:
            return flask.abort(401)
        else:
            return flask.jsonify({'code': ErrorCode.LoginError, 'errors_code': verifymessage['errors_code']})


    except:
        config.Log.info(traceback.format_exc())
        return flask.jsonify({'code': ErrorCode.LoginError})


def needLogin():
    if config.DEBUG_STATUS:
        flask.session['uid'] = 'aaaaa'
        return False
    else:
        try:
            uid = flask.session['uid']
            logininfo = LoginInfoDao.queryByuid(uid)
            token = decrypt(logininfo.token)
            refreshtoken = logininfo.refreshtoken
            verifyrep = requests.post('https://%s%s' % (config.OAUTH_URL, config.OAUTH_VARIFY_URL),
                                      data={'client_id': config.CLIENT_ID, 'token': token},
                                      verify=False)
            config.Log.info('verify token: %s' % token)
            config.Log.info('ret: %s' % verifyrep.content)

            verifymessage = json.loads(verifyrep.content)
            if 'errors_code' not in verifymessage:
                return False

            if verifymessage['errors_code'] == 10004002 or verifymessage['errors_code'] == 10003005:
                # 需要在数据库中更新token和refreshtoken
                refreshrep = requests.post('https://%s%s' % (config.OAUTH_URL, config.OAUTH_REQUIRE_TOKEN_URL),
                                           data={'grant_type': 'refresh_token', 'refresh_token': refreshtoken,
                                                 'client_id': config.CLIENT_ID},
                                           verify=False
                                           )
                config.Log.info('refresh token: refresh_token = %s' % refreshtoken)
                config.Log.info('refresh ret: %s' % refreshrep.content)

                newtokenmessage = json.loads(refreshrep.content)
                newtoken = newtokenmessage['access_token']
                newtoken_crypt = decrypt(newtoken)
                newrefreshtoken = newtokenmessage['refresh_token']

                newverifyrep = requests.post('https://%s%s' % (config.OAUTH_URL, config.OAUTH_VARIFY_URL),
                                             data={'client_id': config.CLIENT_ID, 'token': newtoken_crypt},
                                             verify=False)
                config.Log.info('verify with new token: %s' % newtoken_crypt)
                config.Log.info('new verify ret: %s' % newverifyrep.content)
                newverifymessage = json.loads(newverifyrep.content)

                if 'errors_code' not in newverifymessage:
                    user_id = newverifymessage['userID']
                    user_name = newverifymessage['username']
                    LoginInfoDao.deleteByuserid(user_id)
                    login_info = LoginInfo(uid, newtoken, newrefreshtoken, user_id, user_name, time.time())
                    LoginInfoDao.add(login_info)
                    return False
                else:
                    return True

            else:
                return True

        except:
            return True


def login_required(func):
    '''测试登陆状态，如果未登陆则跳转到登陆页面'''
    @functools.wraps(func)
    def decoratedFunc(*args, **kwargs):
        if needLogin():
            return flask.abort(401)
        return func(*args, **kwargs)
    return decoratedFunc


@app.route('/user/queryusername', methods=['GET'])
@login_required
def queryUsername():
    uid = flask.session['uid']
    login_info = LoginInfoDao.queryByuid(uid)
    if login_info:
        return flask.jsonify({'username': login_info.username, 'code': ErrorCode.NoError})
    else:
        return flask.jsonify({'code': ErrorCode.NotFindUser})


@app.route('/user/querytoken', methods=['GET'])
@login_required
def querytoken():
    uid = flask.session['uid']
    login_info = LoginInfoDao.queryByuid(uid)
    if login_info:
        userid = login_info.userid
        token = getTokenByuserid(userid)
        if token:
            return flask.jsonify({'token': token, 'code': ErrorCode.NoError})
        else:
            return flask.abort(401)
    else:
        return flask.jsonify({'code': ErrorCode.NotFindUser})


@app.route('/user/logout', methods=['GET'])
def logout():
    uid = flask.session['uid']
    if LoginInfoDao.queryByuid(uid):
        flask.session['uid'] = ''
        return flask.jsonify({'code': ErrorCode.NoError})
    else:
        return flask.jsonify({'code': ErrorCode.NotUserLogin})


def getUserId():
    if config.DEBUG_STATUS:
        uid = 'aaaaa'
        return LoginInfoDao.getUserId(uid)
    else:
        if 'uid' in flask.session:
            return LoginInfoDao.getUserId(flask.session['uid'])
        else:
            return ''
