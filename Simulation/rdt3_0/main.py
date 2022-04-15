import simpy.rt
from flask_sse import sse
from Simulation.rdt3_0.receiver import Receiver
from Simulation.rdt3_0.sender import Sender
from Simulation.Utils.channel import ErrorAndLossChannel
from Simulation.Utils.packetID import PacketID
from Simulation.Utils.statistics import Statistics


class SimulationManager():
    def __init__(self, env, errorRate, lossRate, stats):
        self.env = env
        self.channel = ErrorAndLossChannel(self.env, errorRate, lossRate, stats)
        self.receiver = Receiver(self.env, self.channel)
        self.sender = Sender(self.env, self.channel, stats)
        self.action = self.env.process(self.start())


    def start(self):
        while True:
            yield self.env.process(self.sender.generate_packets(self.receiver))


def run(runTime, errorRate, lossRate):
        sse.publish({"protocol": "Stop-and-Wait"}, type='start')

        stats = Statistics()
        env = simpy.rt.RealtimeEnvironment()
        sim = SimulationManager(env, errorRate, lossRate, stats)
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
