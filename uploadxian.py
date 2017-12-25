# coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from taskserver.log import Log
from common import webos
import config
import time
from common.userserver import getTokenByuserid


# 注册log模块
config.Log = Log
token = getTokenByuserid()
dirname = time.strftime('%Y%m%d%H%M%S')
dirid = webos.createDir('Koqx+SdW7dgnuikcLmWQtjZ5OuQivSHXiOA/xBwndnPLx8Ze9r5p/ehXHjJZLHIrnFXZxSb+/Y9ApAnBwr+UKQD1c6wNfBNkqyqDGTTgq9u+soGx0R8QCUsjGC4CUyJs+ZqHNikcGy4/JeCbcmx757puWns8/j7zu3t0hN0u+uc=', 'ssy', 'cehuiZY3-14hh39mmxian', '-2')
print dirid
webos.uploadDir('Koqx+SdW7dgnuikcLmWQtjZ5OuQivSHXiOA/xBwndnPLx8Ze9r5p/ehXHjJZLHIrnFXZxSb+/Y9ApAnBwr+UKQD1c6wNfBNkqyqDGTTgq9u+soGx0R8QCUsjGC4CUyJs+ZqHNikcGy4/JeCbcmx757puWns8/j7zu3t0hN0u+uc=', dirid, 'ssy', u'/mnt/mfs-cli/cehuiData/ZY3/input')
config.Log.info('dirname is: %s' % dirname)
