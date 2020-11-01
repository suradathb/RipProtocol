from datetime import datetime


# node init save value master file
class NodeMaster:
    def __init__(self, Name, IPAddress, Port, Subnet, link):
        self.Name = Name
        self.IPAddress = IPAddress
        self.Port = Port
        self.Subnet = Subnet
        self.link = link
        self.stampdatetime = datetime.now()
