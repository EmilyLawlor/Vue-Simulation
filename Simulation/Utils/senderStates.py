from Simulation.Utils.state import SequencedState
from Simulation.Utils.state import State


class SequencedWaiting(SequencedState):
    def __init__(self, seqnum):
        super(SequencedWaiting, self).__init__('Waiting', seqnum)


class SequencedSending(SequencedState):
    def __init__(self, seqnum):
        super(SequencedSending, self).__init__('Sending', seqnum)


class Waiting(State):
    def __init__(self):
        super(Waiting, self).__init__('Waiting')


class Sending(State):
    def __init__(self):
        super(Sending, self).__init__('Sending')
