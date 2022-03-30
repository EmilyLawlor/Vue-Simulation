from Simulation.Utils.state import State

class Waiting(State):
    def __init__(self):
        super(Waiting, self).__init__('Waiting')


class WaitingFirst(Waiting):
    def __init__(self):
        super().__init__()
        self.seqnum = 0


class WaitingSecond(Waiting):
    def __init__(self):
        super().__init__()
        self.seqnum = 1


class Sending(State):
    def __init__(self):
        super(Sending, self).__init__('Sending')


class SendingFirst(Sending):
    def __init__(self):
        super().__init__()
        self.seqnum = 0


class SendingSecond(Sending):
    def __init__(self):
        super().__init__()
        self.seqnum = 1
