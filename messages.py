#!/usr/bin/python

"""
Message formats for the spanning-tree reconfiguration algorithm:
https://ieeexplore.ieee.org/document/287705
"""


class Reconfig:
    _id = "RECONFIG"

    def __init__(self):
        self.node_list = list()
        self.frag_id = 0

    def __str__(self):
        out_tuple = (self._id, self.node_list, self.frag_id)
        out_string = "MESSAGE_TYPE: %s, NODE_LIST: %s, FRAG_ID: %s" % out_tuple
        return out_string
