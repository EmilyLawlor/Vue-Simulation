from random import randrange

class Channel():
    def __init__(self,env):
        self.env = env


    def send(self, destination, packet, source):
        errors = randrange(10)
        # only check creating errors in data packets not in ACKs and NACKs
        if ( errors % 3 == 0):
            # bit error
            print("{" + str(self.env.now) + "} | " + "Bit error occured in " + packet.__class__.__name__ + " number " + str(packet.seqnum))
            packet.state = False
        yield self.env.process(destination.handle(packet, source))
