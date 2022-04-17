from Simulation.Utils.state import SequencedState
from Simulation.Utils.state import State


class SequencedWaiting(SequencedState):
    def __init__(self, seqnum):
        super(SequencedWaiting, self).__init__('Waiting', seqnum)


class SequencedReceiving(SequencedState):
    def __init__(self, seqnum):
        super(SequencedReceiving, self).__init__('Receiving', seqnum)


class Waiting(State):
    def __init__(self):
        super(Waiting, self).__init__('Waiting')


class Receiving(State):
    def __init__(self):
        super(Receiving, self).__init__('Receiving')