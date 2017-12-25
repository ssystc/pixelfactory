# coding: utf-8


class MsgException(Exception):
    
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __iter(self):
        return "<MsgException msg:%s code:%d>" % (self.msg, self.code)