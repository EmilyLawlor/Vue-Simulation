import simpy.rt
from flask_sse import sse
from Simulation.rdt1_0.channel import Channel
from Simulation.rdt1_0.receiver import Receiver
from Simulation.rdt1_0.sender import Sender
from Simulation.rdt1_0.packet import Packet
from Simulation.Utils.statistics import Statistics


class SimulationManager():
    def __init__(self, env, stats):
        self.env = env
        self.channel = Channel(self.env)
        self.receiver = Receiver(self.env, self.channel)
        self.sender = Sender(self.env, self.channel, stats)
        self.action = self.env.process(self.start())


    def start(self):
        while True:
            yield self.env.process(self.sender.rdt_send(self.receiver))


class Start():

    def run(self, runTime):
        sse.publish({"protocol": "rdt1.0"}, type='start')
        stats = Statistics('rdt1.0')
        env = simpy.rt.RealtimeEnvironment()
        sim = SimulationManager(env, stats)
        env.run(until=runTime)
        statement = "END"
        Packet().resetSeqnum()
        print(statement)
        stats = stats.getStats()
        stats['message'] = statement
        sse.publish(stats, type='terminate')


if __name__ == '__main__':
    env = simpy.Environment()
    sim = SimulationManager(env)
    env.run(until=10)
