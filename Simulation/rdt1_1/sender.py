from Simulation.rdt1_1.packet import DataPacket, ACK, NAK, ResendPacket
from Simulation.rdt1_1.senderStates import WaitingFirst, WaitingSecond, SendingFirst, SendingSecond


SEND_TIME = 2


class Sender():
    def __init__(self, env, channel):
        self.env = env
        self.sequenceNumbers = [0,1]
        self.currentSeqNum = self.sequenceNumbers[0]
        self.states = {'waiting0': WaitingFirst(), 'sending0':SendingFirst(), 'waiting1': WaitingSecond(), 'sending1':SendingSecond()}
        self.currentState = self.states['waiting0']
        self.channel = channel


    def setState(self, state):
        self.currentState = self.states[state]
        print("{" + str(self.env.now) + "} | " + "Sender now: " + str(self.currentState))


    def rdt_send(self, destination):
        if type(self.currentState) == type(self.states['waiting0']):
            self.setState('sending0')
            packet=DataPacket(0, 'data')
            print("{" + str(self.env.now) + "} | " + "Sending packet num " + str(packet.seqnum))
            yield self.env.timeout(SEND_TIME)
            self.env.process(self.channel.send(destination, packet, self))
        elif type(self.currentState) == type(self.states['waiting1']):
            self.setState('sending1')
            packet=DataPacket(1, 'data')
            print("{" + str(self.env.now) + "} | " + "Sending packet num " + str(packet.seqnum))
            yield self.env.timeout(SEND_TIME)
            self.env.process(self.channel.send(destination, packet, self))
        else:
            print("{" + str(self.env.now) + "} | " + "Sender busy please wait")


    def handle(self, packet, source):
        # Decides what to do with ACKs and NAKs received
        # if the packet is an ACK and it is not corrupted
        if type(packet) is ACK and packet.state is True:
            print("{" + str(self.env.now) + "} | " + "ACK received for packet num: " + str(packet.seqnum) + " by sender")
            if type(self.currentState) == type(self.states['sending0']):
                self.setState('waiting1')
            elif type(self.currentState) == type(self.states['sending1']):
            # if the packet is an ACK and it is not corrupted
                self.setState('waiting0')
        # if the packet received is corrupted
        elif packet.state is False:
            print("{" + str(self.env.now) + "} | " + "Response received was corrupted, resend packet: " + str(packet.seqnum))
            yield self.env.process(self.rdt_resend(source, packet.seqnum))
        # packet was received incorrectly at receiver, send again
        elif type(packet) is NAK:
            print("{" + str(self.env.now) + "} | " + "Bit errors in packet sent: " + str(packet.seqnum))
            yield self.env.process(self.rdt_resend(source, packet.seqnum))


    def rdt_resend(self, destination, seqnum):
        packet = ResendPacket(seqnum)
        print("{" + str(self.env.now) + "} | " + "Resending packet num: " + str(seqnum))
        yield self.env.timeout(SEND_TIME)
        self.env.process(self.channel.send(destination, packet, self))
