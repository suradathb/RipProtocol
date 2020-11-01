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
        self.name = node.Name
        self.IPAddress = node.IPAddress
        self.Port = node.Port
        self.Subnet = node.Subnet
        self.Link = node.link