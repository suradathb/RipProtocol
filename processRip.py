from profile import Profile_All
from setingMaster_model.node import NodeMaster
from router import RouterName
from get_arg_perser import GetArgParser
import sys
import setup


def start(profile):
    node = Profile_All(profile)
    if node is None:
        raise Exception('Profile is not found.')
    else :
        router =  RouterName(node)
        router.detail()
        router.start()

def create(setup):
    if setup.args['IPAddress'] is None:
        raise Exception('Please enter a IP Address.')
    if setup.args['Port'] is None:
        raise Exception('Please enter a Port.')

    Name = setup.args['create']
    IPAddress = setup.args['IPAddress']
    Port = int(setup.args['Port'])
    Subnet = []
    Link = []

    if setup.args['Subnet'] is not None:
        Subnet = setup.args['Subnet'].split(',')
    if setup.args['Link'] is not None:
        Link = setup.args['Link'].split(',')

    if Profile_All(Name) is None:
        node = NodeMaster(Name,IPAddress,Port,Subnet,Link)
        router = RouterName(node)
        router.detail()
        router.start()
    else:
        raise Exception('Already profile')

if __name__ == '__main__':
    setup.args = GetArgParser().parse_args()

    if setup.args['profile'] is None and setup.args['create'] is None:
        raise Exception('Please select a profile or create a profile.')
        
    if setup.args['profile'] is not None and setup.args['create'] is not None:
        raise Exception('Please select a profile or create a profile.')

    if setup.args['profile'] is not None:
        start(setup.args['profile'])

    if setup.args['create'] is not None:
        create(setup)
