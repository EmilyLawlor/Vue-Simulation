from random import randrange
from Simulation.rdt3_0.packet import Packet, ResendPacket
from flask_sse import sse


SEND_TIME = 1


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
            if type(packet) is Packet or type(packet) is ResendPacket:
                sse.publish({"packetNumber": packet.id, "source": 'sender'}, type='error')
            else:
                sse.publish({"packetNumber": packet.id, "source": 'receiver'}, type='error')

        # generate new random number for losses, packet loss and bit errors are independent events
        errors = randrange(9)
        if errors < self.lossRate:
            # lost packet
            self.stats.incrementPacketsLost()
            statement = "{" + str(self.env.now) + "} | " + packet.__class__.__name__ + " number " + str(packet.seqnum) + " lost in channel"
            print(statement)
            sse.publish({"message": statement}, type='publish')
            if type(packet) is Packet or type(packet) is ResendPacket:
                sse.publish({"packetNumber": packet.id, "source": 'sender'}, type='lost')
            else:
                sse.publish({"packetNumber": packet.id, "source": 'receiver'}, type='lost')
            return

        yield self.env.timeout(SEND_TIME)
        yield self.env.process(destination.handle(packet, source))
