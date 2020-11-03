import argparse
class GetArgParser():
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            # '-Profile', action='store', dest='Profile', const=sum, default=max, help='Profile')
            '-Profile', action='store', dest='Profile', help='Profile')
        self.parser.add_argument(
            # '-Create', action='store', dest='Create', const=sum, default=max, help='Create')
            '-Create', action='store', dest='Create', help='Create')
        self.parser.add_argument(
            # '-IP', action='store', dest='IP', const=sum, default=max, help='IP Address')
            '-IP', action='store', dest='IP', help='IP Address')
        self.parser.add_argument(
            # '-Port', action='store', dest='Port', const=sum, default=max, help='Port')
            '-Port', action='store', dest='Port', help='Port')
        self.parser.add_argument(
            # '-Subnet', action='store', dest='Subnet', const=sum, default=max, help='Subnet')
            '-Subnet', action='store', dest='Subnet', help='Subnet')
        self.parser.add_argument(
            # '-Link', action='store', dest='Link', const=sum, default=max, help='Link')
            '-Link', action='store', dest='Link', help='Link')

    def parse_args(self):
        return vars(self.parser.parse_args())
