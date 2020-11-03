# Mode Response back to router Master Setup

class Response:
    def __init__(self, res):
        if res is None:
            self.IPAddress = str()
            self.Port = 0
            self.Data = str()
            self.received = False
        else:
            self.IPAddress = res[1][0]
            self.Port = int(res[1][1])
            self.Data = res[0].decode('utf-8')
            self.received = True
