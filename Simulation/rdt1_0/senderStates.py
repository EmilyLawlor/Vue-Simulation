from Simulation.rdt1_0.state import State


class Waiting(State):
    """
    Sender is currently not busy
    """
    def __init__(self):
        super(Waiting, self).__init__('Waiting')


class Sending(State):
    def __init__(self):
        super(Sending, self).__init__('Sending')
