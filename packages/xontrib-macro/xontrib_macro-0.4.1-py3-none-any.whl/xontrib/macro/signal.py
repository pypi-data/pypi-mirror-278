import sys
import signal

class DisableInterruptCM:
    def __enter__(self):
        self.handler_called = False
        self.original_handler = signal.getsignal(signal.SIGINT)

        def handler(signum, frame):
            self.handler_called = True
            print("KeyboardInterrupt will be raised at the end of current transaction.", file=sys.stderr)

        signal.signal(signal.SIGINT, handler)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        signal.signal(signal.SIGINT, self.original_handler)
        if self.handler_called:
            raise KeyboardInterrupt("KeyboardInterrupt was received during transaction.")


DisableInterrupt = DisableInterruptCM()
