from random import randrange
from Simulation.rdt2_2.packet import ACK

class Channel():
    def __init__(self,env):
        self.env = env


    def send(self, destination, packet, source):
        errors = randrange(50)
        # Both data packets and ACKs can have bit errors, no packets get lost
        if errors % 3 == 0:
            # bit error
            print("{" + str(self.env.now) + "} | " + "Bit errors occured in "  + packet.__class__.__name__ + " number " + str(packet.seqnum))
            packet.state = False
        yield self.env.process(destination.handle(packet, source))
