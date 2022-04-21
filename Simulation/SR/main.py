import simpy
import simpy.rt
from flask_sse import sse
from Simulation.SR.receiver import Receiver
from Simulation.SR.sender import Sender
from Simulation.Utils.channel import ErrorAndLossChannel
from Simulation.Utils.statistics import Statistics


class SimulationManager():
    def __init__(self, env, errorRate, lossRate, windowSize, stats, generation):
        self.env = env
        self.channel = ErrorAndLossChannel(self.env, errorRate, lossRate, stats)
        self.receiver = Receiver(self.env, self.channel, windowSize)
        self.sender = Sender(self.env, self.channel, windowSize, stats, generation)
        self.action = self.env.process(self.start())


    def start(self):
        while True:
            yield self.env.process(self.sender.generate_packets(self.receiver))


def run(runTime, errorRate, lossRate, windowSize, generation):
        sse.publish({"protocol": "Selective-Repeat"}, type='start')
        stats = Statistics()
        env = simpy.rt.RealtimeEnvironment()
        sim = SimulationManager(env, errorRate, lossRate, windowSize, stats, generation)
        env.run(until=runTime)
        statement = "END"
        print(statement)
        stats = stats.getStats()
        stats['message'] = statement
        sse.publish( stats , type='terminate')


if __name__ == '__main__':
    env = simpy.rt.RealtimeEnvironment()
    sim = SimulationManager(env, 10, 10, 5)
    env.run(until=50)
