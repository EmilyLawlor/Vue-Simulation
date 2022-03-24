from curses import window
import random

import simpy.rt
from Simulation.GBN.packet import Packet, ResendPacket
from Simulation.GBN.senderStates import Sending, Waiting
from Simulation.Utils.timer import Timer
from flask_sse import sse

SEND_TIME = 2
TIMEOUT_INTERVAL = 5


class Sender():
    def __init__(self, env, channel, windowSize, stats):
        self.env = env
        self.states = {'waiting':Waiting(), 'sending':Sending()}
        self.currentState = self.states['waiting']
        self.channel = channel
        self.windowSize = windowSize
        self.window = simpy.Resource(self.env, capacity=windowSize)
        self.timer = None
        self.nextSeqNum = 1
        self.base = 1
        self.stats = stats


    def setState(self, state):
        self.currentState = self.states[state]
        statement = "{" + str(self.env.now) + "} | " + "Sender now: " + str(self.currentState)
        print(statement)
        sse.publish({"message": statement}, type='publish')


    # simulating packet creation for telephone wires, compare against other packet generation methods
    def generate_packets(self, destination):
        # continuously create packets, generated after random interval
        while True:
            self.stats.incrementPacketsGenerated()
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
        self.env.process(self.rdt_resend(destination))


    def rdt_send(self, destination, packet):
        if self.nextSeqNum < self.base + self.windowSize:
            statement = "{" + str(self.env.now) + "} | " + "Packet num: " + str(packet.seqnum) + " started sending"
            print(statement)
            sse.publish({"message": statement}, type='publish')

            if self.base == self.nextSeqNum:
            # add time packet was sent with sequence number
                self.timer = Timer(self.env, TIMEOUT_INTERVAL, lambda: self.timeout(destination, packet.seqnum), packet.seqnum)
                self.timer.start()

            self.env.process(self.udt_send(destination, packet))
            self.nextSeqNum += 1
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
        # if the packet is corrupted
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

            self.stats.incrementPacketsSuccessfullySent()

            self.base = packet.seqnum + 1
            # if this ACKs the last unACKed packet in channel, stop timer and wait
            if self.base == self.nextSeqNum:
                self.timer.stop()
            # if error occurs in first packet sent it will send an ACK for packet 0, if this happens don't want to start timer for next packet as it would delay the re-sending process 
            # if there are still more unACKed packets in channel, stop current timer and create new timer instance for next oldest unACKed packet in channel
            # don't stop timer and create new timer instance for the same packet
            elif self.base != self.timer.seqnum:
                self.timer.stop()
                self.timer = Timer(self.env, TIMEOUT_INTERVAL, lambda: self.timeout(source, self.base), self.base)
                self.timer.start()


    def rdt_resend(self, destination):

        self.timer = Timer(self.env, TIMEOUT_INTERVAL, lambda: self.timeout(destination, self.base), self.base)
        self.timer.start()

        for seqnum in range(self.base, self.nextSeqNum):
            packet = ResendPacket(seqnum)
            statement = "{" + str(self.env.now) + "} | " + "Resending packet num: " + str(seqnum)
            print(statement)
            sse.publish({"message": statement}, type='publish')
            self.env.process(self.udt_send(destination, packet))
        yield self.env.timeout(0)
