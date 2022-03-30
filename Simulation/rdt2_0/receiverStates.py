from Simulation.Utils.state import State

class Waiting(State):
    """
    Receiver is currently not busy
    """
    def __init__(self):
        super(Waiting, self).__init__('Waiting')



class Receiving(State):
    """
    Receiver is being transmitted data
    """

    def __init__(self):
        super(Receiving, self).__init__('Receiving')
