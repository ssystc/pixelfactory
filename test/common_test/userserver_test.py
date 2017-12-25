#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append("./")

import mock
import unittest
from common import userserver
from model.logininfo import LoginInfo, LoginInfoDao
import config
import json
import requests
from taskserver.log import Log

class userserverTest(unittest.TestCase):
    config.Log = Log
    testtoken = 'vMmkWm/3ARQ2KQTQNAHtZprDzBWJhBBk3uxRwYMdj8oVCK76OvFH+wodk4AXhe2rd8AV5th8es+r/ZxOF1NV2d+eqvL8zaWIjJYVs0BQNt4lLkDfo5m2ieCcUomXjwGZzRG0ku/G8tGg3R9xWzXLSAMmrNQMPl3QEbDWgpR3tls='
    testLoginInfo = LoginInfo('testuid', 'testtoken_in_database', 'testrefreshtoken_in_database', 'testuserid', 'testusername', 0.0)
    
    # 模拟传入token可以认证成功
    class testVerifySuccess():
        content = json.dumps({
            'errors_code': 0,
            'userID': 'testuserid',
            'username': 'testusername'
        })
    
    # 模拟传入token认证显示token过期
    class testVerifyFailed():
        content = json.dumps({
            'errors_code': 10004002
        })

    # 模拟传入token认证，出现令牌过期以外的问题导致的认证失败问题
    class testVerifyFailedNoBaseExpired():
        content = json.dumps({
            'errors_code': 152525252
        })
    
    
    # 模拟刷新token接口
    class testRefreshToken():
        content = json.dumps({
            'access_token': 'testtoken_refresh',
            'refresh_token': 'testrefreshtoken_refreshtoken'
        })
    
    # 模拟refreshtoken过期导致刷新失败
    class testRefreshFailed():
        content = json.dumps({
            'errors_code': 10004002
        })
    
    def test_a_crypt(self):
        print u'**********测试解密**********'
        token_crypt = userserver.crypt(userserverTest.testtoken)
        self.assertTrue(token_crypt)
        
    def test_b_GetTokenByUserId(self):
        print u'**********测试根据UserId获取一个可用的(未过期的)token**********'
        config.DEBUG_STATUS = False

        LoginInfoDao.queryByuserid = mock.Mock(return_value=userserverTest.testLoginInfo)
        LoginInfoDao.deleteByuserid = mock.Mock(return_value=None)
        LoginInfoDao.add = mock.Mock(return_value='testuid')
        userserver.crypt = mock.Mock(return_value='test_token_crypt')
        
        # 第一次拿到token认证直接成功
        requests.post = mock.Mock(side_effect=[userserverTest.testVerifySuccess])
        token = userserver.getTokenByuserid('testuserid')
        self.assertEqual(token, 'testtoken_in_database')
        
        # 第一次的token过期，然后用refreshtoken刷新后，认证成功
        requests.post = mock.Mock(side_effect=[userserverTest.testVerifyFailed, userserverTest.testRefreshToken, userserverTest.testVerifySuccess])
        token = userserver.getTokenByuserid('testuserid')
        self.assertEqual(token, 'testtoken_refresh')
        
        # 第一次token过期，refreshtoken刷新时发现refreshtoken也过期
        requests.post = mock.Mock(side_effect=[userserverTest.testVerifyFailed, userserverTest.testRefreshFailed])
        token = userserver.getTokenByuserid('testuserid')
        self.assertEqual(token, None)

        # 第一次认证时出现除令牌过期以外的问题，导致的认证失败
        requests.post = mock.Mock(side_effect=[userserverTest.testVerifyFailedNoBaseExpired])
        token = userserver.getTokenByuserid('testuserid')
        self.assertEqual(token, None)
        
if __name__ == '__main__':
    unittest.main()
