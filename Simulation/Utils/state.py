class State(object):

    def __init__(self, name):
        self.name = name


    def __str__(self):
        return self.name 


class SequencesState(object):

    def __init__(self, name, seqnum):
        self.name = name
        self.seqnum = seqnum


    def __str__(self):
        return self.name + " " + str(self.seqnum)