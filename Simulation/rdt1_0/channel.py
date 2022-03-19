class Channel():
    def __init__(self,env):
        self.env = env


    def send(self, destination, packet, source):
        yield self.env.process(destination.handle(packet, source))