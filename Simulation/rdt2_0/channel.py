from random import randrange
from flask_sse import sse
from Simulation.Utils.packet import Packet, ResendPacket


SEND_TIME = 1


class Channel():
    def __init__(self, env, errorRate, stats):
        self.env = env
        self.errorRate = int(errorRate/10)
        self.stats = stats


    def send(self, destination, packet, source):
        errors = randrange(9)
        if errors < self.errorRate:
            # bit error
            self.stats.incrementBitErrorsOccurred()
            statement = "{" + str(self.env.now) + "} | " + "Bit errors occured in " + packet.__class__.__name__ + " number " + str(packet.seqnum)
            print(statement)
            sse.publish({"message": statement}, type='publish')
            if type(packet) is Packet or type(packet) is ResendPacket:
                sse.publish({"packetNumber": packet.seqnum-1, "source": 'sender'}, type='error')
            else:
                sse.publish({"packetNumber": packet.seqnum-1, "source": 'receiver'}, type='error')
            packet.state = False

        yield self.env.timeout(SEND_TIME)
        yield self.env.process(destination.handle(packet, source))
