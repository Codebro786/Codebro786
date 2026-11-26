"""Shared visual identity ("Signal") for every SVG on the profile: one palette per GitHub theme."""

THEMES = {
    "dark": dict(
        bg="#0A0B1A", bg2="#0F1030", panel="#11132A", border="#23264A", grid="#1A1D3D",
        text="#E8EAFF", muted="#8A93B2", faint="#5A6185",
        violet="#8B5CF6", blue="#4F6BFF", cyan="#22D3EE", good="#5BE49B",
    ),
    "light": dict(
        bg="#F7F8FF", bg2="#ECEEFF", panel="#FFFFFF", border="#DDE1F5", grid="#E6E9FA",
        text="#12142B", muted="#5B6385", faint="#9AA1C2",
        violet="#6D3FE0", blue="#3B54E6", cyan="#0891B2", good="#16A34A",
    ),
}

SANS = "'Segoe UI', 'Inter', system-ui, -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def defs(t: dict, uid: str) -> str:
    """Common gradients; ids are prefixed so several SVGs never clash."""
    return f"""<defs>
  <linearGradient id="{uid}-accent" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{t['violet']}"/><stop offset="0.55" stop-color="{t['blue']}"/><stop offset="1" stop-color="{t['cyan']}"/>
  </linearGradient>
  <linearGradient id="{uid}-bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{t['bg']}"/><stop offset="1" stop-color="{t['bg2']}"/>
  </linearGradient>
</defs>"""
