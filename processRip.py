from profile import Profile_All
from setingMaster_model.node import NodeMaster
from router import fileRouter
from get_arg_perser import GetArgParser
import sys
import setup


def start(profile):
    node_name = Profile_All(profile)
    if node_name is None:
        raise Exception('Profile is Emty.')
    else :
        router_name =  RouterName(node_name)
        router_name.detail()
        router_name.start()