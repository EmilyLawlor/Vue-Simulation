import simpy.rt
from flask import jsonify
from flask_sse import sse
from Simulation.rdt3_0.channel import Channel
from Simulation.rdt3_0.receiver import Receiver
from Simulation.rdt3_0.sender import Sender


class SimulationManager():
    def __init__(self, env, errorRate, lossRate):
        self.env = env
        self.channel = Channel(self.env, errorRate, lossRate)
        self.receiver = Receiver(self.env, self.channel)
        self.sender = Sender(self.env, self.channel)
        self.action = self.env.process(self.start())


    def start(self):
        #if type(self.sender.state) is Waiting:
        while True:
            yield self.env.process(self.sender.generate_packets(self.receiver))


class Start():

    def run(self, runTime, errorRate, lossRate):
        sse.publish({"protocol": "Stop-and-Wait"}, type='start')
        env = simpy.rt.RealtimeEnvironment()
        # all varibales passed from GUI to back end will go through here, only to be picked by users through dropdowns and sliders and will be set throguh setters
        sim = SimulationManager(env, errorRate, lossRate)
        env.run(until=runTime)
        statement = "END"
        print(statement)
        sse.publish({"message": statement}, type='terminate')


if __name__ == '__main__':
    env = simpy.Environment()
    sim = SimulationManager(env)
    env.run(until=50)
