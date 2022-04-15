from flask_sse import sse
from Simulation.rdt2_0.receiverStates import Receiving, Waiting
from Simulation.Utils.constants import DELIVER_TIME, SEND_TIME
from Simulation.Utils.packet import ACK, NAK


class Receiver():
    def __init__(self, env, channel):
        self.env = env
        self.state = Waiting()
        self.states = {'waiting':Waiting(), 'receiving':Receiving()}
        self.channel = channel


    def setState(self, state):
        self.state = self.states[state]
        statement = "{" + str(self.env.now) + "} | " + "Receiver now: " + str(self.state)
        print(statement)
        sse.publish({"message": statement}, type='publish')


    def handle(self, packet, source):
        if type(self.state) is Waiting:
            self.setState('receiving')
            # packet is not corrupted
            if (packet.state):
                seqnum = packet.seqnum
                statement = "{" + str(self.env.now) + "} | " + "Packet num: " + str(seqnum) + " received"
                print(statement)
                sse.publish({"message": statement}, type='publish')
                self.env.process(self.deliver_data(seqnum))
                yield self.env.process(self.send_ACK(seqnum, source))
            # packet is corrupted
            else:
                yield self.env.process(self.send_NACK(packet.seqnum, source))
        else:
            statement = "{" + str(self.env.now) + "} | " + "Receiver busy please wait"
            print(statement)
            sse.publish({"message": statement}, type='publish')



    def deliver_data(self, seqnum):
        yield self.env.timeout(DELIVER_TIME)
        statement = "{" + str(self.env.now) + "} | " + "Packet num: " + str(seqnum) + " data delivered"
        print(statement)
        sse.publish({"message": statement}, type='publish')


    def send_ACK(self, packet_num, source):
        sse.publish({"packetNumber": packet_num-1}, type='ACK')
        statement = "{" + str(self.env.now) + "} | " + "Sending ACK for packet num: " + str(packet_num)
        print(statement)
        sse.publish({"message": statement}, type='publish')
        ack = ACK(packet_num)
        yield self.env.timeout(SEND_TIME)
        self.env.process(self.channel.send(source, ack, self))
        self.setState('waiting')


    def send_NACK(self, packet_num, source):
        sse.publish({"packetNumber": packet_num-1}, type='NAK')
        statement = "{" + str(self.env.now) + "} | " + "Sending NAK for packet num: " + str(packet_num)
        print(statement)
        sse.publish({"message": statement}, type='publish')
        yield self.env.timeout(SEND_TIME)
        self.env.process(self.channel.send(source, NAK(packet_num), self))
        self.setState('waiting')
