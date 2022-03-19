from Simulation.SR.receiverStates import Waiting
from Simulation.SR.packet import ACK
from flask_sse import sse


DELIVER_TIME = 2    # time to deliver packet to upper layers
SEND_TIME = 2   # time to send packet back to sender - ACK or NAK


class Receiver():
    def __init__(self, env, channel, windowSize):
        self.env = env
        self.states = {'waiting':Waiting()}
        self.currentState = self.states['waiting']
        self.channel = channel
        # the sender will be expecting an ACK 0 for the first packet, if this is corrupted use 1 for the sequece # on the ACK to tell the sender something is wrong, after first packet, last ACK will be updated
        self.base = 1
        self.buffer = []
        self.windowSize = windowSize


    def setState(self, state):
        self.currentState = self.states[state]
        statement = "{" + str(self.env.now) + "} | " + "Receiver now: " + str(self.currentState)
        print(statement)
        sse.publish({"message": statement}, type='publish')



    def handle(self, packet, source):
        seqnum = packet.seqnum
        if packet.state is True and seqnum <= self.base + self.windowSize:
            if seqnum == self.base:
                statement = "{" + str(self.env.now) + "} | " + "Packet num: " + str(seqnum) + " received"
                print(statement)
                sse.publish({"message": statement}, type='publish')
                # deliver data and send ACK
                self.env.process(self.deliver_data(packet))
            else:
                statement = "{" + str(self.env.now) + "} | " + "Packet num: " + str(seqnum) + " received out of order, stored in buffer to delivered later"
                print(statement)
                sse.publish({"message": statement}, type='publish')
                self.env.process(self.buffer_data(packet))
            yield self.env.process(self.send_ACK(seqnum, source))
        elif packet.state is False:
            statement = "{" + str(self.env.now) + "} | " + "Packet num: " + str(seqnum) + " received corrupt, discarded"
            print(statement)
            sse.publish({"message": statement}, type='publish')
            yield self.env.timeout(0)
            

    def deliver_data(self, seqnum):
        # time to receive packet
        while seqnum == self.base:
            yield self.env.timeout(DELIVER_TIME)
            statement = "{" + str(self.env.now) + "} | " + "Packet num: " + str(seqnum) + " data delivered"
            print(statement)
            sse.publish({"message": statement}, type='publish')
            self.base += 1
            seqnum = self.buffer[0].seqnum


    def send_ACK(self, packet_num, source):
        statement = "{" + str(self.env.now) + "} | " + "Sending ACK for packet num: " + str(packet_num)
        print(statement)
        sse.publish({"message": statement}, type='publish')
        # time taken to send ACK
        ack = ACK(packet_num)
        yield self.env.timeout(SEND_TIME)
        self.env.process(self.channel.send(source, ack, self))


    def buffer_data(self, packet):
        pass

