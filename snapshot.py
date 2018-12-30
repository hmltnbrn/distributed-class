#
# Snapshot algorithm for tree reconfiguration
#

from itertools import count # brings in function to iterate forever

class Snapshot_Node(object):

    def __init__(self):
        nodes = {} # key = id of node, value = port (all nodes in tree)
        nodes_length = len(self.nodes.values())
        prev_coord_so_far = None
        success_count = self.nodes_length
    
    def Snapshot():
        for i in count(): # iterates forever
            if self.success_count >= self.nodes_length: # if all nodes are part of the same fragment
                print "Configured Properly"
            else:
                print "Reconfiguration Underway"
            # Broadcast self.nodes.values()[i%nodes_length] # i%nodes_length should give the same remainder every time through and thus always give the same index
                if response == "error": # this was the node that failed
                    del self.nodes[self.nodes.keys()[i%nodes_length]] # removes node from nodes dictionary
                    self.nodes_length -= 1 # reduces length
                    continue # skip rest of algorithm
                if response.Coord_so_far == self.prev_coord_so_far: # if the node's fragment ID is the same as everyone elses
                    self.success_count += 1 # this will continue counting until it reaches an else below
                else:
                    prev_coord_so_far = response.Coord_so_far # if the node's fragment ID is not the same
                    self.success_count = 0
