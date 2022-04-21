from flask_sse import sse
from Simulation.Utils.packet import ACK
from Simulation.Utils.constants import SEND_TIME, DELIVER_TIME


class Receiver():
    def __init__(self, env, channel, windowSize):
        self.env = env
        self.channel = channel
        # the sender will be expecting an ACK 0 for the first packet, if this is corrupted use 1 for the sequece # on the ACK to tell the sender something is wrong, after first packet, last ACK will be updated
        self.base = 1
        self.buffer = []
        self.windowSize = windowSize


    def handle(self, packet, source):
        seqnum = packet.seqnum
        # if this packet has already been received, discard and send ACK, regardless of current state as data has already been received
        if seqnum in range(self.base - self.windowSize, self.base) or seqnum in self.buffer:
            statement = "{" + str(self.env.now) + "} | " + "Packet num: " + str(seqnum) + " was already received, discarding duplicate"
            print(statement)
            sse.publish({"message": statement}, type='publish')
            yield self.env.process(self.send_ACK(seqnum, source))
        elif packet.state is True and seqnum in range(self.base, self.base + self.windowSize):
            if seqnum == self.base:
                statement = "{" + str(self.env.now) + "} | " + "Packet num: " + str(seqnum) + " received"
                print(statement)
                sse.publish({"message": statement}, type='publish')
                # deliver data and send ACK
                self.env.process(self.deliver_data(packet))
            else:
                statement = "{" + str(self.env.now) + "} | " + "Packet num: " + str(seqnum) + " received out of order, stored in buffer to be delivered later"
                print(statement)
                sse.publish({"message": statement}, type='publish')
                self.env.process(self.buffer_data(packet))
            yield self.env.process(self.send_ACK(seqnum, source))
        elif packet.state is False:
            statement = "{" + str(self.env.now) + "} | " + "Packet num: " + str(seqnum) + " received corrupt, discarded"
            print(statement)
            sse.publish({"message": statement}, type='publish')
            yield self.env.timeout(0)
            

    def deliver_data(self, packet):
        # time to receive packet
        seqnum = packet.seqnum
        # data buffered in one go, they don't have individual buffer times
        yield self.env.timeout(DELIVER_TIME)
        # if packet is in order deliver the data, and deliver any packets in buffer while they are in order
        while seqnum == self.base:
            if seqnum in self.buffer:
                self.buffer.remove(seqnum)
            sse.publish({"packetNumber": seqnum-1}, type='delivered')
            statement = "{" + str(self.env.now) + "} | " + "Packet num: " + str(seqnum) + " data delivered"
            print(statement)
            sse.publish({"message": statement}, type='publish')
            # check if there are any packets in buffer
            if len(self.buffer) != 0:
                seqnum = self.buffer[0]
            self.base += 1
        


    def send_ACK(self, packet_num, source):
        sse.publish({"packetNumber": packet_num-1}, type='ACK')
        statement = "{" + str(self.env.now) + "} | " + "Sending ACK for packet num: " + str(packet_num)
        print(statement)
        sse.publish({"message": statement}, type='publish')
        # time taken to send ACK
        ack = ACK(packet_num)
        yield self.env.timeout(SEND_TIME)
        self.env.process(self.channel.send(source, ack, self))


    def buffer_data(self, packet):
        sse.publish({"packetNumber": packet.seqnum-1}, type='buffered')
        self.buffer.append(packet.seqnum)
        self.buffer.sort()
        print(self.buffer)
        yield self.env.timeout(0)

