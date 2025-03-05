# fsm

This project implements a finite state machine (FSM) using the `transitions` library in Python. The FSM is defined in the `fsm.py` file.

## Installation

To install the required dependencies, run the following command:

```sh
pip install transitions
```

## `fsm.py`

The `fsm.py` file contains the `TrackedFSM` class, which defines the states, transitions, and actions for the FSM. The FSM has three states: `idle`, `processing`, and `error`. It also defines transitions between these states with associated actions.

### States

- `idle`: Initial state.
- `processing`: State when processing is ongoing.
- `error`: State when an error occurs.

### Transitions

- `start`: Triggered to move from `idle` to `processing`.
- `fail`: Triggered to move from `processing` to `error`.
- `reset`: Triggered to move from `error` to `idle`.
- `proceed`: Triggered to stay in `processing` if conditions are met.

### Actions

- `on_start`: Action before transitioning from `idle` to `processing`.
- `on_fail`: Action before transitioning from `processing` to `error`.
- `on_reset`: Action before transitioning from `error` to `idle`.
- `on_proceed`: Action before staying in `processing`.

### Usage

To create an instance of the FSM and trigger events, use the following code:

```python
from fsm import TrackedFSM

fsm = TrackedFSM()

fsm.safe_trigger("start")    # Moves from 'idle' to 'processing'
fsm.safe_trigger("proceed")  # Stays in 'processing'
fsm.safe_trigger("fail")     # Moves from 'processing' to 'error'
fsm.safe_trigger("reset")    # Moves from 'error' to 'idle'
fsm.safe_trigger("proceed")  # Logs "Event 'proceed' lost in state 'idle'"
fsm.safe_trigger("fail")     # Logs "Event 'fail' lost in state 'idle'"
```

### `safe_trigger` Method

The `safe_trigger` method is used to safely trigger events and log warnings if the event is not valid in the current state. This method is necessary to prevent the FSM from transitioning to an invalid state and to provide clear logging for debugging purposes.

#### Why it is needed

In a finite state machine, certain events are only valid in specific states. Triggering an event that is not valid in the current state can lead to unexpected behavior or errors. The `safe_trigger` method ensures that only valid events are triggered, and it logs a warning if an invalid event is attempted. This helps maintain the integrity of the FSM and makes it easier to debug issues.

Without the `safe_trigger` method, the `transitions` library will raise an exception if an invalid event is triggered in the current state. This can cause the program to crash or require additional exception handling code to manage these errors. The `safe_trigger` method provides a safer and more user-friendly way to handle invalid events by logging warnings instead of raising exceptions.

The line `getattr(self, event)()` dynamically calls a method on the `self` object based on the `event` string. Here's a breakdown of how it works:

1. **`getattr(self, event)`**: This function retrieves an attribute (in this case, a method) from the `self` object. The attribute's name is specified by the `event` string. For example, if `event` is `"start"`, `getattr(self, "start")` will return the `start` method of the `self` object.

2. **`()`**: This part calls the method retrieved by `getattr`. So, if `getattr(self, "start")` returns the `start` method, `getattr(self, "start")()` will call the `start` method.

In the context of the `safe_trigger` method, this line is used to dynamically call the appropriate event method (like `start`, `fail`, `reset`, etc.) on the `TrackedFSM` instance.

Here's an example to illustrate:

```python
class Example:
    def __init__(self):
        self.state = "idle"

    def start(self):
        print("Starting...")

    def fail(self):
        print("Failing...")

    def trigger_event(self, event):
        getattr(self, event)()

example = Example()
example.trigger_event("start")  # Output: Starting...
example.trigger_event("fail")   # Output: Failing...
```

In this example, `trigger_event` dynamically calls the `start` and `fail` methods based on the `event` string passed to it.

The getattr(self, event)() call in the safe_trigger method dynamically calls the method on the TrackedFSM instance that corresponds to the event name. This is possible because the transitions library uses the methods defined in the TrackedFSM class to handle state transitions and actions.

Here's how it works in detail:

State Machine Setup: When the TrackedFSM instance is created, the transitions library sets up the state machine with the states, transitions, and actions defined in the __init__ method.

Event Triggering: When an event is triggered using the safe_trigger method, the method first checks if the event is valid in the current state using self.machine.get_triggers(self.state). If the event is valid, it dynamically calls the corresponding method using getattr(self, event)().

Method Execution: The dynamically called method (e.g., start, fail, reset, proceed) is executed. These methods are defined in the TrackedFSM class and are responsible for performing the actions associated with the transitions.

State Transition: The transitions library then handles the state transition based on the event and the current state. It uses the methods defined in the TrackedFSM class (e.g., on_start, on_fail, on_reset, on_proceed) to perform actions before and after the state transition.

Here's an example to illustrate:

```
# Create FSM instance
fsm = TrackedFSM()

# Trigger the 'start' event
fsm.safe_trigger("start")  # Moves from 'idle' to 'processing'

# The 'start' event is valid in the 'idle' state, so the 'on_start' method is called
# The state transitions from 'idle' to 'processing'
# The 'on_enter_processing' method is called when entering the 'processing' state
```

In this example, when the start event is triggered, the safe_trigger method calls the start method on the TrackedFSM instance. The transitions library then handles the state transition from idle to processing and calls the appropriate methods (on_start, on_enter_processing) to perform the actions associated with the transition.

The transitions library uses the methods defined in the TrackedFSM class to handle state transitions and actions, ensuring that the FSM behaves as expected based on the defined states, transitions, and actions.