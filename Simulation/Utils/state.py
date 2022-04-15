class State(object):

    def __init__(self, name):
        self.name = name


    def __str__(self):
        return self.name 


class SequencedState(State):

    def __init__(self, name, seqnum):
        super().__init__(name)
        self.seqnum = seqnum


    def __str__(self):
        return self.name + " " + str(self.seqnum)