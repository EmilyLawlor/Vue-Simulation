from flask_sse import sse
from Simulation.rdt2_1.senderStates import (SendingFirst, SendingSecond,
                                            Waiting, WaitingFirst,
                                            WaitingSecond)
from Simulation.Utils.constants import SEND_TIME
from Simulation.Utils.packetID import ACKID, NAKID, PacketID, ResendPacketID


class Sender():
    def __init__(self, env, channel, stats):
        self.env = env
        self.states = {'waiting0': WaitingFirst(), 'sending0':SendingFirst(), 'waiting1': WaitingSecond(), 'sending1':SendingSecond()}
        self.currentState = self.states['waiting0']
        self.channel = channel
        self.stats = stats


    def setState(self, state):
        self.currentState = self.states[state]
        statement = "{" + str(self.env.now) + "} | " + "Sender now: " + str(self.currentState)
        print(statement)
        sse.publish({"message": statement}, type='publish')



    def rdt_send(self, destination):
        if issubclass(type(self.currentState), Waiting):
            if self.currentState.seqnum == 0:
                self.setState('sending0')
            else:
                self.setState('sending1')
            packet=PacketID()
            packet.setSeqnum(self.currentState.seqnum)
            sse.publish({"packetNumber": packet.id}, type='send')
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
        # Decides what to do with ACKs and NAKs received
        # if the packet is an ACK and it is not corrupted
        if type(packet) is ACKID and packet.state is True:
            self.stats.incrementPacketsSuccessfullySent()
            statement = "{" + str(self.env.now) + "} | " + "ACK received for packet num: " + str(packet.seqnum) + " by sender"
            print(statement)
            sse.publish({"message": statement}, type='publish')
            if type(self.currentState) == type(self.states['sending0']):
                self.setState('waiting1')
            elif type(self.currentState) == type(self.states['sending1']):
            # if the packet is an ACK and it is not corrupted
                self.setState('waiting0')
        # if the packet received is corrupted
        elif packet.state is False:
            statement = "{" + str(self.env.now) + "} | " + "Response received was corrupted, resend packet: " + str(packet.seqnum)
            print(statement)
            sse.publish({"message": statement}, type='publish')
            yield self.env.process(self.rdt_resend(source, packet))
        # packet was received incorrectly at receiver, send again
        elif type(packet) is NAKID:
            statement = "{" + str(self.env.now) + "} | " + "Bit errors in packet sent: " + str(packet.seqnum)
            print(statement)
            sse.publish({"message": statement}, type='publish')
            yield self.env.process(self.rdt_resend(source, packet))


    def rdt_resend(self, destination, packet):
        packet = ResendPacketID(packet.seqnum, packet.id)
        sse.publish({"packetNumber": packet.id}, type='resend')
        statement = "{" + str(self.env.now) + "} | " + "Resending packet num: " + str(packet.seqnum)
        print(statement)
        sse.publish({"message": statement}, type='publish')
        yield self.env.timeout(SEND_TIME)
        self.env.process(self.channel.send(destination, packet, self))
