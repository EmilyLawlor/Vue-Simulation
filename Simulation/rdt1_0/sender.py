from flask_sse import sse
from Simulation.rdt1_0.packet import Packet
from Simulation.rdt1_0.senderStates import Sending, Waiting

SEND_TIME = 2   # time to send a packet to receiver

class Sender():
    def __init__(self, env, channel):
        self.env = env
        self.state = Waiting()
        self.states = {'waiting': Waiting(), 'sending':Sending()}
        self.channel = channel


    def setState(self, state):
        self.state = self.states[state]
        statement = "{" + str(self.env.now) + "} | " + "Sender now: " + str(self.state)
        print(statement)
        sse.publish({"message": statement}, type='publish')


    def rdt_send(self, destination):
        if type(self.state) is Waiting:
            self.setState('sending')
            packet = Packet('data')
            statement = "{" + str(self.env.now) + "} | " + "Sending packet num " + str(packet.seqnum)
            print(statement)
            sse.publish({"message": statement}, type='publish')
            yield self.env.timeout(SEND_TIME)
            self.env.process(self.channel.send(destination, packet, self))
        else:
            statement = "{" + str(self.env.now) + "} | " + "Sender busy please wait"
            print(statement)
            sse.publish({"message": statement}, type='publish')


    def handle(self, packet, source):
        # Decides what to do with ACKs received
        statement = "{" + str(self.env.now) + "} | " + "ACK received for packet num: " + str(packet.packet_num) + " by sender"
        print(statement)
        sse.publish({"message": statement}, type='publish')
        self.setState('waiting')
        yield self.env.timeout(2)
