#!/usr/bin/python

"""
Tree reconfiguration algorithm
"""

from fcntl import ioctl
import threading
import random
import pickle
import socket
import struct
import time

import messages


# Real network interface name to send/receive packets
DEV = "eth0"

# Broadcast address
BROADCAST_ADDRESS = "10.0.0.255"
PORT = 55000

# Get the address from the device. IOCTL code.
SIOCGIFADDR = 0x8915

# Backoff range, seconds
MIN_BACKOFF = 0.1
MAX_BACKOFF = 2


# Get ipv4 address from the interface
def get_ipv4_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        ipv4_addr = ioctl(s.fileno(), SIOCGIFADDR, struct.pack('256s', DEV[:15]))[20:24]
    except IOError:
        print("No IPv4 address assigned!")
        return None

    return socket.inet_ntoa(ipv4_addr)


# Main algorithm
class Node(threading.Thread):

    def __init__(self, _id):
        # Inherit methods from thread class
        super(Node, self).__init__()
        self.id = _id
        self.ip = get_ipv4_address()
        # self.neighbors = {} # key = id of node, value = port (note: neighbors does not mean direct neighbors -- I think this means all nodes?)
        self.neighbors = []
        self.coord_so_far = 0
        self.port_to_coord = ""
        self.status = "IDLE"
        self.read_reply = {}
        self.edges = []
        # self.set_of_ports = set()
        # Maintain ID list of already re-broadcasted reconfig messages, to send no_contention messages
        self.processed_reconfig_ids = []

        # Thread run status
        self.running = False

        # Create network socket
        # UDP datagram, bind to local address
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # allow multicast ipv4
        # allow socket reuse - to send initial reconfig message
        self.recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind to local IPv4 address
        self.recv_socket.bind((BROADCAST_ADDRESS, PORT))
        self.send_socket = self.recv_socket

    # Main thread routine - receive packets from the socket interface
    def run(self):
        self.running = True
        while self.running:
            data, addr = self.recv_socket.recvfrom(4096)

            # De-serialize the data
            message = pickle.loads(data)

            # Filter out messages by destination
            if self.ip == message.sender_ip:
                continue

            if (self.ip in message.dest_list) or (message.dest_list == []):

                print("RECEIVED MESSAGE: %s" % message)
                print("FROM ADDRESS: %s" % addr[0])

                print("NEIGHBORS: %s" % self.neighbors)
                print("EDGES: %s" % self.edges)
                print("-" * 50)

                # Update the neighbors list
                if addr[0] not in self.neighbors:
                    self.neighbors.append(addr[0])
                # Fill in read-reply dict
                if addr[0] not in self.read_reply:
                    self.read_reply[addr[0]] = ""

                # Handle incoming messages
                if message.id == "RECONFIG":
                    self.process_reconfig(message)
                elif message.id == "STOP":
                    self.process_stop(message)
                elif message.id == "ABORT":
                    self.process_abort(message)
                elif message.id == "NO_CONTENTION":
                    self.process_no_contention(message)
                elif message.id == "ACCEPT":
                    self.process_accept(message)

    # Broadcast reconfig message
    def send_reconfig_message(self):
        # Create reconfig message
        reconfig_message = messages.Reconfig()
        reconfig_message.frag_id = self.id
        reconfig_message.node_list = []         # ???
        reconfig_message.originator_ip = self.ip
        reconfig_message.sender_ip = self.ip
        reconfig_message.sender_id = self.id

        # Send message
        self.send_socket.sendto(pickle.dumps(reconfig_message), (BROADCAST_ADDRESS, PORT))
        self.processed_reconfig_ids.append(reconfig_message.frag_id)

    # Not needed for now
    # def port_To(self, id):
    #     # just some way to get ids
    #     return self.neighbors[id]
    #
    # def Set_of_ports(self):
    #     # some way to get ports
    #     return self.neighbors.values()
    #
    # def Assign_Edge(self, port):
    #     # This will connect to another node and make this node its neighbor (I think?)
    #     # Needs to be finished
    #     pass
    #
    # def Get_Port(self):
    #     # This will need to return only direct neighbors to this node (which it has edges to)
    #     return self.neighbors.values()

    def assign_edge(self, port):
        if port not in self.edges:
            self.edges.append(port)

    # Process the incoming reconfig message
    def process_reconfig(self, reconfig_message): # this is an incoming message (or initiated by itself if it detects a nearby failed node)
        no_contention_message = messages.NoContention()
        no_contention_message.frag_id = reconfig_message.frag_id
        no_contention_message.originator_ip = reconfig_message.originator_ip
        no_contention_message.sender_ip = self.ip
        no_contention_message.sender_id = self.id

        if self.status == "IDLE":
            # No Contention if no more ports to send reconfig (I think) -- not sure on this or on the if statement below
            # Send no_contention message if the node has already re-broadcasted this reconfig_message
            # if len(self.set_of_ports.remove(self.port_to_coord)) == 0:
            if reconfig_message.frag_id in self.processed_reconfig_ids:
                # broadcast No contention through self.Port_To(sender_of(Reconfig))
                for port in self.neighbors:
                    if port != reconfig_message.sender_ip:
                        no_contention_message.dest_list.append(port)
                self.send_socket.sendto(pickle.dumps(no_contention_message), (BROADCAST_ADDRESS, PORT))
                # return 0    # ???

            self.coord_so_far = reconfig_message.frag_id
            self.status = "WAIT"
            # self.port_to_coord = self.port_To(sender_of(Reconfig)) # self.Port_To(sender_of(Reconfig)) = the port of the node that sent the Reconfig message to this node
            self.port_to_coord = reconfig_message.sender_ip

            # for port in self.set_of_ports.remove(self.port_to_coord):
            #     # Broadcast Reconfig(node_list.append(id), frag_id) through port
            # Broadcast reconfig message further
            reconfig_message.sender_ip = self.ip
            reconfig_message.sender_id = self.id
            reconfig_message.dest_list = []
            for port in self.neighbors:
                if port != self.port_to_coord:
                    reconfig_message.dest_list.append(port)
            self.send_socket.sendto(pickle.dumps(reconfig_message), (BROADCAST_ADDRESS, PORT))

        elif self.status == "WAIT":
            # e = self.Port_To(sender_of(Reconfig))
            e = reconfig_message.originator_ip

            # if reconfig_message.frag_id == self.coord_so_far and e not in self.Get_Port():
            if reconfig_message.frag_id == self.coord_so_far and e not in self.neighbors:
                # broadcast No contention through e
                self.send_socket.sendto(pickle.dumps(no_contention_message), (BROADCAST_ADDRESS, PORT))
                # return 0    # ???

            # How is node_list different from neighbors?
            # if self.id in node_list:
            #     # broadcast No contention through e
            #     return

            stop_message = messages.Stop()
            stop_message.originator_ip = reconfig_message.originator_ip
            stop_message.sender_id = self.id
            stop_message.frag_id = reconfig_message.frag_id
            stop_message.sender_ip = self.ip
            # resolve contention between Coord_so_far and frag_id (I assume this is below? -- covered later in the paper)
            if self.coord_so_far > reconfig_message.frag_id or self.coord_so_far == reconfig_message.frag_id and \
                    self.id > reconfig_message.sender_id:    # sender.id is the unique ID of sender_of(Reconfig), not the port, like usual
                # broadcast Stop(self.Coord_so_far) through self.Port_To(sender_of(Reconfig))
                stop_message.dest_list.append(reconfig_message.sender_ip)
                self.send_socket.sendto(pickle.dumps(stop_message), (BROADCAST_ADDRESS, PORT))
                # return 0    # ???

            else:
                self.coord_so_far = reconfig_message.frag_id
                # # broadcast Stop(frag_id) through self.Port_to_coord
                # self.port_to_coord = self.Port_To(sender_of(Reconfig)) #sender_of
                self.port_to_coord = reconfig_message.sender_ip
                # Broadcast Stop(frag_id) message
                stop_message.dest_list.append(reconfig_message.sender_ip)
                self.send_socket.sendto(pickle.dumps(stop_message), (BROADCAST_ADDRESS, PORT))
                # return 0    # ???

            abort_message = messages.Abort()
            abort_message.sender_ip = self.ip
            abort_message.frag_id = reconfig_message.frag_id
            abort_message.sender_id = self.id
            abort_message.originator_ip = reconfig_message.originator_ip
            # if (self.coord_so_far != reconfig_message.frag_id) or (self.coord_so_far == reconfig_message.frag_id and
            # self.port_To(sender_of(Reconfig)) in self.get_Port):
            # if (self.coord_so_far != reconfig_message.frag_id) or (self.coord_so_far == reconfig_message.frag_id
            #                                                        and reconfig_message.sender_ip in self.neighbors):
            if self.coord_so_far != reconfig_message.frag_id:

                self.status = "BACKOFF"
                # for port in self.set_of_ports.remove(sender_of(Reconfig)):
                #     if not self.read_reply[port]: # neither message happened
                #       # broadcast Abort through port
                # Broadcast about message
                for port in self.neighbors:
                    if port != reconfig_message.sender_ip:
                        abort_message.dest_list.append(port)
                self.send_socket.sendto(pickle.dumps(abort_message), (BROADCAST_ADDRESS, PORT))

            # start random backoff timer
            time.sleep(random.uniform(MIN_BACKOFF, MAX_BACKOFF))

        elif self.status == "BACKOFF":
            # end backoff timer
            self.status = "WAIT"
            if self.coord_so_far == reconfig_message.frag_id:
                # for port in self.Set_of_ports.remove(sender_of(Reconfig)):
                #     if not self.read_reply[port]:
                #         # broadcast Reconfig(node_list, self.Coord_so_far)
                # Broadcast reconfig message further
                reconfig_message.sender_ip = self.ip
                reconfig_message.sender_id = self.id
                reconfig_message.dest_list = []
                for port in self.neighbors:
                    if port != reconfig_message.sender_ip:
                        reconfig_message.dest_list.append(port)
                self.send_socket.sendto(pickle.dumps(reconfig_message), (BROADCAST_ADDRESS, PORT))

    def accept_no_content(self, frag_id, originator_ip):
        # for port in self.Set_of_ports.remove(self.Port_to_coord):
        ports_list = list(self.neighbors)
        if self.port_to_coord in ports_list:
            ports_list.remove(self.port_to_coord)

        accept_message = messages.Accept()
        accept_message.originator_ip = originator_ip
        accept_message.frag_id = frag_id
        accept_message.sender_id = self.id
        accept_message.sender_ip = self.ip

        accept_message.dest_list = []
        no_contention_message = messages.NoContention()
        no_contention_message.frag_id = frag_id
        no_contention_message.originator_ip = originator_ip
        no_contention_message.sender_ip = self.ip
        no_contention_message.sender_id = self.id

        for port in ports_list:
            if self.read_reply[port] == "No contention":
                continue

            elif self.read_reply[port] == "Accepted":
                # broadcast accepted through Port_to_coord
                accept_message.dest_list.append(port)
                # if self.port_to_coord not in self.neighbors:
                if self.port_to_coord not in ports_list:
                    # self.Assign_Edge(self.Port_to_coord)
                    self.assign_edge(self.port_to_coord)
                    pass

                break    # you only need one accepted

        # self.send_socket.sendto(pickle.dumps(accept_message), (BROADCAST_ADDRESS, PORT))

            # if all are no_contention
            # for i in self.set_of_ports.remove(self.port_to_coord):
            for i in ports_list:
                # if i in self.get_Port and self.port_to_coord not in self.get_Port:
                # if i in self.neighbors and self.port_to_coord not in self.neighbors:
                if self.port_to_coord not in ports_list:
                    # broadcast accepted through Port_to_coord
                    # self.assign_Edge(self.port_to_coord)  ???
                    self.assign_edge(self.port_to_coord)
                    accept_message.dest_list.append(i)
                    # self.send_socket.sendto(pickle.dumps(accept_message), (i, PORT))

                else:
                    # broadcast no contention through Port_to_coord
                    no_contention_message.dest_list.append(self.port_to_coord)
                    # self.send_socket.sendto(pickle.dumps(no_contention_message), (i, PORT))

        # if not accept_message.dest_list:
        #     if no_contention_message.dest_list:
        #         self.send_socket.sendto(pickle.dumps(no_contention_message), (BROADCAST_ADDRESS, PORT))
        # else:
        #     self.send_socket.sendto(pickle.dumps(accept_message), (BROADCAST_ADDRESS, PORT))
        if accept_message.dest_list:
            self.send_socket.sendto(pickle.dumps(accept_message), (BROADCAST_ADDRESS, PORT))

    def process_stop(self, stop_message):   # this is a message that will be received from port p
        if stop_message.frag_id > self.coord_so_far:
            self.coord_so_far = stop_message.frag_id
            # broadcast Stop(frag_id) through self.Port_to_coord
            # self.port_to_coord = p # this was the port that this broadcast came from -- I think?
            self.port_to_coord = stop_message.sender_ip
            # Broadcast stop message
            self.send_socket.sendto(pickle.dumps(stop_message), (BROADCAST_ADDRESS, PORT))

        if stop_message.frag_id == self.coord_so_far:
            # if self.port_to_coord not in self.get_Port:
            if self.port_to_coord not in self.neighbors:
                # broadcast No_contention through self.Port_to_coord
                self.read_reply[self.port_to_coord] = "No_contention"
                no_contention_message = messages.NoContention()
                no_contention_message.frag_id = stop_message.frag_id
                no_contention_message.originator_ip = stop_message.originator_ip
                no_contention_message.sender_ip = self.ip
                no_contention_message.sender_id = self.id
                no_contention_message.dest_list.append(self.port_to_coord)
                self.send_socket.sendto(pickle.dumps(no_contention_message), (BROADCAST_ADDRESS, PORT))

            else:
                # broadcast Stop(frag_id) through self.Port_to_coord
                # Broadcast stop message
                stop_message.dest_list = [self.port_to_coord]
                self.send_socket.sendto(pickle.dumps(stop_message), (BROADCAST_ADDRESS, PORT))

            self.port_to_coord = stop_message.sender_ip

        if stop_message.frag_id < self.coord_so_far:
            # broadcast Stop(self.Coord_so_far) through p
            # Broadcast stop message
            stop_message.dest_list = [stop_message.sender_ip]
            self.send_socket.sendto(pickle.dumps(stop_message), (BROADCAST_ADDRESS, PORT))

    def process_abort(self, abort_message):    # this is a message that will be received from port p
        if self.status != "BACKOFF" and self.status != "IDLE":
            self.status = "BACKOFF"
            if self.coord_so_far != abort_message.id:
                # for port in self.set_of_ports.remove(sender_of(abort)):
                #     if not self.read_reply[port]:
                        # broadcast Abort through port
                abort_message.sender_ip = self.ip
                abort_message.dest_list = []
                for port in self.neighbors:
                    if port != abort_message.sender_ip:
                        abort_message.dest_list.append(port)
                self.send_socket.sendto(pickle.dumps(abort_message), (BROADCAST_ADDRESS, PORT))

    def process_no_contention(self, no_contention_message):    # this is a message that will be received from port p
        self.read_reply[no_contention_message.sender_ip] = "No contention"
        self.accept_no_content(no_contention_message.frag_id, no_contention_message.originator_ip)    # I think it's supposed to do this with every one of these received

    def process_accept(self, accept_message):    # this is a message that will be received from port p
        self.read_reply[accept_message.sender_ip] = "Accepted"
        self.accept_no_content(accept_message.frag_id, accept_message.originator_ip)    # I think it's supposed to do this with every one of these received

    def failure_detector(self):
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
    node = Node(random.randrange(1000))
    node.daemon = True

    try:
        # Start receive thread
        node.start()
        print("Node started with ID: %s", node.id)
        # Main thread
        while True:
            time.sleep(1)

    # Catch SIGINT signal
    except KeyboardInterrupt:
        # Stop the thread
        node.quit()

    return 0


if __name__ == "__main__":
    main()
