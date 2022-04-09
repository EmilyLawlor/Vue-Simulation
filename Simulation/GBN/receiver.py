from Simulation.GBN.receiverStates import Waiting
from Simulation.Utils.packet import ACK
from flask_sse import sse


DELIVER_TIME = 2    # time to deliver packet to upper layers
SEND_TIME = 1   # time to send packet back to sender - ACK or NAK


class Receiver():
    def __init__(self, env, channel, windowSize):
        self.env = env
        self.channel = channel
        # the sender will be expecting an ACK 0 for the first packet, if this is corrupted use 1 for the sequece # on the ACK to tell the sender something is wrong, after first packet, last ACK will be updated
        self.expectedSeqNum = 1
        self.windowSize = windowSize


    def setState(self, state):
        self.currentState = self.states[state]
        statement = "{" + str(self.env.now) + "} | " + "Receiver now: " + str(self.currentState)
        print(statement)
        sse.publish({"message": statement}, type='publish')


    def handle(self, packet, source):
        seqnum = packet.seqnum
        if packet.state is True and seqnum == self.expectedSeqNum:
            statement = "{" + str(self.env.now) + "} | " + "Packet num: " + str(seqnum) + " received"
            print(statement)
            sse.publish({"message": statement}, type='publish')
            self.expectedSeqNum += 1
            # deliver data and send ACK
            self.env.process(self.deliver_data(seqnum))
        else:
            statement = "{" + str(self.env.now) + "} | " + "Packet num: " + str(seqnum) + " received out of order or corrupt, discarded"
            print(statement)
            sse.publish({"message": statement}, type='publish')
        # Always send ACK for highest in-order packet received
        yield self.env.process(self.send_ACK(self.expectedSeqNum-1, source))


    def deliver_data(self, seqnum):
        # time to receive packet
        yield self.env.timeout(DELIVER_TIME)
        statement = "{" + str(self.env.now) + "} | " + "Packet num: " + str(seqnum) + " data delivered"
        print(statement)
        sse.publish({"message": statement}, type='publish')


    def send_ACK(self, packet_num, source):
        sse.publish({"packetNumber": packet_num-1}, type='ACK')
        statement = "{" + str(self.env.now) + "} | " + "Sending ACK for packet num: " + str(packet_num)
        print(statement)
        sse.publish({"message": statement}, type='publish')
        # time taken to send ACK
        ack = ACK(packet_num)
        yield self.env.timeout(SEND_TIME)
        self.env.process(self.channel.send(source, ack, self))
