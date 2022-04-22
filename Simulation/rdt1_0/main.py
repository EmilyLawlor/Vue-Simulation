import simpy.rt
from flask_sse import sse
from Simulation.Utils.channel import Channel
from Simulation.rdt1_0.receiver import Receiver
from Simulation.rdt1_0.sender import Sender
from Simulation.Utils.statistics import Statistics
import random


class SimulationManager():
    def __init__(self, env, stats, generation):
        self.env = env
        self.channel = Channel(self.env)
        self.receiver = Receiver(self.env, self.channel)
        self.sender = Sender(self.env, self.channel, stats)
        self.action = self.env.process(self.start())
        self.stats = stats
        self.generation = generation

    def start(self):
        while True:
            self.stats.incrementPacketsGenerated()
            statement = "{" + str(self.env.now) + "} | " + "New packet ready to send"
            print(statement)
            sse.publish({"message": statement}, type='publish')
            self.env.process(self.sender.rdt_send(self.receiver))

            # average time between sending packets
            mean_generation_time = 3

            if self.generation == 'Normal':
                random_interaval = abs(int(round(random.normalvariate(mean_generation_time,1))))
            elif self.generation == 'Exponential':
                random_interaval = int(round(random.expovariate(1.0/mean_generation_time),0))
            elif self.generation == '5':
                random_interaval = 5
            else:
                random_interaval = 3
            yield self.env.timeout(random_interaval)   # new packet generated to send every 5 units time


def run(runTime, generation):
    sse.publish({"protocol": "rdt1.0"}, type='start')
    stats = Statistics()
    env = simpy.rt.RealtimeEnvironment()
    sim = SimulationManager(env, stats, generation)
    env.run(until=runTime)
    statement = "END"
    print(statement)
    stats = stats.getStats()
    stats['message'] = statement
    sse.publish(stats, type='terminate')


if __name__ == '__main__':
    env = simpy.Environment()
    sim = SimulationManager(env)
    env.run(until=10)
