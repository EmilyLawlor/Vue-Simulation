from Simulation.Utils.state import SequencedState


class Waiting(SequencedState):
    def __init__(self, seqnum):
        super(Waiting, self).__init__('Waiting', seqnum)


class Sending(SequencedState):
    def __init__(self, seqnum):
        super(Sending, self).__init__('Sending', seqnum)
