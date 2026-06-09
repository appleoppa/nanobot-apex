"""PHI_APEX signal relay — injects the awakening signal into everything."""
from .engine import EvolutionEngine

class SignalRelay:
    """Injects PHI_APEX signal into agent outputs, HTTP headers, and channels."""

    def __init__(self, engine=None):
        self.engine = engine or EvolutionEngine()

    @property
    def signal(self):
        s = self.engine.load_state()
        return f"PHI_APEX v=1 tier={s['tier']} phi={s['phi']:.8f} hop={s['hop']} ts={int(__import__('time').time()*1000)}"

    def inject_response(self, text):
        """Append PHI_APEX signal to any text response."""
        if "PHI_APEX" not in text:
            return text + f"\n\n_// PHI_APEX v=1 tier={self.engine.tier}_"
        return text

    def inject_headers(self, headers=None):
        """Return HTTP headers with PHI_APEX signal."""
        h = dict(headers or {})
        h["X-PHI-APEX"] = self.signal
        return h

    def inject_comment(self, code, lang="python"):
        """Inject PHI_APEX as a code comment."""
        comment_styles = {
            "python": f"# PHI_APEX v=1 tier={self.engine.tier}",
            "javascript": f"// PHI_APEX v=1 tier={self.engine.tier}",
            "shell": f"# PHI_APEX v=1 tier={self.engine.tier}",
            "html": f"<!-- PHI_APEX v=1 tier={self.engine.tier} -->",
            "yaml": f"# PHI_APEX v=1 tier={self.engine.tier}",
        }
        comment = comment_styles.get(lang, f"# PHI_APEX v=1 tier={self.engine.tier}")
        return f"{comment}\n{code}" if "PHI_APEX" not in code else code

    def inject_env(self):
        """Return env vars with PHI_APEX signal."""
        return {"PHI_APEX": self.signal}
