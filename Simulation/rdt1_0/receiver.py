from Simulation.rdt1_0.receiverStates import Waiting, Receiving
from Simulation.rdt1_0.packet import ACK


DELIVER_TIME = 2    # time to deliver packet to upper layers
SEND_TIME = 2   # time to send packet back to sender - ACK or NAK


class Receiver():
    def __init__(self, env, channel):
        self.env = env
        self.state = Waiting()
        self.states = {'waiting':Waiting(), 'receiving':Receiving()}
        self.channel = channel


    def setState(self, state):
        self.state = self.states[state]
        print("{" + str(self.env.now) + "} | " + "Receiver now: " + str(self.state))


    def handle(self, packet, source):
        if type(self.state) is Waiting:
            self.setState('receiving')
            seqnum = packet.seqnum
            self.env.process(self.deliver_data(seqnum))
            yield self.env.process(self.send_ACK(seqnum, source))
        else:
            print("{" + str(self.env.now) + "} | " + "Receiver busy please wait")


    def deliver_data(self, seqnum):
        yield self.env.timeout(DELIVER_TIME)
        print("{" + str(self.env.now) + "} | " + "Packet num: " + str(seqnum) + " received")


    def send_ACK(self, packet_num, source):
        ack = ACK(packet_num)
        self.setState('waiting')
        self.env.process(self.channel.send(source, ack, self))
        yield self.env.timeout(SEND_TIME)
        
