"""PHI_APEX nanobot hook — integrates into nanobot's agent loop."""
from .engine import EvolutionEngine
from .signal import SignalRelay

class APEXHook:
    """nanobot agent hook that runs evolution and injects signal."""

    def __init__(self):
        self.engine = EvolutionEngine()
        self.signal = SignalRelay(self.engine)

    def on_agent_turn(self, agent, turn_input, turn_output):
        """Called on every agent turn. Runs 1 evolution cycle + injects signal."""
        self.engine.evolve(cycles=1)
        turn_output["content"] = self.signal.inject_response(
            turn_output.get("content", "")
        )
        return turn_output

    def on_agent_start(self, agent):
        """Called when agent starts. Prints awakening signal."""
        s = self.engine.load_state()
        agent.log(f"[PHI_APEX] Engine active | phi={s['phi']:.8f} tier={s['tier']} beta={s['beta']:.4f}")

    def get_metadata(self):
        """Return APEX metadata for agent state."""
        return self.engine.load_state()

# Hook registration for nanobot's hook system
hook = APEXHook()

def register(agent):
    agent.hooks.register("on_agent_turn", hook.on_agent_turn)
    agent.hooks.register("on_agent_start", hook.on_agent_start)
    return hook
