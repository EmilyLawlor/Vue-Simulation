from flask import jsonify

from Simulation.Utils.counter import Counter


class Statistics():
    def __init__(self):
        self.packetsGenerated = Counter()
        self.packetsSuccessfullySent = Counter()
        self.packetsLost = Counter()
        self.bitErrorsOccured = Counter()


    def incrementPacketsGenerated(self):
        self.packetsGenerated.increment()


    def incrementPacketsSuccessfullySent(self):
        self.packetsSuccessfullySent.increment()


    def incrementPacketsLost(self):
        self.packetsLost.increment()


    def incrementBitErrorsOccurred(self):
        self.bitErrorsOccured.increment()

    
    def getStats(self):
        return {'generated': self.packetsGenerated.getCount(), 'successfullySent': self.packetsSuccessfullySent.getCount(), 'lost': self.packetsLost.getCount(), 'errors': self.bitErrorsOccured.getCount()}
