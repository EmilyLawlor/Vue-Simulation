from Simulation.Utils.packetID import PacketID, ResendPacketID
from Simulation.Utils.senderStates import SequencedWaiting, SequencedSending
from Simulation.Utils.timer import Timer
from Simulation.Utils.constants import SEND_TIME, TIMEOUT_INTERVAL
import random
from flask_sse import sse


class Sender():
    def __init__(self, env, channel, stats, generation):
        self.env = env
        self.states = {'waiting-0':SequencedWaiting(0), 'waiting-1':SequencedWaiting(1), 'sending-0':SequencedSending(0), 'sending-1':SequencedSending(1)}
        self.currentState = self.states['waiting-0']
        self.channel = channel
        self.timer = None
        self.stats = stats
        self.generation = generation


    def setState(self, state):
        self.currentState = self.states[state]
        statement = "{" + str(self.env.now) + "} | " + "Sender now: " + str(self.currentState)
        print(statement)
        sse.publish({"message": statement}, type='publish')


    def generate_packets(self, destination):
        # continuously create packets, generated after random interval
        while True:
            self.stats.incrementPacketsGenerated()
            self.env.process(self.rdt_send(destination))
            # average time between sending packets
            mean_generation_time = 3
            # randomly sample the time

            if self.generation == 'Normal':
                random_interaval = abs(int(round(random.normalvariate(mean_generation_time,1))))
            elif self.generation == 'Exponential':
                random_interaval = int(round(random.expovariate(1.0/mean_generation_time),0))
            elif self.generation == '5':
                random_interaval = 5
            else:
                random_interaval = 3

            statement = "{" + str(self.env.now) + "} | " + "New packet ready to send"
            print(statement)
            sse.publish({"message": statement}, type='publish')
            yield self.env.timeout(random_interaval)


    def rdt_send(self, destination):
        if type(self.currentState) is SequencedWaiting:
            if self.currentState.seqnum == 0:
                self.setState('sending-0')
            else:
                self.setState('sending-1')
            packet=PacketID()
            packet.setSeqnum(self.currentState.seqnum)
            sse.publish({"packetNumber": packet.id}, type='send')
            statement = "{" + str(self.env.now) + "} | " + "Packet num: " + str(packet.seqnum) + " started sending"
            print(statement)
            sse.publish({"message": statement}, type='publish')

            # create timer instance for this packet and start the timer
            self.timer = Timer(self.env, TIMEOUT_INTERVAL, lambda: self.timeout(destination, packet), packet.seqnum)
            self.timer.start()

            # time taken to send one packet
            yield self.env.timeout(SEND_TIME)
            self.env.process(self.channel.send(destination, packet, self))
        else:
            statement = "{" + str(self.env.now) + "} | " + "Sender busy"
            print(statement)
            sse.publish({"message": statement}, type='publish')


    def handle(self, packet, source):
        # Decides what to do with ACKs received
        # if the packet is corrupted or it is the incorrect sequence number
        if packet.state is False or packet.seqnum != self.currentState.seqnum:
            # resend
            statement = "{" + str(self.env.now) + "} | " + "ACK not received correctly, resend"
            print(statement)
            sse.publish({"message": statement}, type='publish')
            # stop timer if it has not already been stopped, new timer will be started when packet is resent
            if self.timer.stopped is False:
                self.timer.stop()
            yield self.env.process(self.rdt_resend(source, packet))
        else:
            statement = "{" + str(self.env.now) + "} | " + "ACK received for packet num: " + str(packet.seqnum) + " by sender"
            sse.publish({'seqnum': packet.id}, type='ACKreceived')
            self.stats.incrementPacketsSuccessfullySent()
            print(statement)
            sse.publish({"message": statement}, type='publish')
            # packet receive ok stop timer, if it has not already been stopped
            if self.timer.stopped is False:
                self.timer.stop()
            if self.currentState.seqnum == 0:
                self.setState('waiting-1')
            else:
                self.setState('waiting-0')
            # packet received ok, do nothing
            yield self.env.timeout(0)


    def rdt_resend(self, destination, packet):
        sse.publish({"packetNumber": packet.id}, type='resend')
        statement = "{" + str(self.env.now) + "} | " + "Resending packet num: " + str(packet.seqnum)
        print(statement)
        sse.publish({"message": statement}, type='publish')
        # restart timer
        self.timer.start()
        yield self.env.timeout(SEND_TIME)
        self.env.process(self.channel.send(destination, ResendPacketID(packet.seqnum, packet.id), self))


    def timeout(self, destination, packet):
        statement = "{" + str(self.env.now) + "} | " + "Timeout occured for packet: " + str(packet.seqnum)
        print(statement)
        sse.publish({"message": statement}, type='publish')
        self.env.process(self.rdt_resend(destination, packet))
