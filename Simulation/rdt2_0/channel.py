from random import randrange
from flask_sse import sse

class Channel():
    def __init__(self, env, errorRate):
        self.env = env
        self.errorRate = errorRate


    def send(self, destination, packet, source):
        errors = randrange(9)
        if errors < self.errorRate:
            # bit error
            statement = "{" + str(self.env.now) + "} | " + "Bit errors occured in " + packet.__class__.__name__ + " number " + str(packet.seqnum)
            print(statement)
            sse.publish({"message": statement}, type='publish')
            packet.state = False
        yield self.env.process(destination.handle(packet, source))
