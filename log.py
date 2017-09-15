#!/usr/bin/env python

#########################################################################
#file name:log.py
#file description:this file creat a logger and config it,and stream handle
#and file handle to it
#author:joneww
#start date:20170823
#########################################################################

import logging
import logging.config
import sys

##########################################################################
#usage:
######import log
######logger = logging.getLogger("1")
######logger.debug("")
#########################################################################

class my_log:
    def __init__(self, pro_log_name, logger_name):
        #creat a stream handler and  config it
        stream_formatter = logging.Formatter('%(message)s')
        stream_handler = logging.StreamHandler(sys.stderr)
        stream_handler.setFormatter(stream_formatter)
        stream_handler.setLevel(logging.DEBUG)

        # creat a file handler and  config it
        file_formatter = logging.Formatter('%(asctime)s %(filename)s:%(lineno)d->%(levelname)s:%(message)s',\
                                           '%Y-%m-%d %H:%M:%S')
        file_handler = logging.FileHandler(pro_log_name)
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.DEBUG)

        #get a logger inherit root,root logger don't need any handle, if add handle to root logger, log will be both processed
        #by child logger and root logger
        #NOTSET is not the lowest level,but is the default level WARNING
        #the logger level is the first level, the handle level is the second level
        logger = logging.getLogger(logger_name)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        logger.setLevel(logging.DEBUG)



