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
dirname = time.strftime('%Y%m%d%H%M%S')
dirid = webos.createDir('200010035324693', '1215-testdelete-1', '-2')
print dirid

webos.uploadDir('200010035324693', dirid, u'/mnt/mfs-cli/cehuiData/ZY3-GC2jing/input', 'SourceImage_iFactory')
config.Log.info('dirname is: %s' % dirname)
