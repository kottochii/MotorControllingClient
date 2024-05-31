import time
import threading
import states 


class timer:
    stop_required = False
    def __init__(self, secs):
        self.secs = secs
        self.thread = threading.Thread( target=self.keep_going)
        self.thread.start()

    def keep_going(self):
        while((not self.stop_required) and (self.secs > 0)):
            self.secs -= 1
            time.sleep(1)

        self.on_done()

    def on_done(self):
        states.global_state = states.signed_out_state()

    def terminate(self):
        self.stop_required = True