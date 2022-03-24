from flask_sse import sse
from Simulation.rdt2_0.packet import ACK, NAK, Packet, ResendPacket
from Simulation.rdt2_0.senderStates import Sending, Waiting

SEND_TIME = 2


class Sender():
    def __init__(self, env, channel, stats):
        self.env = env
        self.state = Waiting()
        self.states = {'waiting': Waiting(), 'sending':Sending()}
        self.channel = channel
        self.stats = stats


    def setState(self, state):
        self.state = self.states[state]
        statement = "{" + str(self.env.now) + "} | " + "Sender now: " + str(self.state)
        print(statement)
        sse.publish({"message": statement}, type='publish')


    def rdt_send(self, destination):
        if type(self.state) is Waiting:
            self.setState('sending')
            packet=Packet('data')
            statement = "{" + str(self.env.now) + "} | " + "Sending packet num " + str(packet.seqnum)
            print(statement)
            sse.publish({"message": statement}, type='publish')
            yield self.env.timeout(SEND_TIME)
            self.env.process(self.channel.send(destination, packet, self))
        else:
            statement = "{" + str(self.env.now) + "} | " + "Sender busy please wait"
            print(statement)
            sse.publish({"message": statement}, type='publish')


    def handle(self, packet, source):
        # Decides what to do with ACKs received
        if type(packet) is ACK and packet.state is not False:
            self.stats.incrementPacketsSuccessfullySent()
            statement = "{" + str(self.env.now) + "} | " + "ACK received for packet num: " + str(packet.seqnum) + " by sender"
            print(statement)
            sse.publish({"message": statement}, type='publish')
            self.setState('waiting')
            # packet was received correctly at sender do nothing
            yield self.env.timeout(0)
        elif type(packet) is NAK and packet.state is not False:
            statement = "{" + str(self.env.now) + "} | " + "Bit errors in packet: " + str(packet.seqnum)
            print(statement)
            sse.publish({"message": statement}, type='publish')
            yield self.env.process(self.rdt_resend(source, packet.seqnum))
        elif packet.state is False:
            statement = "{" + str(self.env.now) + "} | " + "Bit errors in ACK or NAK, sender has entered infinite loop"
            print(statement)
            sse.publish({"message": statement}, type='publish')


    def rdt_resend(self, destination, seqnum):
        packet = ResendPacket(seqnum)
        statement = "{" + str(self.env.now) + "} | " + "Resending packet num: " + str(seqnum)
        print(statement)
        sse.publish({"message": statement}, type='publish')
        yield self.env.timeout(SEND_TIME)
        self.env.process(self.channel.send(destination, packet, self))
