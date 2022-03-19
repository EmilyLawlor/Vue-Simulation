from Simulation.SR.sender import Sender
from Simulation.SR.receiver import Receiver
from Simulation.SR.channel import Channel
import simpy.rt
from flask_sse import sse


class SimulationManager():
    def __init__(self, env, errorRate, lossRate, windowSize):
        self.env = env
        self.channel = Channel(self.env, errorRate, lossRate)
        self.receiver = Receiver(self.env, self.channel, windowSize)
        self.sender = Sender(self.env, self.channel, windowSize)
        self.action = self.env.process(self.start())


    def start(self):
        #if type(self.sender.state) is Waiting:
        while True:
            yield self.env.process(self.sender.generate_packets(self.receiver))


class Start():

    def run(self, runTime, errorRate, lossRate, windowSize):
        sse.publish({"protocol": "Selective-Repeat"}, type='start')
        env = simpy.rt.RealtimeEnvironment()
        # all varibales passed from GUI to back end will go through here, only to be picked by users through dropdowns and sliders and will be set throguh setters
        sim = SimulationManager(env, errorRate, lossRate, windowSize)
        env.run(until=runTime)
        statement = "END"
        print(statement)
        sse.publish({"message": statement}, type='terminate')


if __name__ == '__main__':
    env = simpy.Environment()
    sim = SimulationManager(env)
    env.run(until=50)
