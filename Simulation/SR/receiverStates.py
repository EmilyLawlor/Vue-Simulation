from Simulation.Utils.state import State


class Waiting(State):
    def __init__(self):
        super(Waiting, self).__init__('Waiting')


class Receiving(State):
    def __init__(self):
        super(Receiving, self).__init__('Receiving')
