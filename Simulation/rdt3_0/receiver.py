from Simulation.rdt3_0.receiverStates import Waiting
from Simulation.rdt3_0.packet import ACK
from flask_sse import sse

DELIVER_TIME = 2  # time to deliver packet to upper layers
SEND_TIME = 1   # time to send packet back to sender - ACK or NAK


class Receiver():
    def __init__(self, env, channel):
        self.env = env
        self.states = {'waiting-0':Waiting(0), 'waiting-1':Waiting(1)}
        self.currentState = self.states['waiting-0']
        self.channel = channel
        # the sender will be expecting an ACK 0 for the first packet, if this is corrupted use 1 for the sequece # on the ACK to tell the sender something is wrong, after first packet, last ACK will be updated
        self.lastACK = (1, -1)


    def setState(self, state):
        self.currentState = self.states[state]
        statement = "{" + str(self.env.now) + "} | " + "Receiver now: " + str(self.currentState)
        print(statement)
        sse.publish({"message": statement}, type='publish')


    def handle(self, packet, source):
        # packet is not corrupted
        seqnum = packet.seqnum
        if packet.state is True and seqnum == self.currentState.seqnum:
            statement = "{" + str(self.env.now) + "} | " + "Packet num: " + str(seqnum) + " received"
            print(statement)
            sse.publish({"message": statement}, type='publish')
            self.lastACK = (seqnum, packet.id)
            self.env.process(self.deliver_data(seqnum))
            yield self.env.process(self.send_ACK(self.lastACK, source))
        # packet is corrupted or incorrect seqnum
        elif packet.state is False:
            statement = "{" + str(self.env.now) + "} | " + "Data not delivered"
            print(statement)
            sse.publish({"message": statement}, type='publish')
            # do nothing
            yield self.env.timeout(0)
        elif seqnum != self.currentState.seqnum:
            statement = "{" + str(self.env.now) + "} | " + "Packet " + str(seqnum) + " was already received, deleting duplicate"
            print(statement)
            sse.publish({"message": statement}, type='publish')
            yield self.env.process(self.send_ACK(self.lastACK, source))



    def deliver_data(self, seqnum):
        # time to receive packet
        yield self.env.timeout(DELIVER_TIME)
        statement = "{" + str(self.env.now) + "} | " + "Packet num: " + str(seqnum) + " data delivered"
        print(statement)
        sse.publish({"message": statement}, type='publish')
        # Only move to next state if packet received correctly and data delivered
        if self.currentState.seqnum == 0:
            self.setState('waiting-1')
        else:
            self.setState('waiting-0')


    def send_ACK(self, packet, source):
        sse.publish({"packetNumber": packet[1]}, type='ACK')
        statement = "{" + str(self.env.now) + "} | " + "Sending ACK for packet num: " + str(packet[0])
        print(statement)
        sse.publish({"message": statement}, type='publish')
        ack = ACK(packet[0], packet[1])
        yield self.env.timeout(SEND_TIME)
        self.env.process(self.channel.send(source, ack, self))
