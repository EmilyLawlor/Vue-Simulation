from Simulation.Utils.state import State

class Waiting(State):
    def __init__(self):
        super(Waiting, self).__init__('Waiting')


class WaitingFirst(Waiting):
    def __init__(self):
        self.seqnum = 0
        super().__init__()


class WaitingSecond(Waiting):
    def __init__(self):
        self.seqnum = 1
        super().__init__()


class Receiving(State):
    def __init__(self):
        super(Receiving, self).__init__('Receiving')


class ReceivingFirst(Receiving):
    def __init__(self):
        self.seqnum = 0
        super().__init__()


class ReceivingSecond(Receiving):
    def __init__(self):
        self.seqnum = 1
        super().__init__()
