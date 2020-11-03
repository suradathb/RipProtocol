import time
import socket
import os

from socket import socket as Socket
from datetime import datetime
from threading import Thread

import profile
import setup
from profile import Profile_All
from setingMaster_model.node import NodeMaster
from setingMaster_model.response import Response
from setingMaster_model.routing import RoutingTable
from setingMaster_model.request import Request


class RouterName:
    def __init__(self,node:NodeMaster):
        self.Name = node.Name
        self.IPAddress = node.IPAddress
        self.Port = node.Port
        self.Subnet = node.Subnet
        self.Link = node.link
        self.linkNode = {}
        self.tablerouting = {}
        self.linkconvert(node)
        self.subnetconvert(node)

    def linkconvert(self,node:NodeMaster):
        for Link in node.Link:
            profile_node = Profile_All(Link)
            if profile_node is not None:
                self.linkNode[profile_node.Name] = profile_node

    def subnetconvert(self, node:NodeMaster):
        for Subnet in node.Subnet:
            self.tablerouting[Subnet] = RoutingTable(Subnet, None, 1)

    def start(self):
        self.prefix_packet(setup.PREFIX_CHECK)
        self.check_link()
        Thread(target=self.serverP,args=[]).start()
        Thread(target=self.clientP,args=[]).start()
        Thread(target=self.display,args=[]).start()
        self.command()

    def command(self):
        while True:
            try:
                command_cmd = input()
                command = command_cmd.split(' ')
                command = list(filter(lambda x: x != '',command))
                if command[0].upper() == 'COST':
                    if len(command) <= 1:
                        print('Please enter an action: [reset|Link name] [Link cost]')
                    elif len(command) == 2 and command[1].upper() == 'RESET':
                        print('Please enter an action: [reset|Link name] [Link cost]')
                    elif len(command) == 3 and command[1].upper() == '':
                        print('Please enter an action: [reset|Link name] [Link cost]')
                else:
                    print('Option: cost reset|Link name [Link cost]')
            except:
                pass
    
    def serverP(self):
        server = Socket(socket.AF_INET,socket.SOCK_DGRAM)
        server.settimeout(setup.DELAY_TIMEOUT)
        server.bind((self.IPAddress,self.Port))
        while True:
            try:
                recv = server.recvfrom(setup.SIZE_BUFFER_RETURN)
                sock_Response = Response(recv)
                reply = (sock_Response.IPAddress,sock_Response.Port)
                if sock_Response.received == True:
                    self.packet_response(sock_Response.Data)
                    if sock_Response.Data.startswith(setup.PREFIX_CHECK):
                        packet = self.generate_packet(setup.PREFIX_CHECK)
                    if sock_Response.Data.startswith(setup.PREFIX_UPDATE):
                        packet = self.generate_packet(setup.PREFIX_UPDATE)
                byte = str.encode(packet)
                server.sendto(byte,reply)
                self.log_server(reply,sock_Response)
            except Exception:
                pass

    def clientP(self):
        while True:
            time.sleep(setup.DELAY_CHECK)
            self.prefix_packet(setup.PREFIX_CHECK)
            self.check_link()

    def clientSend(self,request:Request):
        sock_Response = Response(None)
        try:
            byte = str.encode(request.Data)
            client = Socket(socket.AF_INET,socket.SOCK_DGRAM)
            client.settimeout(setup.DELAY_TIMEOUT)
            client.sendto(byte,(request.IPAddress,request.Port))
            recv = client.recvfrom(setup.SIZE_BUFFER_RETURN)
            sock_Response = Response(recv)
            sock_Response.received = True
            self.log_client(request,sock_Response)
        except Exception as ex:
            sock_Response.IPAddress = request.IPAddress
            sock_Response.Port = request.Port
            sock_Response.received = False
            sock_Response.Data = str(ex)
        return sock_Response

    def prefix_packet(self, Data):
        packet = self.generate_packet(Data)
        for linkNode in self.linkNode.values():
            sock_request = Request(linkNode.IPAddress, linkNode.Port, packet)
            sock_Response = self.clientSend(sock_request)
            if sock_Response.received == True:
                self.packet_response(sock_Response.Data)
    
    def packet_response(self, Data):
        split_line = Data.splitlines()
        header = split_line[0].split("|")
        node = self.get_node_detail(header)

        if self.linkNode.__contains__(node.Name):
            self.linkNode[node.Name].latest_received = datetime.now()
        else:
            self.linkNode[node.Name] = node

        if len(split_line) >= 2:
            iterline = iter(split_line)
            next(iterline)
            recv_routing_table = self.get_routing_table(node, iterline)
            self.update_routing(node, recv_routing_table)
    
    def update_routing(self, node: NodeMaster, recv_routing_table):
        for recv_routing in recv_routing_table:
            if self.tablerouting.__contains__(recv_routing.dest):
                current_routing = self.tablerouting[recv_routing.dest]

                if current_routing.cost > recv_routing.cost + 1:
                    current_routing.next_hop = node.Name
                    current_routing.cost = recv_routing.cost + 1
                elif recv_routing.cost + 1 > current_routing.cost and node.Name == current_routing.next_hop:
                    current_routing.cost = recv_routing.cost + 1
            else:
                recv_routing.next_hop = node.Name
                recv_routing.cost += 1
                self.tablerouting[recv_routing.dest] = recv_routing
    
    def get_routing_table(self, node: NodeMaster, array_row):
        recv_routing_table = []
        for row in array_row:
            array_data = row.split('|')
            routing = RoutingTable(
                str(array_data[0]),
                str(array_data[1]),
                int(array_data[2])
            )
            recv_routing_table.append(routing)
        return recv_routing_table
    
    def get_node_detail(self, array_data):
        Name = array_data[1]
        IPAddress = array_data[2].split(':')[0]
        Port = int(array_data[2].split(':')[1])
        return NodeMaster(Name, IPAddress, Port, [], [])

    def check_link(self):
        list_remove_node = []
        list_remove_table = []
        for linkNode in self.linkNode.values():
            if int((datetime.now()-linkNode.latest_received).seconds) >= setup.DELAY_KEEPALIVE:
                list_remove_node.append(linkNode.Name)
                for key in self.tablerouting.keys():
                    if self.tablerouting[key].next_hop == linkNode.Name:
                        list_remove_table.append(key)
                break
        for key in self.tablerouting.keys():
            if self.tablerouting[key].cost >= setup.MAX_HOPS:
                if key not in list_remove_table:
                    list_remove_table.append(key)

        self.remove_node(list_remove_node)
        self.remove_table(list_remove_table)
    
    def remove_node(self,list_remove_node):
        for key in list_remove_node:
            del self.linkNode[key]
    
    def remove_table(self,list_remove_table):
        for key in list_remove_table:
            del self.tablerouting[key]
    
    def log_client(self, Request, Response):
        if setup.ENABLE_PRINT_LOG == True:
            log_request = (Request.IPAddress, Request.Port)
            log_response = (Response.IPAddress, Response.Port)
            print("[SENT] --> %s:%s" % log_request)
            print("[RECV] <-- %s:%s" % log_response)
            print("[RECV] <-- %s" % Response.Data)
        
    def log_server(self, reply, Response):
        if setup.ENABLE_PRINT_LOG == True:
            log_response = (Response.IPAddress, Response.Port)
            print("[RECV] <-- %s:%s" % log_response)
            print("[SENT] --> %s:%s" % reply)
    
    def generate_packet(self, prefix):
        list_packet = []
        header = "%s|%s|%s:%s" % (prefix,
                                  self.Name,
                                  self.IPAddress,
                                  self.Port)
        list_packet.append(header)
        for routing in self.tablerouting.values():
            if routing.cost <= setup.MAX_HOPS:
                sub_packet = "%s|%s|%s" % (
                    str(routing.dest),
                    str(routing.next_hop),
                    str(routing.cost)
                )
                list_packet.append(sub_packet)
        packet = '\n'.join(list_packet)
        return packet
    
    def detail(self):
        print("================================================")
        print("Router Name\t:", self.Name)
        print("IP Address\t:", self.IPAddress)
        print("Port\t\t:", self.Port)
        print("Subnet\t\t:", self.Subnet)
        print("Link\t\t:", self.Link)
        print("================================================")

    def display(self):
        while True:
            time.sleep(1)
            os.system("cls")
            print("|=================|=============|===========|")
            print("| NAME %s|     %s |" % (
                str(self.Name).ljust(11),
                (str(self.IPAddress) + ":" + str(self.Port)).ljust(19))
            )
            print("|=================|=============|===========|")
            print("|   Destination   | Next Router | Link Cost |")
            print("|=================|=============|===========|")
            for routing in self.tablerouting.values():
                print("|%s|%s|%s|" % (
                    str(routing.dest).ljust(17),
                    str(routing.next_hop).ljust(13),
                    str(routing.cost).ljust(11))
                )

            print("|=================|=============|===========|")
            for linkNode in self.linkNode.values():
                print("NODE=%s IP=[%s:%s] LastUpdate=%d seconds ago" %
                      (linkNode.Name, linkNode.IPAddress, linkNode.Port, (datetime.now()-linkNode.latest_received).seconds))