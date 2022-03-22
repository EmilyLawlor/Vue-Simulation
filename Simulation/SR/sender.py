import random

import simpy.rt
from Simulation.SR.packet import Packet, ResendPacket
from Simulation.SR.senderStates import Sending, Waiting
from Simulation.Utils.timer import Timer
from flask_sse import sse


SEND_TIME = 2
TIMEOUT_INTERVAL = 7


class Sender():
    def __init__(self, env, channel, windowSize):
        self.env = env
        self.states = {'waiting':Waiting(), 'sending':Sending()}
        self.currentState = self.states['waiting']
        self.channel = channel
        self.windowSize = windowSize
        self.timer = {}
        self.nextSeqNum = 1
        self.base = 1
        self.unACKed = []


    def setState(self, state):
        self.currentState = self.states[state]
        statement = "{" + str(self.env.now) + "} | " + "Sender now: " + str(self.currentState)
        print(statement)
        sse.publish({"message": statement}, type='publish')


    def generate_packets(self, destination):
        # continuously create packets, generated after random interval
        while True:
            packet=Packet(self.nextSeqNum, 'data')

            self.env.process(self.rdt_send(destination, packet))

            # average time between sending packets
            mean_send_time = 3
            # randomly sample the time
            random_interaval = int(round(random.expovariate(1.0/mean_send_time),0))
            statement = "{" + str(self.env.now) + "} | " + "New packet ready to send"
            print(statement)
            sse.publish({"message": statement}, type='publish')
            yield self.env.timeout(random_interaval)


    def timeout(self, destination, seqnum):
        statement = "{" + str(self.env.now) + "} | " + "Timeout occured for packet: " + str(seqnum)
        print(statement)
        sse.publish({"message": statement}, type='publish')
        self.env.process(self.rdt_resend(destination, seqnum))
        

    def rdt_send(self, destination, packet):
        if self.nextSeqNum < self.base + self.windowSize:
            statement = "{" + str(self.env.now) + "} | " + "Packet num: " + str(packet.seqnum) + " started sending"
            print(statement)
            sse.publish({"message": statement}, type='publish')

            # add time packet was sent with sequence number
            self.timer[packet.seqnum] = Timer(self.env, TIMEOUT_INTERVAL, lambda: self.timeout(destination, packet.seqnum), packet.seqnum)
            if packet.seqnum in self.timer:
                self.timer[packet.seqnum].start()

            self.unACKed.append(packet.seqnum)
            self.nextSeqNum += 1

            self.env.process(self.udt_send(destination, packet))
            yield self.env.timeout(0)
        else:
            statement = "{" + str(self.env.now) + "} | " + "Sender busy"
            print(statement)
            sse.publish({"message": statement}, type='publish')


    def udt_send(self, destination, packet):
        # time taken to send one packet
        # move this to seperate function so it can be called mulitple times at once so more than one packet can be sent at a time
        yield self.env.timeout(SEND_TIME)
        self.env.process(self.channel.send(destination, packet, self))


    def handle(self, packet, source):
        # Decides what to do with ACKs received
        # if the packet is corrupted or it is the incorrect sequence number
        if packet.state is False:
            # do nothing
            statement = "{" + str(self.env.now) + "} | " + "ACK not received correctly"
            print(statement)
            sse.publish({"message": statement}, type='publish')
            yield self.env.timeout(0)
        else:
            statement = "{" + str(self.env.now) + "} | " + "ACK received for packet num: " + str(packet.seqnum) + " by sender"
            print(statement)
            sse.publish({"message": statement}, type='publish')
            if packet.seqnum in self.timer:
                self.timer[packet.seqnum].stop()
            # if this packet is the smallest unACKed packet, move window base to the next smallest unACKed packet
            if self.unACKed[0] == packet.seqnum:
                # use .pop() to remove from unACKed list as they are ACKed
                self.unACKed.pop(0)
                if len(self.unACKed) > 0:
                    self.base = self.unACKed[0]
                # if another there are no other unACKed packets in the channel, increase the base by 1
                else:
                    self.base = self.nextSeqNum
            # if it was not smallest unACKed packet, find in unACKed list and remove
            elif packet.seqnum in self.unACKed:
                self.unACKed.remove(packet.seqnum)



    def rdt_resend(self, destination, seqnum):
        packet = ResendPacket(seqnum)
        statement = "{" + str(self.env.now) + "} | " + "Resending packet num: " + str(seqnum)
        print(statement)
        sse.publish({"message": statement}, type='publish')
        if seqnum in self.timer:
            self.timer[seqnum].start()
        self.env.process(self.udt_send(destination, packet))
        yield self.env.timeout(0)
