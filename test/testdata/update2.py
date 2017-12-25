# coding: utf-8
import requests
import os
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')

config = {
    "trans.tar.gz":"transspimg.json",
    "trans.tar.gz":"transtiff.json"
}

url = 'http://192.168.44.111:9019/api/v1/llts/add1'

if __name__ == '__main__':
    for tar, conf in config.items():
        if not os.path.exists(tar):
            print u"文件不存在：%s" % tar
            continue
        if not os.path.exists(conf):
            print u"文件不存在：%s" % conf
            continue

        print u"注册：%s   %s" % (tar, conf)

        with open(conf) as f:
            confStr = f.read()
            rep = requests.post(url, data = {'config':confStr},files={'tar':open(tar)})
            if rep.status_code != 200:
                print u"注册请求失败: %s" % rep
            else:
                repObj = json.loads(rep.content)
                if '__CODE__' in repObj:
                    print u'注册失败：%s' % rep['__CODE__']
                else:
                    print u"注册失败"