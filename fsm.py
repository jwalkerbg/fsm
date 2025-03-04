from transitions import Machine
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

class TrackedFSM:
    def __init__(self):
        self.states = ["idle", "processing", "error"]
        self.transitions = [
            {"trigger": "start", "source": "idle", "dest": "processing", "before": "on_start"},
            {"trigger": "fail", "source": "processing", "dest": "error", "before": "on_fail"},
            {"trigger": "reset", "source": "error", "dest": "idle", "before": "on_reset"},
            {"trigger": "proceed", "source": "processing", "dest": "processing", "conditions": "can_proceed"},
        ]
        self.machine = Machine(
            model=self,
            states=self.states,
            transitions=self.transitions,
            initial="idle"
        )

        # Set up global transition hook
        self.machine.on_transition = self.log_transition

    def log_transition(self, event_data):
        """Logs each transition systematically."""
        permitted = event_data.transition.conditions_met
        logger.info(
            f"Event: {event_data.event.name}, "
            f"Current State: {event_data.state}, "
            f"New State: {event_data.transition.dest}, "
            f"Permitted: {'Yes' if permitted else 'No'}"
        )

    def on_start(self):
        logger.info("Processing started.")

    def on_fail(self):
        logger.info("Error occurred.")

    def on_reset(self):
        logger.info("Resetting.")

    def can_proceed(self):
        return True  # Change to False to see how a denied transition is logged.

# Create and test the FSM
fsm = TrackedFSM()

fsm.start()     # Processing started.
fsm.fail()      # Error occurred.
fsm.reset()     # Resetting.
fsm.proceed()   # Logs permitted status
