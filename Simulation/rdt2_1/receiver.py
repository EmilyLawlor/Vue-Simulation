from flask_sse import sse
from Simulation.Utils.receiverStates import SequencedWaiting
from Simulation.Utils.constants import DELIVER_TIME, SEND_TIME
from Simulation.Utils.packetID import ACKID, NAKID


class Receiver():
    def __init__(self, env, channel):
        self.env = env
        self.states = {'waiting-0':SequencedWaiting(0), 'waiting-1':SequencedWaiting(1)}
        self.currentState = self.states['waiting-0']
        self.channel = channel


    def setState(self, state):
        if type(state) != type(self.currentState):
            self.currentState = self.states[state]
            statement = "{" + str(self.env.now) + "} | " + "Receiver now: " + str(self.currentState)
            print(statement)
            sse.publish({"message": statement}, type='publish')


    def handle(self, packet, source):
        seqnum = packet.seqnum
        if type(self.currentState) == type(self.states['waiting-0']):
            # packet received uncorrupted and in correct order
            if packet.state is True and seqnum == 0:
                statement = "{" + str(self.env.now) + "} | " + "Packet num: " + str(seqnum) + " received"
                print(statement)
                sse.publish({"message": statement}, type='publish')
                self.env.process(self.deliver_data(seqnum))
                self.setState('waiting-1')
                yield self.env.process(self.send_ACK(packet, source))
            # packet receive is corrupted
            elif packet.state is False:
                yield self.env.process(self.send_NAK(packet, source))
            # packet received uncorrupted but wrong sequence number
            elif packet.state is True and seqnum != 0:
                self.env.process(self.send_ACK(packet, source))
        elif type(self.currentState) == type(self.states['waiting-1']):
            # packet received uncorrupted and in correct order
            if packet.state is True and seqnum == 1:
                statement = "{" + str(self.env.now) + "} | " + "Packet num: " + str(seqnum) + " received"
                print(statement)
                sse.publish({"message": statement}, type='publish')
                self.env.process(self.deliver_data(seqnum))
                self.setState('waiting-0')
                yield self.env.process(self.send_ACK(packet, source))
            # packet receive is corrupted
            elif packet.state is False:
                yield self.env.process(self.send_NAK(packet, source))
            # packet received uncorrupted but wrong sequence number
            elif packet.state is True and seqnum != 1:
                self.env.process(self.send_ACK(packet, source))
        else:
            statement = "{" + str(self.env.now) + "} | " + "Receiver busy please wait"
            print(statement)
            sse.publish({"message": statement}, type='publish')


    def deliver_data(self, seqnum):
        yield self.env.timeout(DELIVER_TIME)
        statement = "{" + str(self.env.now) + "} | " + "Packet num: " + str(seqnum) + " data delivered"
        print(statement)
        sse.publish({"message": statement}, type='publish')
        

    def send_ACK(self, packet, source):
        sse.publish({"packetNumber": packet.id}, type='ACK')
        statement = "{" + str(self.env.now) + "} | " + "Sending ACK for packet num: " + str(packet.seqnum)
        print(statement)
        sse.publish({"message": statement}, type='publish')
        ack = ACKID(packet.seqnum, packet.id)
        yield self.env.timeout(SEND_TIME)
        self.env.process(self.channel.send(source, ack, self))


    def send_NAK(self, packet, source):
        sse.publish({"packetNumber": packet.id}, type='NAK')
        statement = "{" + str(self.env.now) + "} | " + "Sending NAK for packet num: " + str(packet.seqnum)
        print(statement)
        sse.publish({"message": statement}, type='publish')
        nak = NAKID(packet.seqnum, packet.id)
        yield self.env.timeout(SEND_TIME)
        self.env.process(self.channel.send(source, nak, self))
