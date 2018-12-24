#!/usr/bin/python

"""
Tree reconfiguration algorithm
"""

import threading
import pickle
import socket
import time

import messages


# Real network interface name to send/receive packets
DEV = "wlp2s0"

# Broadcast address
BROADCAST_ADDRESS = "192.168.255.255"
PORT = 55000

# Get the address of the device. IOCTL code.
SIOCGIFADDR = 0x8915


# Main algorithm
class Node(threading.Thread):

    def __init__(self, _id):
        # Inherit methods from thread class
        super(Node, self).__init__()

        self.id = _id
        self.neighbors = {} # key = id of node, value = port (note: neighbors does not mean direct neighbors -- I think this means all nodes?)
        self.coord_so_far = id
        self.port_to_coord = None
        self.status = "IDLE"
        self.read_reply = {}
        self.set_of_ports = set()

        # Thread run status
        self.running = False

        # Create network socket
        # UDP datagram, bind to local address
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # Bind to local IPv4 address
        self.recv_socket.bind((BROADCAST_ADDRESS, PORT))
        self.send_socket = self.recv_socket
        self.iface_name = DEV

    # Main thread routine - receive packets from the socket interface
    def run(self):
        self.running = True
        while self.running:
            data, addr = self.recv_socket.recvfrom(4096)
            print(pickle.loads(data))
            print(addr)

    # Broadcast reconfig message
    def send_reconfig_message(self):
        # Create reconfig message
        reconfig_message = messages.Reconfig()
        reconfig_message.frag_id = self.id      # ???
        reconfig_message.node_list = ["foo"]         # ???

        # Send message
        self.send_socket.sendto(pickle.dumps(reconfig_message), BROADCAST_ADDRESS)

    def port_To(self, id):
        # just some way to get ids
        return self.neighbors[id]

    def Set_of_ports(self):
        # some way to get ports
        return self.neighbors.values()

    def Assign_Edge(self, port):
        # This will connect to another node and make this node its neighbor (I think?)
        # Needs to be finished
        pass

    def Get_Port(self):
        # This will need to return only direct neighbors to this node (which it has edges to)
        return self.neighbors.values()

    def Reconfig(self, node_list, frag_id): # this is an incoming message (or initiated by itself if it detects a nearby failed node)
        if self.status == "IDLE":
            # No Contention if no more ports to send reconfig (I think) -- not sure on this or on the if statement below
            if len(self.set_of_ports.remove(self.port_to_coord)) == 0:
                # broadcast No contention through self.Port_To(sender_of(Reconfig))
            self.coord_so_far = frag_id
            self.status = "WAIT"
            self.port_to_coord = self.port_To(sender_of(Reconfig)) # self.Port_To(sender_of(Reconfig)) = the port of the node that sent the Reconfig message to this node
            for port in self.set_of_ports.remove(self.port_to_coord):
                # Broadcast Reconfig(node_list.append(id), frag_id) through port

        elif self.status == "WAIT":
            e = self.Port_To(sender_of(Reconfig))
            if frag_id == Coord_so_far and e not in self.Get_Port():
                # broadcast No contention through e
                return
            if self.id in node_list:
                # broadcast No contention through e
                return
            # resolve contention between Coord_so_far and frag_id (I assume this is below? -- covered later in the paper)
            if self.Coord_so_far > frag_id or self.Coord_so_far == frag_id and id > sender.id: # sender.id is the unique ID of sender_of(Reconfig), not the port, like usual
                # broadcast Stop(self.Coord_so_far) through self.Port_To(sender_of(Reconfig))
            else:
                self.Coord_so_far = frag_id
                # broadcast Stop(frag_id) through self.Port_to_coord
                self.Port_to_coord = self.Port_To(sender_of(Reconfig)) #sender_of
            if (self.coord_so_far != frag_id) or (self.coord_so_far == frag_id and self.port_To(sender_of(Reconfig)) in self.get_Port):
                self.status = "BACKOFF"
                for port in self.set_of_ports.remove(sender_of(Reconfig)):
                    if(not self.read_reply[port]): # neither message happened
                        # broadcast Abort through port
            # start random backoff timer
        elif self.status == "BACKOFF":
            # end backoff timer
            self.status = "WAIT"
            if self.Coord_so_far == frag_id:
                for port in self.Set_of_ports.remove(sender_of(Reconfig)):
                    if not self.read_reply[port]:
                        # broadcast Reconfig(node_list, self.Coord_so_far)

    def accept_No_Content(self):
        for port in self.Set_of_ports.remove(self.Port_to_coord):
            if(self.read_reply[port] == "No contention"):
                continue
            else if(self.read_reply[port] == "Accepted"):
                # broadcast accepted through Port_to_coord
                if(self.Port_to_coord not in self.Get_Port):
                    self.Assign_Edge(self.Port_to_coord)
                break # you only need one accepted
            # if all are no_contention
            for i in self.set_of_ports.remove(self.port_to_coord):
                if i in self.get_Port and self.port_to_coord not in self.get_Port:
                    # broadcast accepted through Port_to_coord
                    self.assign_Edge(self.port_to_coord)
                else:
                    # broadcast no contention through Port_to_coord

    def stop(self, frag_id): #this is a message that will be received from port p
        if frag_id > self.coord_so_far:
            self.coord_so_far = frag_id
            # broadcast Stop(frag_id) through self.Port_to_coord
            self.port_to_coord = p # this was the port that this broadcast came from -- I think?
        if frag_id == self.Coord_so_far:
            if self.port_to_coord not in self.get_Port:
                # broadcast No_contention through self.Port_to_coord
                self.read_reply[self.port_to_coord] = "No_contention"
            else:
                # broadcast Stop(frag_id) through self.Port_to_coord
            self.port_to_coord = p
        if frag_id < self.coord_so_far:
            # broadcast Stop(self.Coord_so_far) through p

    def abort(self): #this is a message that will be received from port p
        if self.status != "BACKOFF" and self.status != "IDLE":
            self.status = "BACKOFF"
            if self.Coord_so_far != id:
                for port in self.set_of_ports.remove(sender_of(abort)):
                    if not self.read_reply[port]:
                        # broadcast Abort through port

    def no_Contention(self): #this is a message that will be received from port p
        self.read_reply[p] = "No contention"
        self.accept_No_Content() # I think it's supposed to do this with every one of these received

    def accepted(self): #this is a message that will be received from port p
        self.read_reply[p] = "Accepted"
        self.accept_No_Content() # I think it's supposed to do this with every one of these received

    def failure_Detector(self):
        # this is my creation
        # it will need to run forever and check with all direct neighbors to try and find a failure
        # when it finds one, it will initiate a Reconfig([id], id) and set self.Coord_so_far = id and self.Port_to_coord = None
        pass

    # Stop thread routine
    def quit(self):
        self.recv_socket.close()
        self.running = False


# Starting point
def main():
    # Create Node instance
    node = Node(0)
    node.daemon = True

    try:
        # Start receive thread
        node.start()

        while True:
            time.sleep(1)

    # Catch SIGINT signal
    except KeyboardInterrupt:
        # Stop the thread
        node.quit()

    return 0


if __name__ == "__main__":
    main()
