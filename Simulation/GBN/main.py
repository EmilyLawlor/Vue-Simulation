import simpy.rt
from flask_sse import sse
from Simulation.GBN.receiver import Receiver
from Simulation.GBN.sender import Sender
from Simulation.Utils.channel import ErrorAndLossChannel
from Simulation.Utils.statistics import Statistics


class SimulationManager():
    def __init__(self, env, errorRate, lossRate, windowSize, stats):
        self.env = env
        self.channel = ErrorAndLossChannel(self.env, errorRate, lossRate, stats)
        self.receiver = Receiver(self.env, self.channel, windowSize)
        self.sender = Sender(self.env, self.channel, windowSize, stats)
        self.action = self.env.process(self.start())


    def start(self):
        while True:
            yield self.env.process(self.sender.generate_packets(self.receiver))


def run(runTime, errorRate, lossRate, windowSize):
        sse.publish({"protocol": 'Go-Back-N'}, type='start')

        stats = Statistics()
        env = simpy.rt.RealtimeEnvironment()
        sim = SimulationManager(env, errorRate, lossRate, windowSize, stats)
        env.run(until=runTime)

        statement = "END"
        print(statement)
        stats = stats.getStats()
        stats['message'] = statement
        sse.publish(stats, type='terminate')


if __name__ == '__main__':
    print(__package__)
    env = simpy.Environment()
    sim = SimulationManager(env)
    env.run(until=50)
