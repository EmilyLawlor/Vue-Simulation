from Simulation.rdt1_1.sender import Sender
from Simulation.rdt1_1.receiver import Receiver
from Simulation.rdt1_1.channel import Channel
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
            print("{" + str(self.env.now) + "} | " + "New packet ready to send")
            self.env.process(self.sender.rdt_send(self.receiver))
            yield self.env.timeout(3)   # new packet generated to send every 3 units time


if __name__ == '__main__':
    env = simpy.Environment()
    sim = SimulationManager(env)
    env.run(until=50)
