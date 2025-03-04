from transitions import Machine
import logging

class MyFSM:
    def __init__(self):
        states = ["idle", "processing", "error"]
        transitions = [
            {"trigger": "start", "source": "idle", "dest": "processing", "before": "on_start"},
            {"trigger": "fail", "source": "processing", "dest": "error", "before": "on_fail"},
            {"trigger": "reset", "source": "error", "dest": "idle", "before": "on_reset"},
            {"trigger": "continue", "source": "processing", "dest": "processing", "conditions": "can_continue"},
        ]
        self.machine = Machine(model=self, states=states, transitions=transitions, initial="idle")

    def on_start(self):
        print("on_start: Processing started.")

    def on_fail(self):
        print("on_fail: Error occurred.")

    def on_reset(self):
        print("on_reset: Resetting.")

    def can_continue(self):
        # Guard condition example: only continue if some condition is met
        return True  # Change to False to prevent the transition

fsm = MyFSM()
fsm.start()     # Processing started.
fsm.fail()      # Error occurred.
fsm.reset()     # Resetting.
