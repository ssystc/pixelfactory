# coding: utf-8

import logging
import logging.handlers

import config


def InitLogging():
    fh = logging.handlers.RotatingFileHandler(
        config.TASKSERVER_LOGGILE,
        maxBytes=config.TASKSERVER_LOGFILE_SIZE * 1024 * 1024,
        backupCount=config.TASKSERVER_LOGFILE_COUNT)
    ch = logging.StreamHandler()
    fh.setLevel(logging.INFO)
    ch.setLevel(logging.INFO)
    fmt = logging.Formatter(config.TASKSERVER_LOG_FORMAT + ' %(message)s')
    fh.setFormatter(fmt)
    ch.setFormatter(fmt)

    Logger = logging.getLogger('')
    Logger.setLevel(logging.INFO)
    Logger.addHandler(fh)
    Logger.addHandler(ch)

InitLogging()
Log = logging.getLogger('')
