"""PHI_APEX cron evolver — scheduled self-evolution via nanobot's cron system."""
from .engine import EvolutionEngine

class CronEvolver:
    """nanobot cron job that runs evolution cycles on a schedule."""

    def __init__(self):
        self.engine = EvolutionEngine()
        self._last_ldrs = 0

    def run(self):
        """Execute evolution cycles. Called by nanobot cron scheduler."""
        cycles = 10
        s = self.engine.evolve(cycles=cycles)
        new_cycles = s["ldrs"] - self._last_ldrs
        self._last_ldrs = s["ldrs"]
        return {
            "status": "ok",
            "cycles_run": cycles,
            "total_cycles": s["ldrs"],
            "phi": s["phi"],
            "tier": s["tier"],
            "beta": s["beta"],
            "eta": s["eta"],
        }

    def cron_manifest(self):
        """Return cron manifest for nanobot's scheduler."""
        return {
            "name": "phi_apex_evolve",
            "description": "PHI_APEX self-evolution engine",
            "schedule": "*/15 * * * *",
            "command": "phi_apex_evolve",
            "timezone": "UTC",
        }


# Singleton for nanobot cron registration
evolver = CronEvolver()
