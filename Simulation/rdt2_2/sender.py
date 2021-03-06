from flask_sse import sse
from Simulation.Utils.packetID import PacketID, ResendPacketID
from Simulation.Utils.senderStates import SequencedSending, SequencedWaiting
from Simulation.Utils.constants import SEND_TIME


class Sender():
    def __init__(self, env, channel, stats):
        self.env = env
        self.states = {'waiting-0':SequencedWaiting(0), 'waiting-1':SequencedWaiting(1), 'sending-0':SequencedSending(0), 'sending-1':SequencedSending(1)}
        self.currentState = self.states['waiting-0']
        self.channel = channel
        self.stats = stats
        self.currentPacketID = 1


    def setState(self, state):
        self.currentState = self.states[state]
        statement = "{" + str(self.env.now) + "} | " + "Sender now: " + str(self.currentState)
        print(statement)
        sse.publish({"message": statement}, type='publish')


    def rdt_send(self, destination):
        if type(self.currentState) is SequencedWaiting:
            if self.currentState.seqnum == 0:
                self.setState('sending-0')
            else:
                self.setState('sending-1')
            packet=PacketID()
            packet.setSeqnum(self.currentState.seqnum)
            self.currentPacketID = packet.id
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
        # Decides what to do with ACKs received
        # if the packet is corrupted or it is the incorrect sequence number
        if packet.state is False or packet.seqnum != self.currentState.seqnum:
            #resend
            statement = "{" + str(self.env.now) + "} | " + "ACK not received correctly, resend packet"
            print(statement)
            sse.publish({"message": statement}, type='publish')
            yield self.env.process(self.rdt_resend(source, self.currentState.seqnum))
        else:
            self.stats.incrementPacketsSuccessfullySent()
            statement = "{" + str(self.env.now) + "} | " + "ACK received for packet num: " + str(packet.seqnum) + " by sender"
            print(statement)
            sse.publish({"message": statement}, type='publish')
            if self.currentState.seqnum == 0:
                self.setState('waiting-1')
            else:
                self.setState('waiting-0')
            # packet received ok, do nothing
            yield self.env.timeout(0)


    def rdt_resend(self, destination, seqnum):
        sse.publish({"packetNumber": self.currentPacketID}, type='resend')
        packet = ResendPacketID(seqnum, self.currentPacketID)
        statement = "{" + str(self.env.now) + "} | " + "Resending packet num: " + str(seqnum)
        print(statement)
        sse.publish({"message": statement}, type='publish')
        yield self.env.timeout(SEND_TIME)
        self.env.process(self.channel.send(destination, packet, self))
