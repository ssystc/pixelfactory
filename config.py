# coding: utf-8

# import requests
# import os
# DOCKER_SERVER_HOST = 'www.center.geovis.ai'
# DOCKER_GETUUID_BY_OWNDNS = '/api/v1/serviceManager/getServiceUidByDNS/'
# MY_DNS = 'www.factory05.geovis.ai'
# def getUUID():
#     try:
#         uuid = os.getenv('UUID_ENV')
#         if uuid == None:
#             rep = requests.get('http://%s%s%s' % (DOCKER_SERVER_HOST, DOCKER_GETUUID_BY_OWNDNS, MY_DNS))
#             uuid = rep.content
#         return uuid
#     except:
#         return None
# DOCKER_UUID = getUUID()
# DOCKER_GET_OWN_HOST_URL = '/api/v1/instance/GetHost/'
# DOCKER_GET_RELYSERVER_URL = '/api/v1/serviceManager/GetDependKey?uid=%s&type=%s&key=%s'
# get_ownhost_url = 'http://%s%s%s' % (DOCKER_SERVER_HOST, DOCKER_GET_OWN_HOST_URL, DOCKER_UUID)
# own_host = (requests.get(get_ownhost_url)).content
# MYIP = own_host.split(':')[0]
# MYPORT = own_host.split(':')[1]
#
# get_weboshost_url = 'http://%s%s' % (DOCKER_SERVER_HOST, DOCKER_GET_RELYSERVER_URL % (DOCKER_UUID, 'Data.DFS.FileManage.V1', 'HOST'))
# webos_host = requests.get(get_weboshost_url)

import socket

def GetMyIP(subnet, port=1):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect((subnet, port))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


CENTER_HOST = '192.168.48.14:9019'
LLTS_API_URL = '/api/v1/llts/api'
LLTS_LIST_URL = '/api/v1/llts/getList'
LLTS_TOOL_DETAIL = '/api/v1/llts/getData/{id}'

LLTS_TEMPORARY_HOST = '192.168.4.221:50000'
LLTS_TEMPORARY_API_URL = '/api'
LLTS_AGENT_STATISTIC = '/api/agent/stat'
LLTS_AGENT_DETAIL = '/api/agent'


TASK_SERVER_IP = GetMyIP("192.168.0.0")
TASK_SERVER_PORT = 8282
ZMQ_RECV_TIMEOUT = 3000

WEB_SERVER_IP = TASK_SERVER_IP
WEB_SERVER_PORT = 8283


# 创建的临时本地文件系统
FILE_SYSTEM_ROOT = '/mnt/mfs-cli/ssyllts/llts-data/pf2/'

# FILE_SYSTEM_ROOT = '/mnt/parastor/pftest/'


WEBOS_DIR_HOST = 'www.userdata.geovis.ai'
WEBOS_MKDIR_URL = '/user_data/favorites/addFavoritesInfo'
WEBOS_LISTDIR_URL = '/user_data/favorites/getFavoritesinfobyParentID'
WEBOS_EDITOR_URL = '/user_data/favorites/editFavoritesInfo'
WEBOS_REMOVEDIR_URL = '/user_data/favorites/removeFavoritesInfo'

METEDATA_HSOT = 'www.img.geovis.ai'
METEDATA_QUERY_BY_METAID = '/metadata-service/metadata/manage/id'

TIFF_DATA_HOST = 'www.img.geovis.ai'
TIFF_DATA_UPLOAD_URL = '/image-service/manager/uploadImage.action'
TIFF_QUERY_SLICE_URL = '/image-service/image/query/getTileServer'
TIFF_DATA_QUERY_BY_TIFFID = '/image-service/image/query/id'

IMG_SERVER_HOST = 'www.tile.geovis.ai'
IMG_SERVER_WMS_URL = '/geowebcache/service/wms?TIMESTAMP=2012-05-29%2009:45:35.0&QUERYTYPE=phasetile&service=WMS&request=GetMap&version=1.1.1&layers='
IMG_SERVER_INFO_URL = '/geowebcache/product/getinfo?productid='
IMG_SERVER_DATA_URL = '/geowebcache/product/tile?layers='

SHP_SERVER_HOST = '192.168.4.229:8509'
SHP_SERVER_UPLOAD_URL = '/uploadFiles'
SHP_WMS_HOST = '192.168.4.229:28080'
SHP_WMS_URL = '/Liu0821Upload/SearchWMS'


DATA_SERVER_HOST = 'www.text.geovis.ai'
DATA_SERVER_UPLOAD_URL = '/fileManagement/upload'
DATA_SERVER_DOWNLOAD_URL = '/fileManagement/Download'
DATA_FILE_SIZE_LIMIT = 10 * 1024 * 1024


# INPUT_DIR_NAME = u'输入目录'
# OUTPUT_DIR_NAME = u'输出目录'
# INPUT_DIRS = [u'全色', u'多光谱', u'立体象对']
INPUT_DIR_NAME = u'input'
OUTPUT_DIR_NAME = u'output'
INPUT_DIRS = [u'pan', u'mss', u'stere']
AUTO_DIRS = [u'dir_pan', u'dir_mss', u'dir_stereo']

MCOS_VISITOR = 'visitor_pixfac'
MCOS_TOKEN = 'rZa4i7yh898Dh6BV5xiSaYdvxu0nD6kIH6CZTYuYJCFF469jGhByHap2cHOvB2vA'

WEBSERVER_LOGFILE = './log/web.log'
TASKSERVER_LOGGILE = './log/wf.log'
TASKSERVER_LOGFILE_SIZE = 10
TASKSERVER_LOGFILE_COUNT = 5
TASKSERVER_LOG_FORMAT = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s'

DEFAULT_RES_CLASSIFY = u'我的资源'

PARALLEL_TEMPLATE = '%s-%s'

DB_ADDRESS = 'postgresql://postgres:postgres@192.168.4.211:5432/pf3'

# 在server启动的时候，会将log类绑定到该变量
Log = None


PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDf3qWLHkHBVC3AW/ch/dut5pd3
9E2L7l6cJ0QK/hOE9VCue8DAm0mw42631zRib38uhnG5UjYfUd4CHKPlje/RiIEn
i+/ihwcY7pNtIKLMgUcTXe4Ve7TTznlmG9R/Rvse5x5vqfRVVKMNturSlLE2nQRB
8HfTv38r/l2pnGG8gQIDAQAB
-----END PUBLIC KEY-----'''


CLIENT_ID = '200010035326904'
OAUTH_URL = 'www.user.geovis.ai'
OAUTH_LOGIN_URL = '/user_oauth/oauth-server-idp/oauth2/authorize?client_id=%s&redirect_uri=%s%s&response_type=code'
OAUTH_REQUIRE_TOKEN_URL = '/user_oauth/oauth-server-idp/oauth2/access_token'
OAUTH_VARIFY_URL = '/user_oauth/oauth-server-idp/verify2'
OAUTH_REDIRECT_URL = 'http://%s:%s/user/logincallback/' % (WEB_SERVER_IP, WEB_SERVER_PORT)
INDEX_PAGE = '/pixelfactory/views/task/index.html'
OAUTH_QUERY_USERNAME_URL = '/user_oauth/admin/privilege/operation_queryUserById?user.id=%s'
OAUTH_FACTORY_ROLE = u'像素工厂'

EP_HOST = '192.168.31.12:9090'
EP_UPLOAD_MODULEJSON_URL = '/rest/jsonfiles/analysis'

DEBUG_STATUS = False

TEZHENGDIAN_HOST = '192.168.4.221:2666'
VERSION = 0

