from Simulation.SR.state import State


class Waiting(State):
    def __init__(self):
        super(Waiting, self).__init__('Waiting')


class Sending(State):
    def __init__(self):
        super(Sending, self).__init__('Sending')
