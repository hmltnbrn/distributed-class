#
# Tree reconfiguration algorithm
#

class Node(object):

    def __init__(self, id):
        id = id
        neighbors = {} # key = id of node, value = port (note: neighbors does not mean direct neighbors)
        Coord_so_far = None
        Port_to_coord = None
        status - "IDLE"
        read_reply = []

    def Port_To(id):
        return neighbors[id]

    def Set_of_ports():
        return neighbors.values()

    def Assign_Edge(port):
        # This will connect to another node and make this node its neighbor (I think?)
        # Needs to be finished
        pass

    def Get_Port():
        # This will need to return only direct neighbors to this node (which it has edges to)
        return neighbors.values()

    def Reconfig(node_list, frag_id): # this is an imcoming message
        if(self.status == "IDLE"):
            #No Contention
            self.Coord_so_far = frag_id
            self.status = "WAIT"
            self.Port_to_coord = self.Port_To(frag_id) # I'm not sure about this -- there's nothing explaining sender_of -- it may be the port of the node that sent the Reconfig to this node
            for port in self.Set_of_ports().remove(self.Port_to_coord):
                pass
                # Broadcast Reconfig(node_list.append(id), frag_id)
        else:
            e = self.Port_To(frag_id)
            if(frag_id == Coord_so_far and e is not in self.Get_Port()):
                #No contention
                return
            if(id is in node_list):
                #No contention
                return
            #resolve contention between Coord_so_far and frag_id
    
    def Accept_No_Content():
        for port in self.Set_of_ports.remove(self.Port_to_coord):
            # Broadcast
                if (response is "accepted"):
                    # send accepted through Port_to_coord
                    if(self.Port_to_coord is not in self.Get_Port):
                        self.Assign_Edge(self.Port_to_coord)
                    else:
                        #nothing?
                    for i in self.Set_of_ports.remove(self.Port_to_coord):
                        if(i in self.Get_Port and self.Port_to_coord not in self.Get_Port):
                            #send accepted through Port_to_coord
                            self.Assign_Edge(self.Port_to_coord)
                        else:
                            #send no contention through Port_to_coord
