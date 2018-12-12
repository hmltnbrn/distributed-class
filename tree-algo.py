#
# Tree reconfiguration algorithm
#

class Node(object):

    def __init__(self, id):
        id = id
        neighbors = {} # key = id of node, value = port (note: neighbors does not mean direct neighbors -- I think this means all nodes?)
        Coord_so_far = id
        Port_to_coord = None
        status - "IDLE"
        read_reply = {}

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
            #No Contention if no more ports to send reconfig (uh?) -- should this be at the end of this if statement after the for loop or if Set_of_ports.remove(self.Port_to_coord) is empty?
            self.Coord_so_far = frag_id
            self.status = "WAIT"
            self.Port_to_coord = self.Port_To(sender_of(Reconfig)) # I'm not sure about this -- there's nothing explaining sender_of -- it may be the port of the node that sent the Reconfig to this node
            for port in self.Set_of_ports.remove(self.Port_to_coord):
                # Broadcast Reconfig(node_list.append(id), frag_id) through port
        else if(self.status == "WAIT":
            e = self.Port_To(sender_of(Reconfig))
            if(frag_id == Coord_so_far and e not in self.Get_Port()):
                #No contention through e
                self.read_reply[e] = "No_contention" # you may need to do this -- not explained or in code
                return
            if(id in node_list):
                #No contention through e
                self.read_reply[e] = "No_contention" # you may need to do this -- not explained or in code
                return
            #resolve contention between Coord_so_far and frag_id (I assume this is below? -- covered later in the paper)
            if(self.Coord_so_far > frag_id or self.Coord_so_far == frag_id and id > sender.id): # sender.id is sender_of(Reconfig) -- I'm a bit confused on this, obviously
                # broadcast Stop(self.Coord_so_far) through self.Port_To(sender_of(Reconfig))
            else:
                self.Coord_so_far = frag_id
                # broadcast Stop(frag_id) through self.Port_to_coord
                self.Port_to_coord = self.Port_To(sender_of(Reconfig)) #sender_of
            if((self.Coord_so_far != frag_id) or (self.Coord_so_far == frag_id and self.Port_To(sender_of(Reconfig)) in self.Get_Port)):
                self.status = "BACKOFF"
                for port in self.Set_of_ports.remove(sender_of(Reconfig)):
                    if(not self.read_reply[port]):
                        # broadcast Abort through port
            #start random backoff timer
        else if(self.status == "BACKOFF"):
            #end backoff timer
            self.status = "WAIT"
            if(self.Coord_so_far == frag_id):
                for port in self.Set_of_ports.remove(sender_of(Reconfig)):
                    if(not self.read_reply[port]):
                        # broadcast Reconfig(node_list, self.Coord_so_far)
    
    def Accept_No_Content():
        for port in self.Set_of_ports.remove(self.Port_to_coord):
            if(self.read_reply[port] == "Accepted")
                # send accepted through Port_to_coord
                self.read_reply[self.Port_to_coord] = "Accepted" # you may need to do this -- not explained or in code
                if(self.Port_to_coord not in self.Get_Port):
                    self.Assign_Edge(self.Port_to_coord)
                else:
                    #nothing?
                for i in self.Set_of_ports.remove(self.Port_to_coord):
                    if(i in self.Get_Port and self.Port_to_coord not in self.Get_Port):
                        #send accepted through Port_to_coord
                        self.read_reply[self.Port_to_coord] = "Accepted" # you may need to do this -- not explained or in code
                        self.Assign_Edge(self.Port_to_coord)
                    else:
                        #send no contention through Port_to_coord
                        self.read_reply[self.Port_to_coord] = "No_contention" # you may need to do this -- not explained or in code
                break #it says you only need one?
    
    def Stop(frag_id): #this is a message that will be received from port p
        if(frag_id > self.Coord_so_far):
            self.Coord_so_far = frag_id
            # broadcast Stop(frag_id) through self.Port_to_coord
            self.Port_to_coord = p # this was the port that this broadcast came from -- I think?
        if(frag_id == self.Coord_so_far):
            if(self.Port_to_coord not in self.Get_Port):
                # broadcast No_contention through self.Port_to_coord
                self.read_reply[self.Port_to_coord] = "No_contention"
            else:
                # broadcast Stop(frag_id) through self.Port_to_coord
            self.Port_to_coord = p
        if(frag_id < self.Coord_so_far):
            # broadcast Stop(self.Coord_so_far) through p
    
    def Abort(): #this is a message that will be received from port p
        if(self.status != "BACKOFF" and self.status != "IDLE"):
            self.status = "BACKOFF"
            if(self.Coord_so_far != id):
                for port in self.Set_of_ports.remove(sender_of(Abort)):
                    if(not self.read_reply[port]):
                        # broadcast Abort through port
    
    def Failure_Detector():
        #this is my creation
        #it will need to run forever and check with all direct neighbors to try and find a failure
        #when it finds one, it will initiate a Reconfig([id], id) and set self.Coord_so_far = id and self.Port_to_coord = None
