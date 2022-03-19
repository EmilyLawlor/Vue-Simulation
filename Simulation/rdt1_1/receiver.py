from Simulation.rdt1_1.receiverStates import WaitingFirst, WaitingSecond
from Simulation.rdt1_1.packet import ACK, NAK


DELIVER_TIME = 2    # time to deliver packet to upper layers
SEND_TIME = 2   # time to send packet back to sender - ACK or NAK


class Receiver():
    def __init__(self, env, channel):
        self.env = env
        self.states = {'waiting0': WaitingFirst(), 'waiting1': WaitingSecond()}
        self.currentState = self.states['waiting0']
        self.channel = channel


    def setState(self, state):
        if type(state) != type(self.currentState):
            self.currentState = self.states[state]
            print("{" + str(self.env.now) + "} | " + "Receiver now: " + str(self.currentState))


    def handle(self, packet, source):
        seqnum = packet.seqnum
        if type(self.currentState) == type(self.states['waiting0']):
            # packet received uncorrupted and in correct order
            if packet.state is True and seqnum == 0:
                print("{" + str(self.env.now) + "} | " + "Packet num: " + str(seqnum) + " received")
                self.env.process(self.deliver_data(seqnum))
                self.setState('waiting1')
                yield self.env.process(self.send_ACK(seqnum, source))
            # packet receive is corrupted
            elif packet.state is False:
                yield self.env.process(self.send_NAK(seqnum, source))
            # packet received uncorrupted but wrong sequence number
            elif packet.state is True and seqnum != 0:
                self.env.process(self.send_ACK(seqnum, source))
        elif type(self.currentState) == type(self.states['waiting1']):
            # packet received uncorrupted and in correct order
            if packet.state is True and seqnum == 1:
                print("{" + str(self.env.now) + "} | " + "Packet num: " + str(seqnum) + " received")
                self.env.process(self.deliver_data(seqnum))
                self.setState('waiting0')
                yield self.env.process(self.send_ACK(seqnum, source))
            # packet receive is corrupted
            elif packet.state is False:
                yield self.env.process(self.send_NAK(seqnum, source))
            # packet received uncorrupted but wrong sequence number
            elif packet.state is True and seqnum != 1:
                self.env.process(self.send_ACK(seqnum, source))
        else:
            print("{" + str(self.env.now) + "} | " + "Receiver busy please wait")


    def deliver_data(self, seqnum):
        yield self.env.timeout(DELIVER_TIME)
        print("{" + str(self.env.now) + "} | " + "Packet num: " + str(seqnum) + " data delivered")
        

    def send_ACK(self, packet_num, source):
        print("{" + str(self.env.now) + "} | " + "Sending ACK for packet num: " + str(packet_num))
        ack = ACK(packet_num)
        yield self.env.timeout(SEND_TIME)
        self.env.process(self.channel.send(source, ack, self))


    def send_NAK(self, packet_num, source):
        print("{" + str(self.env.now) + "} | " + "Sending NAK for packet num: " + str(packet_num))
        nak = NAK(packet_num)
        yield self.env.timeout(SEND_TIME)
        self.env.process(self.channel.send(source, nak, self))
