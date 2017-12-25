

# coding: utf-8

import requests
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://192.168.44.111:9019/api/v1/llts/add1'

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(-1)

    jsonFile = sys.argv[1]
    tarFile = sys.argv[2]

    print jsonFile, tarFile

    jsonStr = None
    with open(jsonFile) as f:
        jsonStr = f.read()

    rep = requests.post(url, data = {'config':jsonStr},files={'tar':open(tarFile)})
    print rep, rep.content
