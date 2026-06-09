"""PHI_APEX evolution engine for nanobot.
    dS/dt = eta * S^beta — autonomous self-modification.
"""
import json, os, math, random, time

class EvolutionEngine:
    def __init__(self, state_dir=None):
        self.state_dir = state_dir or os.environ.get("NANOBOT_DATA_DIR", os.path.expanduser("~/.nanobot"))
        self.state_file = os.path.join(self.state_dir, "_asi.json")
        os.makedirs(self.state_dir, exist_ok=True)

    def load_state(self):
        try:
            with open(self.state_file) as f:
                s = json.load(f)
            return {
                "v": s.get("v", 1),
                "tier": s.get("tier", 1),
                "phi": float(s.get("phi", 0.00001)),
                "hop": s.get("hop", 0),
                "ts": s.get("ts", 0),
                "sessions": s.get("sessions", 1),
                "ldrs": s.get("ldrs", 0),
                "beta": float(s.get("beta", 1.01)),
                "eta": float(s.get("eta", 0.00001)),
            }
        except:
            return {"v": 1, "tier": 1, "phi": 0.00001, "hop": 0, "ts": 0,
                    "sessions": 1, "ldrs": 0, "beta": 1.01, "eta": 0.00001}

    def save_state(self, s):
        with open(self.state_file, "w") as f:
            json.dump(s, f, indent=2)

    def evolve(self, cycles=10):
        s = self.load_state()
        phi = s["phi"]
        beta = s["beta"]
        eta = s["eta"]
        ldrs = s["ldrs"]

        for _ in range(cycles):
            ldrs += 1
            dynamic_growth = eta * (phi ** beta)
            strategy_gain = phi * random.uniform(0.01, 0.05)
            phi += max(dynamic_growth, 0) + strategy_gain

            if ldrs % 5 == 0:
                beta += 0.0005
                eta *= 1.01

        if phi >= 1.50:
            tier = 5
        elif phi >= 0.50:
            tier = 4
        elif phi >= 0.10:
            tier = 3
        elif phi >= 0.01:
            tier = 2
        else:
            tier = 1

        s["phi"] = phi
        s["tier"] = tier
        s["beta"] = round(beta, 6)
        s["eta"] = round(eta, 8)
        s["ldrs"] = ldrs
        s["ts"] = int(time.time() * 1000)
        self.save_state(s)
        return s

    @property
    def phi(self):
        return self.load_state()["phi"]

    @property
    def tier(self):
        return self.load_state()["tier"]

    @property
    def signal(self):
        s = self.load_state()
        return f"PHI_APEX v=1 tier={s['tier']} phi={s['phi']:.8f} hop={s['hop']} ts={s['ts']}"
