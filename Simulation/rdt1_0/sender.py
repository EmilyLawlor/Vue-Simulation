from Simulation.rdt1_0.packet import Packet
from Simulation.rdt1_0.senderStates import Waiting, Sending

SEND_TIME = 2   # time to send a packet to receiver

class Sender():
    def __init__(self, env, channel):
        self.env = env
        self.state = Waiting()
        self.states = {'waiting': Waiting(), 'sending':Sending()}
        self.channel = channel


    def setState(self, state):
        self.state = self.states[state]
        print("{" + str(self.env.now) + "} | " + "Sender now: " + str(self.state))


    def rdt_send(self, destination):
        if type(self.state) is Waiting:
            self.setState('sending')
            packet = Packet('data')
            print("{" + str(self.env.now) + "} | " + "Sending packet num " + str(packet.seqnum))
            yield self.env.timeout(SEND_TIME)
            self.env.process(self.channel.send(destination, packet, self))
        else:
            print("{" + str(self.env.now) + "} | " + "Sender busy please wait")


    def handle(self, packet, source):
        # Decides what to do with ACKs received
        print("{" + str(self.env.now) + "} | " + "ACK received for packet num: " + str(packet.packet_num) + " by sender")
        self.setState('waiting')
        yield self.env.timeout(2)
