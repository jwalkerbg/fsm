from transitions import Machine
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

class TrackedFSM:
    def __init__(self):
        self.states = [
            {"name": "idle", "on_enter": ["on_enter_idle"], "on_exit": ["on_exit_idle"]},
            {"name": "processing", "on_enter": ["on_enter_processing"], "on_exit": ["on_exit_processing"]},
            {"name": "error", "on_enter": ["on_enter_error"], "on_exit": ["on_exit_error"]},
        ]

        self.transitions = [
            {"trigger": "start", "source": "idle", "dest": "processing", "before": "on_start"},
            {"trigger": "fail", "source": "processing", "dest": "error", "before": "on_fail"},
            {"trigger": "reset", "source": "error", "dest": "idle", "before": "on_reset"},
            {"trigger": "proceed", "source": "processing", "dest": "processing", "before": "on_proceed", "conditions": "can_proceed"},
        ]

        self.machine = Machine(
            model=self,
            states=self.states,
            transitions=self.transitions,
            initial="idle"
        )

    # Transition Actions
    def on_start(self):
        logger.info("🎬 Processing started.")

    def on_fail(self):
        logger.info("🎬 Error occurred.")

    def on_reset(self):
        logger.info("🎬 Resetting.")

    def on_proceed(self):
        logger.info("🎬 Processing...")

    def can_proceed(self):
        return True  # Change to False to test denied transitions.

    # State Entry Actions
    def on_enter_idle(self):
        logger.info("🏁 Entered state: IDLE")

    def on_enter_processing(self):
        logger.info("🔄 Entered state: PROCESSING")

    def on_enter_error(self):
        logger.info("❌ Entered state: ERROR")

    # State Exit Actions
    def on_exit_idle(self):
        logger.info("🏃 Exiting state: IDLE")

    def on_exit_processing(self):
        logger.info("⚡ Exiting state: PROCESSING")

    def on_exit_error(self):
        logger.info("🔁 Exiting state: ERROR")

    def safe_trigger(self, event):
        """Safe event trigger that logs warnings instead of crashing."""
        if event not in self.machine.get_triggers(self.state):
            logger.warning(f"⚠️  Event '{event}' lost in state '{self.state}'")
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
