import argparse


class GetArgParser():
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            '-Profile', action='store', dest='Profile', const=sum, default=max, help='Profile')
        self.parser.add_argument(
            '-Create', action='store', dest='Create', const=sum, default=max, help='Create')
        self.parser.add_argument(
            '-IP', action='store', dest='IP', const=sum, default=max, help='IP Address')
        self.parser.add_argument(
            '-Port', action='store', dest='Port', const=sum, default=max, help='Port')
        self.parser.add_argument(
            '-Subnet', action='store', dest='Subnet', const=sum, default=max, help='Subnet')
        self.parser.add_argument(
            '-Link', action='store', dest='Link', const=sum, default=max, help='Link')

    def perserargs(self):
        return vars(self.perser.perserargs())
