import random

import simpy.rt
from flask_sse import sse
from Simulation.rdt2_1.receiver import Receiver
from Simulation.rdt2_1.sender import Sender
from Simulation.Utils.channel import ErrorChannel
from Simulation.Utils.packetID import PacketID
from Simulation.Utils.statistics import Statistics


class SimulationManager():
    def __init__(self, env, errorRate, stats, generation):
        self.env = env
        self.channel = ErrorChannel(self.env, errorRate, stats)
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
                random_interaval = abs(int(round(random.expovariate(1.0/mean_generation_time),0)))
            elif self.generation == '5':
                random_interaval = 5
            else:
                random_interaval = 3
            yield self.env.timeout(random_interaval)   # new packet generated to send every 3 units time


def run(runTime, errorRate, generation):
        sse.publish({"protocol": "rdt2.1"}, type='start')
        stats = Statistics()
        env = simpy.rt.RealtimeEnvironment()
        sim = SimulationManager(env, errorRate, stats, generation)
        env.run(until=runTime)
        statement = "END"
        print(statement)
        stats = stats.getStats()
        stats['message'] = statement
        sse.publish(stats, type='terminate')
        PacketID.resetId()


if __name__ == '__main__':
    env = simpy.Environment()
    sim = SimulationManager(env)
    env.run(until=50)
