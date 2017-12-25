import subprocess
import sys
import json
import os

def getInputFileName(conf):
    return conf['Userproperty']['InputParameter']['InputFilePath'][0]['value']

def getOutputFileName(conf):
    return conf['Userproperty']['OutputParameter']['OutPutFilePath'][0]['value']

def getTransType(conf):
    return conf['Userproperty']['InputParameter']['Configuration'][0]['value']

if __name__ == '__main__':
    inputFile = sys.argv[1]

    with open(inputFile, 'r') as f:
        conf = json.load(f)

    opType = getTransType(conf)
    inImg = getInputFileName(conf)
    outImg = getOutputFileName(conf)

    cmd = './sptrans %s %s %s' % (inImg, outImg, opType)
    print('run cmd: %s' % cmd)
    cmdPro = subprocess.Popen(cmd, shell=True)
    cmdPro.wait()
