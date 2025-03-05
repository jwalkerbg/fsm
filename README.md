# fsm

This project implements a finite state machine (FSM) using the `transitions` library in Python. The FSM is defined in the `fsm.py` file.

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

The safe_trigger method is used to safely trigger events and log warnings if the event is not valid in the current state.
