from random import randrange

class Channel():
    def __init__(self,env):
        self.env = env


    def send(self, destination, packet, source):
        errors = randrange(50)
        # all packet types can be corrupted or lost
        if ( errors % 3 == 0):
            # bit error
            print("{" + str(self.env.now) + "} | " + "Bit error occured in " + packet.__class__.__name__ + " number " + str(packet.seqnum))
            packet.state = False
        yield self.env.process(destination.handle(packet, source))
        # the version doesnt include lost packets
"""         elif (errors % 6 == 0):
            # lost packet
            return """