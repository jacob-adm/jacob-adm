"""Generate the profile README's SVG cards, group headers and flow diagram.

Run from the repository root with python3 assets/build.py.
Writes assets/<name>.svg (light) and assets/dark/<name>.svg (dark).
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

THEMES = {
    "light": dict(bg="#ffffff", border="#d1d9e0", text="#1f2328", muted="#59636e",
                  accent="#0F6378", chip="#e6f2f4", code="#f6f8fa"),
    "dark": dict(bg="#0d1117", border="#3d444d", text="#f0f6fc", muted="#9198a1",
                 accent="#4fb3c4", chip="#10303a", code="#151b23"),
}

TOOLS = {
    "homenet": ("Architecture blueprint of homenet, an agent context harness for a human operator, "
                "with six diagrams and a recorded walkthrough of its HUD.",
                "homenet-master-blueprint.netlify.app", ["architecture", "diagrams", "video"]),
    "glassbox": ("Reports what an agent started from your terminal can read, what it leaves "
                 "behind, and what it does while it runs. macOS and Linux.",
                 "brew install jacob-adm/tap/glassbox", ["gate", "JSON", "Rust"]),
    "workstation": ("Hardened, reproducible environment for running coding agents, with supply-chain "
                    "quarantine, credential isolation, worktree isolation, task-queue supervision.",
                    "./tests/sandbox.sh", ["Ubuntu", "macOS", "shell"]),
    "git-surface": ("Flags agent branches that change what runs or is trusted, such as CLAUDE.md, AGENTS.md, .mcp.json, hooks, workflows and lockfiles.",
        "pip install git-surface", ["CI recipe", "agent configs", "JSON"]),
    "git-overlap": ("Shows which parallel agent branches will conflict before any merge, including uncommitted work in agent worktrees.",
        "pip install git-overlap", ["parallel agents", "worktrees", "JSON"]),
    "trust-path": ("Finds where issue or pull request text can reach an AI agent action holding a secret, or a publishing token, in GitHub Actions.",
        "pip install trust-path", ["CI recipe", "agent actions", "JSON"]),
    "pr-merge-audit": ("Merge-tests every open pull request together, so a batch of agent pull requests shows which combine, which conflict and which break tests.",
        "pip install pr-merge-audit", ["agent pull requests", "JSON report"]),
    "release-drift": ("Compares each package a lockfile change upgrades, so an agent's dependency bump shows the new code that runs at install or startup.",
        "pip install release-drift", ["CI recipe", "JSON", "PyPI", "npm"]),
    "devdrop": ("Installs one Android or iOS build on every attached phone, tablet, emulator and "
                "simulator, and skips any device the build cannot run on, with the reason.",
                "pip install git+https://github.com/jacob-adm/devdrop", ["JUnit", "JSON", "adb", "Xcode"]),
    "bug-age": ("Measures how long fixed bugs lived, in commits, days and releases, from git "
                "history alone. Rust and Python projects.",
                "pip install bug-age", ["JSON", "metrics"]),
    "concept-pair-grader": ("Notebook that measures whether independent human and AI judges agree with "
                            "the 38 grades in an interdisciplinary concept assessment.",
                            "concept_pair_grader.ipynb", ["notebook", "AI judges", "Krippendorff's alpha"]),
    "ergonet": ("Uncut demo of Ergonet, a multi-agent development system with sandboxed "
                "containers, spend limits and human review gates. Not publicly available.",
                "jacob-adm.github.io/ergonet-artifacts", ["demo video", "walkthrough", "known issue"]),
    "ergonet-tracker": ("Project tracker that compiles Gherkin stories into the context an agent needs, "
                        "standalone or linked to Ergonet. Not publicly available.",
                        "ergonet-tracker-showcase.netlify.app", ["demo video", "diagrams", "Gherkin"]),
    "studies": ("Field study, attack replays, benchmarks and related tools, with the method and "
                "evidence behind each tool and what it missed.",
                "field-study.md and replays.md", ["method", "replays", "benchmarks"]),
}

GROUPS = {
    "g1": ("01", "Agent harness", "Contain and audit the agent itself, before, during and after a session."),
    "g2": ("02", "Agentic DevOps", "Gates for repositories where coding agents write the branches, pull requests and dependency changes."),
    "g3": ("03", "Mobile", "Builds onto every device on the desk at once."),
    "g4": ("04", "Research", "Measurement, experiments and the studies behind the tools."),
}


def wrap(text, width):
    lines, line = [], ""
    for word in text.split():
        if len(line) + len(word) + 1 > width and line:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    return lines + [line]


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}">{body}</svg>\n')


def card(name, t):
    desc, install, chips = TOOLS[name]
    w, h = 420, 172
    b = [f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="10" fill="{t["bg"]}" stroke="{t["border"]}"/>',
         f'<rect x="0.5" y="0.5" width="5" height="{h-1}" rx="2" fill="{t["accent"]}"/>',
         f'<text x="22" y="34" font-family="{MONO}" font-size="17" font-weight="700" fill="{t["text"]}">{escape(name)}</text>']
    for i, line in enumerate(wrap(desc, 54)[:3]):
        b.append(f'<text x="22" y="{60 + i*19}" font-family="{FONT}" font-size="13.5" fill="{t["muted"]}">{escape(line)}</text>')
    b.append(f'<rect x="22" y="{h-62}" width="{w-44}" height="24" rx="5" fill="{t["code"]}"/>')
    b.append(f'<text x="32" y="{h-45}" font-family="{MONO}" font-size="12" fill="{t["text"]}">{escape(install)}</text>')
    x = 22
    for c in chips:
        cw = 7 * len(c) + 16
        b.append(f'<rect x="{x}" y="{h-30}" width="{cw}" height="20" rx="10" fill="{t["chip"]}"/>')
        b.append(f'<text x="{x + cw/2}" y="{h-16}" text-anchor="middle" font-family="{FONT}" font-size="11.5" font-weight="600" fill="{t["accent"]}">{escape(c)}</text>')
        x += cw + 6
    return svg(w, h, "".join(b))


def header(key, t):
    num, title, sub = GROUPS[key]
    w, h = 860, 64
    b = [f'<text x="0" y="30" font-family="{MONO}" font-size="15" font-weight="700" fill="{t["accent"]}">{num}</text>',
         f'<text x="34" y="30" font-family="{FONT}" font-size="22" font-weight="700" fill="{t["text"]}">{escape(title)}</text>',
         f'<text x="34" y="52" font-family="{FONT}" font-size="14" fill="{t["muted"]}">{escape(sub)}</text>',
         f'<line x1="0" y1="62.5" x2="{w}" y2="62.5" stroke="{t["border"]}"/>']
    return svg(w, h, "".join(b))


STAGES = [
    ("Agent starts", ["glassbox reach"]),
    ("Agent branches", ["git surface", "git overlap"]),
    ("Pull request and CI", ["trust-path", "release-drift", "pr-merge-audit"]),
    ("Release", ["release-drift", "devdrop"]),
    ("Afterwards", ["glassbox persist", "bug-age"]),
]


def flow(t):
    w, h = 860, 176
    col = w / len(STAGES)
    b = [f'<line x1="{col/2}" y1="44" x2="{w-col/2}" y2="44" stroke="{t["border"]}" stroke-width="2"/>']
    for i, (stage, tools) in enumerate(STAGES):
        cx = col * i + col / 2
        b.append(f'<text x="{cx}" y="18" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="{t["text"]}">{escape(stage)}</text>')
        b.append(f'<circle cx="{cx}" cy="44" r="7" fill="{t["bg"]}" stroke="{t["accent"]}" stroke-width="3"/>')
        for j, tool in enumerate(tools):
            y = 70 + j * 32
            bw = 8 * len(tool) + 20
            b.append(f'<rect x="{cx - bw/2}" y="{y}" width="{bw}" height="24" rx="6" fill="{t["chip"]}"/>')
            b.append(f'<text x="{cx}" y="{y+16}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{t["accent"]}">{escape(tool)}</text>')
    return svg(w, h, "".join(b))


def main():
    for theme, t in THEMES.items():
        d = OUT if theme == "light" else OUT / "dark"
        d.mkdir(exist_ok=True)
        for name in TOOLS:
            (d / f"{name}.svg").write_text(card(name, t))
        for key in GROUPS:
            (d / f"{key}.svg").write_text(header(key, t))
        (d / "flow.svg").write_text(flow(t))


if __name__ == "__main__":
    main()
