import simpy.rt
from flask_sse import sse
from Simulation.rdt2_2.channel import Channel
from Simulation.rdt2_2.packet import Packet
from Simulation.rdt2_2.receiver import Receiver
from Simulation.rdt2_2.sender import Sender
from Simulation.Utils.statistics import Statistics


class SimulationManager():
    def __init__(self, env, errorRate, stats):
        self.env = env
        self.channel = Channel(self.env, errorRate, stats)
        self.receiver = Receiver(self.env, self.channel)
        self.sender = Sender(self.env, self.channel, stats)
        self.action = self.env.process(self.start())
        self.stats = stats


    def start(self):
        #if type(self.sender.state) is Waiting:
        while True:
            self.stats.incrementPacketsGenerated()
            statement = "{" + str(self.env.now) + "} | " + "New packet ready to send"
            print(statement)
            sse.publish({"message": statement}, type='publish')
            self.env.process(self.sender.rdt_send(self.receiver))
            yield self.env.timeout(3)   # new packet generated to send every 3 units time


class Start():

    def run(self, runTime, errorRate):
        sse.publish({"protocol": "rdt2.2"}, type='start')
        stats = Statistics()
        env = simpy.rt.RealtimeEnvironment()
        sim = SimulationManager(env, errorRate, stats)
        env.run(until=runTime)
        statement = "END"
        print(statement)
        stats = stats.getStats()
        stats['message'] = statement
        sse.publish(stats, type='terminate')
        Packet.resetId()
        

if __name__ == '__main__':
    env = simpy.Environment()
    sim = SimulationManager(env)
    env.run(until=50)
