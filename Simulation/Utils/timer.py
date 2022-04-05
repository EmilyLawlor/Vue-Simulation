import simpy


class Timer():
    def __init__(self, env, timeout_interval, callback, seqnum):
        self.env = env
        self.timeout_interval = timeout_interval
        self.callback = callback
        self.seqnum = seqnum
        self.timer = None
        self.running = False
        self.stopped = False


    def start(self):
        if self.running is False:
            print("{" + str(self.env.now) + "} | " + "Timer for packet " + str(self.seqnum) + " started")
            self.running = True
            self.stopped = False
            self.timer = self.env.process(self.timeout())


    def timeout(self):
        try:
            yield self.env.timeout(self.timeout_interval)
            self.running = False
            self.stopped = True
            self.callback()
        except simpy.Interrupt:
            pass

    
    def stop(self):
        if self.running:
            print("{" + str(self.env.now) + "} | " + "Timer for packet " + str(self.seqnum) + " stopped")
            self.running = False
            self.stopped = True
            self.timer.interrupt()


