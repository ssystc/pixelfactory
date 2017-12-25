# coding: utf-8

from model.logininfo import LoginInfoDao, LoginInfo
import requests
import config
import json
import M2Crypto
import base64
import time

def crypt(access_token):
    bio = M2Crypto.BIO.MemoryBuffer(config.PUBLIC_KEY)
    pkey = M2Crypto.RSA.load_pub_key_bio(bio)
    token = pkey.public_decrypt(base64.decodestring(
        access_token),M2Crypto.RSA.no_padding)
    return token.strip('\x00')

def getTokenByuserid(userid):
    myinfo = LoginInfoDao.queryByuserid(userid)
    uid = 'aaaaa' if config.DEBUG_STATUS else myinfo.uid
    # config.Log.info('***********uid = %s' % uid)

    try:
        logininfo = LoginInfoDao.queryByuserid(userid)
        token = logininfo.token
        token_crypt = crypt(token)
        refreshtoken = logininfo.refreshtoken

        verifyrep = requests.post('https://%s%s' % (config.OAUTH_URL, config.OAUTH_VARIFY_URL),
                                  data={'client_id': config.CLIENT_ID, 'token': token_crypt},
                                  verify=False)
        verifymessage = json.loads(verifyrep.content)

        if 'errors_code' not in verifymessage:
            # config.Log.info('**********token = %s' % token)
            return token
        elif verifymessage['errors_code'] == 10004002 or verifymessage['errors_code'] == 10003005:

            refreshrep = requests.post('https://%s%s' % (config.OAUTH_URL, config.OAUTH_REQUIRE_TOKEN_URL),
                                       data={'grant_type': 'refresh_token', 'refresh_token': refreshtoken,
                                             'client_id': config.CLIENT_ID},
                                       verify=False
                                       )

            # newtokenmessage = json.loads(refreshrep.content)
            # newtoken = newtokenmessage['access_token']
            newtokenmessage = json.loads(refreshrep.content)
            
           

            newtoken = newtokenmessage['access_token']
            newtoken_crypt = crypt(newtoken)
            newrefreshtoken = newtokenmessage['refresh_token']


            newverifyrep = requests.post('https://%s%s' % (config.OAUTH_URL, config.OAUTH_VARIFY_URL),
                                  data={'client_id': config.CLIENT_ID, 'token': newtoken_crypt},
                                  verify=False)
            newverifymessage = json.loads(newverifyrep.content)



            if 'errors_code' not in newverifymessage:
                user_id = newverifymessage['userID']
                user_name = newverifymessage['username']
                LoginInfoDao.deleteByuserid(user_id)
                login_info = LoginInfo(uid, newtoken, newrefreshtoken, user_id, user_name, time.time())
                LoginInfoDao.add(login_info)
                config.Log.info('newtoken = %s' % newtoken)
                return newtoken
            else:
                return None
        else:
            return None

    except:
        return None
    
def refreshToken(userid):
    logininfo = LoginInfoDao.queryByuserid(userid)
    uid = 'aaaaa' if config.DEBUG_STATUS else logininfo.uid
    refreshtoken = logininfo.refreshtoken
    refreshrep = requests.post('https://%s%s' % (config.OAUTH_URL, config.OAUTH_REQUIRE_TOKEN_URL),
                               data={'grant_type': 'refresh_token', 'refresh_token': refreshtoken,
                                     'client_id': config.CLIENT_ID},
                               verify=False
                               )
    newtokenmessage = json.loads(refreshrep.content)

    newtoken = newtokenmessage['access_token']
    newtoken_crypt = crypt(newtoken)
    newrefreshtoken = newtokenmessage['refresh_token']
    
    newverifyrep = requests.post('https://%s%s' % (config.OAUTH_URL, config.OAUTH_VARIFY_URL),
                                 data={'client_id': config.CLIENT_ID, 'token': newtoken_crypt},
                                 verify=False)
    newverifymessage = json.loads(newverifyrep.content)
    
    if 'errors_code' not in newverifymessage:
        user_id = newverifymessage['userID']
        user_name = newverifymessage['username']
        LoginInfoDao.deleteByuserid(user_id)
        login_info = LoginInfo(uid, newtoken, newrefreshtoken, user_id, user_name, time.time())
        LoginInfoDao.add(login_info)
        # config.Log.info('newtoken = %s' % newtoken)
        return newtoken
    else:
        return None





