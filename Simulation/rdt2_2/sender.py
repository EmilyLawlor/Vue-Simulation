from Simulation.rdt2_2.packet import Packet, ResendPacket
from Simulation.rdt2_2.senderStates import Waiting, Sending


SEND_TIME = 2


class Sender():
    def __init__(self, env, channel):
        self.env = env
        self.states = {'waiting-0':Waiting(0), 'waiting-1':Waiting(1), 'sending-0':Sending(0), 'sending-1':Sending(1)}
        self.currentState = self.states['waiting-0']
        self.channel = channel
        """         # last ACK received by sender, to check for duplicates, if everything works correctly the sequence number of the first ACK should be 0, in first call of handle if packet.seqnum is equal to 1 there is a problem
                self.lastACKseqnum = 1   ----- replaced by current state sequence number"""


    def setState(self, state):
        self.currentState = self.states[state]
        print("{" + str(self.env.now) + "} | " + "Sender now: " + str(self.currentState))


    def rdt_send(self, destination):
        if type(self.currentState) is Waiting:
            if self.currentState.seqnum == 0:
                self.setState('sending-0')
            else:
                self.setState('sending-1')
            packet=Packet(self.currentState.seqnum, 'data')
            print("{" + str(self.env.now) + "} | " + "Sending packet num " + str(packet.seqnum))
            yield self.env.timeout(SEND_TIME)
            self.env.process(self.channel.send(destination, packet, self))
        else:
            print("{" + str(self.env.now) + "} | " + "Sender busy please wait")


    def handle(self, packet, source):
        # Decides what to do with ACKs received
        # if the packet is corrupted or it is the incorrect sequence number
        if packet.state is False or packet.seqnum != self.currentState.seqnum:
            #resend
            print("{" + str(self.env.now) + "} | " + "ACK not received correctly, resend packet")
            yield self.env.process(self.rdt_resend(source, self.currentState.seqnum))
        else:
            print("{" + str(self.env.now) + "} | " + "ACK received for packet num: " + str(packet.seqnum) + " by sender")
            if self.currentState.seqnum == 0:
                self.setState('waiting-1')
            else:
                self.setState('waiting-0')
            # packet received ok, do nothing
            yield self.env.timeout(0)


    def rdt_resend(self, destination, seqnum):
        packet = ResendPacket(seqnum)
        print("{" + str(self.env.now) + "} | " + "Resending packet num: " + str(seqnum))
        yield self.env.timeout(SEND_TIME)
        self.env.process(self.channel.send(destination, packet, self))
