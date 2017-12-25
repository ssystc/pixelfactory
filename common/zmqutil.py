# coding: utf-8

import zmq
import config

def CreateReq():
    ctx = zmq.Context.instance()
    sock = ctx.socket(zmq.REQ)
    sock.setsockopt(zmq.RCVTIMEO, config.ZMQ_RECV_TIMEOUT)
    sock.connect('tcp://%s:%d' % (config.TASK_SERVER_IP, config.TASK_SERVER_PORT))
    return sock

def CreateRep():
    ctx = zmq.Context.instance()
    sock = ctx.socket(zmq.REP)
    sock.setsockopt(zmq.RCVTIMEO, config.ZMQ_RECV_TIMEOUT)
    sock.bind('tcp://*:%d' % config.TASK_SERVER_PORT)
    return sock

def RecvMsg(sock, alwaysWait=True):
    while True:
        try:
            return sock.recv_json()
        except zmq.error.Again, e:
            if not alwaysWait:
                raise e
        
def SendMsg(sock, msg):
    sock.send_json(msg)

def SendAndRecv(sock, msg, alwaysWait=True):
    SendMsg(sock, msg)
    return RecvMsg(sock, alwaysWait)