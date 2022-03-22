from random import randrange

from flask_sse import sse


class Channel():
    def __init__(self,env, errorRate, lossRate):
        self.env = env
        self.errorRate = int(errorRate/10)
        self.lossRate = int(lossRate/10)


    def send(self, destination, packet, source):
        errors = randrange(9)
        # Both data packets and ACKs can have bit errors and may get lost
        if errors < self.errorRate:
            # bit error
            statement = "{" + str(self.env.now) + "} | " + "Bit errors occured in " + packet.__class__.__name__ + " number " + str(packet.seqnum)
            print(statement)
            sse.publish({"message": statement}, type='publish')
            packet.state = False

        errors = randrange(9)
        if errors < self.lossRate:
            # lost packet
            statement = "{" + str(self.env.now) + "} | " + packet.__class__.__name__ + " number " + str(packet.seqnum) + " lost in channel"
            print(statement)
            sse.publish({"message": statement}, type='publish')
            return
        yield self.env.process(destination.handle(packet, source))
