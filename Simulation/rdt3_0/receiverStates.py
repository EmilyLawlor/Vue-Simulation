from Simulation.Utils.state import SequencesState


class Waiting(SequencesState):
    def __init__(self, seqnum):
        super(Waiting, self).__init__('Waiting', seqnum)


class Receiving(SequencesState):
    def __init__(self, seqnum):
        self.seqnum = seqnum
        super(Receiving, self).__init__('Receiving', seqnum)
