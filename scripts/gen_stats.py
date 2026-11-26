"""Daily GitHub stats → themed SVGs (overview + streak, languages, 8-week activity). Stdlib only.

Needs GITHUB_TOKEN (the Action's built-in token is enough for public data; a fine-grained PAT with
read-only access adds private contributions if you want them counted). The token is only sent to api.github.com.
Run: GITHUB_TOKEN=... python scripts/gen_stats.py [username]   → writes assets/generated/*.svg
"""
import datetime as dt
import json
import os
import sys
import urllib.request
from theme import THEMES, SANS, MONO, esc, defs

USER = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GH_USER", "Codebro786")
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "generated")
EXCLUDE = {USER.lower()}  # the profile repo itself isn't a project

LANG_COLORS = {"Kotlin": "#A97BFF", "Python": "#3572A5", "JavaScript": "#F1E05A", "HTML": "#E34C26", "CSS": "#663399",
               "PowerShell": "#012456", "Java": "#B07219", "TypeScript": "#3178C6", "Shell": "#89E051"}


# GitHub's own colours, except ones too dark to read on the dark theme.
READABLE = {"PowerShell": "#5391FE"}


def gql(query: str, **variables):
    req = urllib.request.Request("https://api.github.com/graphql", json.dumps({"query": query, "variables": variables}).encode(),
                                 {"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "User-Agent": "profile-stats"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(f"GitHub API error: {data['errors'][0].get('message')}")
    return data["data"]


def fetch():
    q = """query($login:String!){ user(login:$login){
      createdAt followers{totalCount}
      contributionsCollection{ totalCommitContributions totalPullRequestContributions totalIssueContributions
        contributionCalendar{ totalContributions weeks{ contributionDays{ date contributionCount } } } }
      repositories(first:100, ownerAffiliations:OWNER, privacy:PUBLIC, isFork:false){ totalCount nodes{ name stargazerCount
        languages(first:10, orderBy:{field:SIZE, direction:DESC}){ edges{ size node{ name color } } } } } } }"""
    u = gql(q, login=USER)["user"]
    days = [d for w in u["contributionsCollection"]["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    langs = {}
    colors = {}
    repos = [r for r in u["repositories"]["nodes"] if r["name"].lower() not in EXCLUDE]
    for r in repos:
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]
            langs[n] = langs.get(n, 0) + e["size"]
            colors[n] = READABLE.get(n) or e["node"]["color"] or LANG_COLORS.get(n, "#888888")
    c = u["contributionsCollection"]
    return dict(created=u["createdAt"][:10], repos=len(repos), stars=sum(r["stargazerCount"] for r in repos),
                total=c["contributionCalendar"]["totalContributions"], commits=c["totalCommitContributions"],
                prs=c["totalPullRequestContributions"], days=days, langs=langs, colors=colors)


def streaks(days):
    """Current streak counts today only if today already has a contribution (else it ends yesterday)."""
    counts = [d["contributionCount"] for d in days]
    longest = run = 0
    for n in counts:
        run = run + 1 if n > 0 else 0
        longest = max(longest, run)
    cur, i = 0, len(counts) - 1
    if i >= 0 and counts[i] == 0:
        i -= 1
    while i >= 0 and counts[i] > 0:
        cur += 1; i -= 1
    active = sum(1 for n in counts if n > 0)
    return cur, longest, active


def shell(t, u, w, h, title, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">
{defs(t, u)}
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="18" fill="url(#{u}-bg)" stroke="{t['border']}"/>
<text x="36" y="52" font-family="{MONO}" font-size="19" fill="{t['faint']}" letter-spacing="1.5">{esc(title.upper())}</text>
{body}
</svg>"""


def overview(t, theme, s):
    u = f"o{theme[0]}"
    cur, longest, active = streaks(s["days"])
    since = dt.date.fromisoformat(s["created"]).strftime("%b %Y")
    tiles = [("Contributions", s["total"], "last 12 months"), ("Current streak", cur, "days"), ("Longest streak", longest, "days"),
             ("Commits", s["commits"], "last 12 months"), ("Active days", active, "last 12 months"), ("Public projects", s["repos"], f"since {since}")]
    body, tw, th = [], (1200 - 72 - 2 * 16) / 3, 136
    for i, (label, val, sub) in enumerate(tiles):
        x, y = 36 + (i % 3) * (tw + 16), 76 + (i // 3) * (th + 16)
        hi = i in (1, 2)
        body.append(f'''<rect x="{x:.0f}" y="{y}" width="{tw:.0f}" height="{th}" rx="16" fill="{t['panel']}" stroke="{t['border']}"/>
<text x="{x + 26:.0f}" y="{y + 70}" font-family="{SANS}" font-size="58" font-weight="700" fill="{f'url(#{u}-accent)' if hi else t['text']}">{val}</text>
<text x="{x + 26:.0f}" y="{y + 104}" font-family="{SANS}" font-size="23" fill="{t['text']}">{esc(label)}</text>
<text x="{tw + x - 24:.0f}" y="{y + 104}" text-anchor="end" font-family="{MONO}" font-size="17" fill="{t['faint']}">{esc(sub)}</text>''')
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%d %b %Y")
    body.append(f'<text x="1164" y="52" text-anchor="end" font-family="{MONO}" font-size="17" fill="{t["faint"]}">updated {stamp}</text>')
    return shell(t, u, 1200, 76 + 2 * th + 16 + 36, "GitHub overview", "".join(body))


def languages(t, theme, s):
    u = f"l{theme[0]}"
    total = sum(s["langs"].values()) or 1
    top = sorted(s["langs"].items(), key=lambda kv: -kv[1])[:6]
    bar, x, W = [], 36, 1128
    for n, v in top:
        w = max(6, W * v / total)
        bar.append(f'<rect x="{x:.1f}" y="78" width="{w:.1f}" height="20" fill="{s["colors"][n]}"/>')
        x += w
    legend = []
    for i, (n, v) in enumerate(top):
        cx, cy = 36 + (i % 3) * 384, 150 + (i // 3) * 46
        legend.append(f'<circle cx="{cx + 9}" cy="{cy - 8}" r="9" fill="{s["colors"][n]}"/>'
                      f'<text x="{cx + 30}" y="{cy}" font-family="{SANS}" font-size="24" fill="{t["text"]}">{esc(n)}</text>'
                      f'<text x="{cx + 350}" y="{cy}" text-anchor="end" font-family="{MONO}" font-size="21" fill="{t["muted"]}">{100 * v / total:.1f}%</text>')
    rows = (len(top) + 2) // 3
    body = f'<clipPath id="{u}-bar"><rect x="36" y="78" width="{W}" height="20" rx="10"/></clipPath><g clip-path="url(#{u}-bar)">{"".join(bar)}</g>{"".join(legend)}'
    return shell(t, u, 1200, 150 + rows * 46 + 10, "Most used languages", body)


def activity(t, theme, s):
    u = f"a{theme[0]}"
    days = s["days"][-56:]
    mx = max([d["contributionCount"] for d in days] + [1])
    step = 1128 / len(days); bw = step * 0.72
    base, hmax = 236, 150
    body = [f'<line x1="36" y1="{base + 0.5}" x2="1164" y2="{base + 0.5}" stroke="{t["border"]}"/>']
    for i, d in enumerate(days):
        n = d["contributionCount"]
        h = 4 if n == 0 else 12 + (hmax - 12) * n / mx
        fill = t["border"] if n == 0 else f"url(#{u}-accent)"
        x = 36 + i * step + (step - bw) / 2
        body.append(f'<rect x="{x:.1f}" y="{base - h:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="3" fill="{fill}"><title>{d["date"]}: {n}</title></rect>')
    first = dt.date.fromisoformat(days[0]["date"]).strftime("%d %b")
    body.append(f'<text x="36" y="270" font-family="{MONO}" font-size="17" fill="{t["faint"]}">{first}</text>'
                f'<text x="1164" y="270" text-anchor="end" font-family="{MONO}" font-size="17" fill="{t["faint"]}">today</text>'
                f'<text x="1164" y="52" text-anchor="end" font-family="{MONO}" font-size="17" fill="{t["faint"]}">peak {mx}/day</text>')
    return shell(t, u, 1200, 292, "Last 8 weeks", "".join(body))


if __name__ == "__main__":
    s = fetch()
    os.makedirs(OUT, exist_ok=True)
    for theme, t in THEMES.items():
        for name, fn in (("overview", overview), ("languages", languages), ("activity", activity)):
            with open(os.path.join(OUT, f"{name}-{theme}.svg"), "w", encoding="utf-8", newline="\n") as f:
                f.write(fn(t, theme, s))
    cur, longest, active = streaks(s["days"])
    print(f"{USER}: {s['total']} contributions, {s['commits']} commits, streak {cur}/{longest}, {s['repos']} repos, langs {list(s['langs'])[:6]}")
