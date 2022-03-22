import simpy.rt
from flask_sse import sse
from Simulation.rdt1_0.channel import Channel
from Simulation.rdt1_0.receiver import Receiver
from Simulation.rdt1_0.sender import Sender
from Simulation.rdt1_0.packet import Packet


class SimulationManager():
    def __init__(self, env):
        self.env = env
        self.channel = Channel(self.env)
        self.receiver = Receiver(self.env, self.channel)
        self.sender = Sender(self.env, self.channel)
        self.action = self.env.process(self.start())


    def start(self):
        while True:
            yield self.env.process(self.sender.rdt_send(self.receiver))


class Start():

    def run(self, runTime):
        sse.publish({"protocol": "rdt1.0"}, type='start')
        env = simpy.rt.RealtimeEnvironment()
        sim = SimulationManager(env)
        env.run(until=runTime)
        statement = "END"
        Packet().resetSeqnum()
        print(statement)
        sse.publish({"message": statement}, type='terminate')


if __name__ == '__main__':
    env = simpy.Environment()
    sim = SimulationManager(env)
    env.run(until=10)
