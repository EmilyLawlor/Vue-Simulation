from Simulation.rdt1_0.sender import Sender
from Simulation.rdt1_0.receiver import Receiver
from Simulation.rdt1_0.channel import Channel
from Simulation.rdt1_0.senderStates import Waiting
import simpy


class SimulationManager():
    def __init__(self, env):
        self.env = env
        self.channel = Channel(self.env)
        self.receiver = Receiver(self.env, self.channel)
        self.sender = Sender(self.env, self.channel)
        self.action = self.env.process(self.start())


    def start(self):
        #if type(self.sender.state) is Waiting:
        while True:
            yield self.env.process(self.sender.rdt_send(self.receiver))


if __name__ == '__main__':
    env = simpy.Environment()
    sim = SimulationManager(env)
    env.run(until=10)
