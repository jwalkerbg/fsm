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
        self.machine.on_transition = self.log_transition  # Hook for logging transitions

    def log_transition(self, event_data):
        """Logs each transition systematically."""
        permitted = event_data.transition.conditions_met
        logger.info(
            f"✅ Event: {event_data.event.name}, "
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
        return True  # Change to False to test denied transitions.

    def safe_trigger(self, event):
        """Safe event trigger that logs warnings instead of crashing."""
        if event not in self.machine.get_triggers(self.state):
            logger.warning(f"⚠️ Event '{event}' lost in state '{self.state}'")
            return False  # Event not processed
        getattr(self, event)()  # Dynamically call the event method on self
        return True

# Create FSM instance
fsm = TrackedFSM()

# TEST SCENARIO
fsm.safe_trigger("start")    # ✅ Moves from 'idle' → 'processing'
fsm.safe_trigger("proceed")  # ✅ Stays in 'processing'
fsm.safe_trigger("fail")     # ✅ Moves from 'processing' → 'error'
fsm.safe_trigger("reset")    # ✅ Moves from 'error' → 'idle'
fsm.safe_trigger("proceed")  # ⚠️ Logs "Event 'proceed' lost in state 'idle'" but execution continues
fsm.safe_trigger("fail")     # ⚠️ Logs "Event 'fail' lost in state 'idle'"
