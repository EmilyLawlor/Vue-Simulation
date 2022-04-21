import random

from flask_sse import sse
from Simulation.Utils.constants import SEND_TIME, TIMEOUT_INTERVAL
from Simulation.Utils.packet import Packet
from Simulation.Utils.timer import Timer


class Sender():
    def __init__(self, env, channel, windowSize, stats, generation):
        self.env = env
        self.channel = channel
        self.windowSize = windowSize
        self.timer = None
        self.nextSeqNum = 1
        self.base = 1
        self.stats = stats
        self.generation = generation
        self.lastACK = 0


    # simulating packet creation for telephone wires, compare against other packet generation methods
    def generate_packets(self, destination):
        # continuously create packets, generated after random interval
        while True:
            self.stats.incrementPacketsGenerated()
            packet=Packet(self.nextSeqNum)
            self.env.process(self.rdt_send(destination, packet))

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

            statement = "{" + str(self.env.now) + "} | " + "New packet ready to send"
            print(statement)
            #sse.publish({"message": statement}, type='publish')
            yield self.env.timeout(random_interaval)



    def timeout(self, destination, seqnum):
        statement = "{" + str(self.env.now) + "} | " + "Timeout occured for packet: " + str(seqnum)
        print(statement)
        sse.publish({"message": statement}, type='publish')
        self.env.process(self.rdt_resend(destination))


    def rdt_send(self, destination, packet):
        if self.nextSeqNum < self.base + self.windowSize:
            sse.publish({"packetNumber": packet.seqnum - 1}, type='send')
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

            if packet.seqnum != self.lastACK:
                # if this packet has just been ACKed and this is not a duplicate ACK sent due to out-of-order or corrupt packets, then mark as new packet successfully received
                # loop for cumulative ACKs
                for i in range (self.lastACK, packet.seqnum):
                    self.stats.incrementPacketsSuccessfullySent()
            self.lastACK = packet.seqnum

            self.base = packet.seqnum + 1
            sse.publish({"base": self.base, 'seqnum': packet.seqnum}, type='ACKreceived')
            # if this ACKs the last unACKed packet in channel, stop timer and wait
            if self.base == self.nextSeqNum:
                self.timer.stop()
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
            packet = Packet(seqnum)
            sse.publish({"packetNumber": seqnum-1}, type='resend')
            statement = "{" + str(self.env.now) + "} | " + "Resending packet num: " + str(seqnum)
            print(statement)
            sse.publish({"message": statement}, type='publish')
            self.env.process(self.udt_send(destination, packet))
        yield self.env.timeout(0)
