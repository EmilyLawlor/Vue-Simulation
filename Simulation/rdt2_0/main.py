import simpy
from flask_sse import sse
from Simulation.rdt2_0.channel import Channel
from Simulation.rdt2_0.receiver import Receiver
from Simulation.rdt2_0.sender import Sender
from Simulation.rdt2_0.packet import Packet


class SimulationManager():
    def __init__(self, env, errorRate):
        self.env = env
        self.channel = Channel(self.env, errorRate)
        self.receiver = Receiver(self.env, self.channel)
        self.sender = Sender(self.env, self.channel)
        self.action = self.env.process(self.start())


    def start(self):
        #if type(self.sender.state) is Waiting:
        while True:
            statement = "{" + str(self.env.now) + "} | " + "New packet ready to send"
            print(statement)
            sse.publish({"message": statement}, type='publish')
            self.env.process(self.sender.rdt_send(self.receiver))
            yield self.env.timeout(3)   # new packet generated to send every 3 units time


class Start():

    def run(self, runTime, errorRate):
        sse.publish({"protocol": "rdt2.0"}, type='start')
        env = simpy.rt.RealtimeEnvironment()
        sim = SimulationManager(env, errorRate)
        env.run(until=runTime)
        statement = "END"
        Packet().resetSeqnum()
        print(statement)
        sse.publish({"message": statement}, type='terminate')


if __name__ == '__main__':
    env = simpy.Environment()
    sim = SimulationManager(env)
    env.run(until=50)
