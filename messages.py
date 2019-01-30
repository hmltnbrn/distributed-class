#!/usr/bin/python

"""
Message formats for the spanning-tree reconfiguration algorithm:
https://ieeexplore.ieee.org/document/287705
"""


class Reconfig:
    def __init__(self):
        self.id = "RECONFIG"
        self.node_list = list()
        self.frag_id = 0
        self.originator_ip = ""
        self.sender_ip = ""
        self.sender_id = 0
        self.dest_list = []
        self.start_ts = 0

    def __str__(self):
        out_tuple = (self.id, self.node_list, self.frag_id, self.originator_ip,
                     self.sender_ip, self.sender_id, self.dest_list)
        out_string = "MESSAGE_TYPE: %s, NODE_LIST: %s, FRAG_ID: %s, ORIG_IP: %s, " \
                     "SENDER_IP: %s, SENDER_ID: %s, DEST_LIST: %s" % out_tuple
        return out_string


class Stop:
    def __init__(self):
        self.id = "STOP"
        self.frag_id = 0
        self.originator_ip = ""
        self.sender_ip = ""
        self.sender_id = 0
        self.dest_list = []

    def __str__(self):
        out_tuple = (self.id, self.frag_id, self.originator_ip, self.sender_ip, self.sender_id, self.dest_list)
        out_string = "MESSAGE_TYPE: %s, FRAG_ID: %s, ORIG_IP: %s, SENDER_IP: %s, " \
                     "SENDER_ID: %s, DEST_LIST: %s" % out_tuple
        return out_string


class Abort:
    def __init__(self):
        self.id = "ABORT"
        self.frag_id = 0
        self.originator_ip = ""
        self.sender_ip = ""
        self.sender_id = 0
        self.dest_list = []

    def __str__(self):
        out_tuple = (self.id, self.frag_id, self.originator_ip, self.sender_ip, self.sender_id, self.dest_list)
        out_string = "MESSAGE_TYPE: %s, FRAG_ID: %s, ORIG_IP: %s, SENDER_IP: %s, " \
                     "SENDER_ID: %s, DEST_LIST: %s" % out_tuple
        return out_string


class NoContention:
    def __init__(self):
        self.id = "NO_CONTENTION"
        self.frag_id = 0
        self.originator_ip = ""
        self.sender_ip = ""
        self.sender_id = 0
        self.dest_list = []

    def __str__(self):
        out_tuple = (self.id, self.frag_id, self.originator_ip, self.sender_ip, self.sender_id, self.dest_list)
        out_string = "MESSAGE_TYPE: %s, FRAG_ID: %s, ORIG_IP: %s, SENDER_IP: %s, " \
                     "SENDER_ID: %s, DEST_LIST: %s" % out_tuple
        return out_string


class Accept:
    def __init__(self):
        self.id = "ACCEPT"
        self.frag_id = 0
        self.originator_ip = ""
        self.sender_ip = ""
        self.sender_id = 0
        self.dest_list = []

    def __str__(self):
        out_tuple = (self.id, self.frag_id, self.originator_ip, self.sender_ip, self.sender_id, self.dest_list)
        out_string = "MESSAGE_TYPE: %s, FRAG_ID: %s, ORIG_IP: %s, SENDER_IP: %s, " \
                     "SENDER_ID: %s, DEST_LIST: %s" % out_tuple
        return out_string
