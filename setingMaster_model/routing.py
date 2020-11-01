
# mode setup routing Table Master

class RoutingTable:
    def __init__(self, dest, next_hop, cost):
        self.dest = dest
        self.next_hop = next_hop
        self.cost = cost
