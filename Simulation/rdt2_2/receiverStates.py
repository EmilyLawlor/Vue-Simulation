from Simulation.Utils.state import SequencedState


class Waiting(SequencedState):
    def __init__(self, seqnum):
        super(Waiting, self).__init__('Waiting', seqnum)
