from setingMaster_model.node import NodeMaster

node_list = {}

# ====================================
# Node A Detail
# ====================================
node_list["A"] = {
    "Subnet": ["192.168.1.0/24", "192.168.4.0/24"],
    "link": ["B", "D"],
    "IPAddress": "127.0.0.1",
    "Port": 8101,
}

# ====================================
# Node B Detail
# ====================================
node_list["B"] = {
    "Subnet": ["192.168.2.0/24"],
    "link": ["A", "C", "D"],
    "IPAddress": "127.0.0.1",
    "Port": 8102,
}

# ====================================
# Node C Detail
# ====================================
node_list["C"] = {
    "Subnet": ["192.168.2.0/24", "192.168.3.0/24"],
    "link": ["B", "F"],
    "IPAddress": "127.0.0.1",
    "Port": 8103,
}

# ====================================
# Node D Detail
# ====================================
node_list["D"] = {
    "Subnet": ["192.168.4.0/24"],
    "link": ["A", "B", "E"],
    "IPAddress": "127.0.0.1",
    "Port": 8104,
}

# ====================================
# Node E Detail
# ====================================
node_list["E"] = {
    "Subnet": ["192.168.6.0/24"],
    "link": ["D", "F"],
    "IPAddress": "127.0.0.1",
    "Port": 8105,
}

# ====================================
# Node F Detail
# ====================================
node_list["F"] = {
    "Subnet": ["192.168.5.0/24"],
    "link": ["C", "E"],
    "IPAddress": "127.0.0.1",
    "Port": 8106,
}

# ====================================
# Node G Detail
# ====================================
node_list["G"] = {
    "Subnet": ["192.168.5.0/24"],
    "link": ["E"],
    "IPAddress": "127.0.0.1",
    "port": 8107,
}


def Profile_All(name):
    if node_list.__contains__(name):
        node_profile = node_list[name]
        return NodeMaster(
            name,
            node_profile["IPAddressAddress"],
            node_profile["Port"],
            node_profile["Subnet"],
            node_profile["link"]
        )
    else:
        return None
