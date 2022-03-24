from random import randrange
from Simulation.rdt3_0.packet import ACK
from flask_sse import sse

class Channel():
    def __init__(self, env, errorRate, lossRate, stats):
        self.env = env
        self.errorRate = int(errorRate/10)
        self.lossRate = int(lossRate/10)
        self.stats = stats


    def send(self, destination, packet, source):
        errors = randrange(9)
        # Both data packets and ACKs can have bit errors and may get lost
        if errors < self.errorRate:
            # bit error
            self.stats.incrementBitErrorsOccurred()
            statement = "{" + str(self.env.now) + "} | " + "Bit errors occured in " + packet.__class__.__name__ + " number " + str(packet.seqnum)
            print(statement)
            sse.publish({"message": statement}, type='publish')
            packet.state = False

        # generate new random number for losses, packet loss and bit errors are independent events
        errors = randrange(9)
        if errors < self.lossRate:
            # lost packet
            self.stats.incrementPacketsLost()
            statement = "{" + str(self.env.now) + "} | " + packet.__class__.__name__ + " number " + str(packet.seqnum) + " lost in channel"
            print(statement)
            sse.publish({"message": statement}, type='publish')
            return
        yield self.env.process(destination.handle(packet, source))
