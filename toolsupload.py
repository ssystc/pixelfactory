# coding: utf-8

import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

import requests
import os


def upload(conf, tar):
    try:
        with open(conf) as f:
            jsonStr = f.read()
        url = 'http://192.168.4.221:9019/api/v1/llts/add1'
        rep = requests.post(url, data = {'config':jsonStr},files={'tar':open(tar, 'rb')})
        if rep.status_code == 200:
            print(u'上传成功 %s %s' % (conf, tar))
        else:
            print(u'上传失败 %s %s' % (conf, tar))
    except:
        print(u'上传失败 %s %s' % (conf, tar))


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print(u'需要指定目录。')
        sys.exit(-1)

    dirname = sys.argv[1].decode('gbk')

    for f in os.listdir(dirname):
        fpath = os.path.join(dirname, f)
        if os.path.isfile(fpath):
            filename, ext = os.path.splitext(fpath)
            if ext == '.gz':
                conf = '%s.%s' % (filename, 'json')
                if os.path.exists(conf):
                    upload(conf, fpath)