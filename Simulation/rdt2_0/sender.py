from Simulation.rdt2_0.packet import Packet, ACK, NAK, ResendPacket
from Simulation.rdt2_0.senderStates import Waiting, Sending


SEND_TIME = 2


class Sender():
    def __init__(self, env, channel):
        self.env = env
        self.state = Waiting()
        self.states = {'waiting': Waiting(), 'sending':Sending()}
        self.channel = channel


    def setState(self, state):
        self.state = self.states[state]
        print("{" + str(self.env.now) + "} | " + "Sender now: " + str(self.state))


    def rdt_send(self, destination):
        if type(self.state) is Waiting:
            self.setState('sending')
            packet=Packet('data')
            print("{" + str(self.env.now) + "} | " + "Sending packet num " + str(packet.seqnum))
            yield self.env.timeout(SEND_TIME)
            self.env.process(self.channel.send(destination, packet, self))
        else:
            print("{" + str(self.env.now) + "} | " + "Sender busy please wait")


    def handle(self, packet, source):
        # Decides what to do with ACKs received
        if type(packet) is ACK and packet.state is not False:
            print("{" + str(self.env.now) + "} | " + "ACK received for packet num: " + str(packet.seqnum) + " by sender")
            self.setState('waiting')
            # packet was received correctly at sender do nothing
            yield self.env.timeout(0)
        elif type(packet) is NAK and packet.state is not False:
            print("{" + str(self.env.now) + "} | " + "Bit errors in packet: " + str(packet.seqnum))
            yield self.env.process(self.rdt_resend(source, packet.seqnum))
        elif packet.state is False:
            print("{" + str(self.env.now) + "} | " + "Bit errors in ACK or NAK, sender has entered infinite loop")


    def rdt_resend(self, destination, seqnum):
        packet = ResendPacket(seqnum)
        print("{" + str(self.env.now) + "} | " + "Resending packet num: " + str(seqnum))
        yield self.env.timeout(SEND_TIME)
        self.env.process(self.channel.send(destination, packet, self))
