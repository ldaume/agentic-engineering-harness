#!/usr/bin/env python3
"""Report what keeps a repository from working for any coding agent on any host.

SKILL.md, Agent-Ready Audit. Needs only the repository: no coordinator, no
installed Skill, no network.

  verify-agent-ready.py [repository root, default .]

Findings (exit 1):
  bridge        an AGENTS.md without a CLAUDE.md beside it that imports @AGENTS.md
  skill-link    a Skill in .agents/skills without a .claude/skills entry
  name          a repository Skill named like a host's built-in command whose
                frontmatter does not name that /command as its neighbour
  missing       a path named in AGENTS.md or CLAUDE.md that does not exist (a
                directory counts with its trailing slash; a path under a host
                directory such as .claude/ or .agents/ is not checked, it may
                exist only after install)
  machine-path  a home-directory path (~, /Users/, /home/) from one person's machine
A missing glossary (GLOSSARY.md, or the older CONTEXT.md) is printed as a note
and does not fail: write one only for confirmed domain language. A glossary
still under its old name CONTEXT.md gets a note to rename it.

Exit 0 when clean, 1 on findings.
"""

import os
import re
import sys
from pathlib import Path

# Built-in slash commands that a same-named Skill competes with. A snapshot of
# Claude Code, Codex CLI, and Gemini CLI help output, checked 2026-11; extend it
# when a host adds commands.
BUILT_INS = {
    "agents", "clear", "compact", "config", "context", "cost", "diff", "doctor",
    "help", "hooks", "init", "login", "logout", "mcp", "memory", "model", "new",
    "permissions", "plan", "quit", "resume", "review", "security-review",
    "status", "tools",
}
# "templates" holds files this repository ships for others to copy, not its own
# instructions; a Skill's templates/ folder is never an instruction root here.
SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "build", ".venv", "templates"}
# Directories a host creates or this audit recommends creating: an instruction
# file may name them before they exist (a hint, not a finding).
HOST_DIRS = {".claude", ".agents", ".codex", ".cursor", ".gemini"}
BACKTICKS = re.compile(r"`([^`\n]+)`")
NOT_A_PATH = re.compile(r"[<>*{}$:|=@()\[\]]|^-|^https?:")
EXTENSION = re.compile(r"\.[A-Za-z][A-Za-z0-9]{0,5}$")
FENCE = re.compile(r"^\s*(```|~~~).*?^\s*\1", re.M | re.S)
HOME = ("~", "/Users/", "/home/", "/root/")


def instruction_files(root):
    for directory, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for name in ("AGENTS.md", "CLAUDE.md"):
            if name in files:
                yield Path(directory) / name


def read(path):
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def bridged(agents):
    claude = agents.with_name("CLAUDE.md")
    if not claude.exists():
        return False
    if claude.resolve() == agents.resolve():
        return True
    return any(line.strip() == "@AGENTS.md" for line in read(claude).splitlines())


def looks_like_path(token):
    # ponytail: a token needs a trailing slash (a directory) or a slash and a file
    # extension, so git refs, config keys, slash commands, and bare file names in
    # prose pass; an extensionless directory reference without a slash is not checked.
    if NOT_A_PATH.search(token.lstrip("~")):
        return False
    if token.endswith("/"):
        return token.strip("/") != ""
    return "/" in token.strip("/") and bool(EXTENSION.search(token))


def referenced_paths(text):
    """@imports, and tokens in backticks that read as a file path, outside fenced examples."""
    text = FENCE.sub("", text)
    for line in text.splitlines():
        if line.strip().startswith("@"):
            yield line.strip()[1:]
    for span in BACKTICKS.findall(text):
        for token in span.split():
            token = token.rstrip(".,;")
            if looks_like_path(token):
                yield token


def colliding_skills(root):
    """Skills named like a built-in whose SKILL.md does not name the /command."""
    names = set()
    for base in (".agents/skills", ".claude/skills"):
        directory = root / base
        if not directory.is_dir():
            continue
        for skill in directory.iterdir():
            manifest = skill / "SKILL.md"
            if skill.name in BUILT_INS and manifest.exists():
                if not re.search(rf"/{re.escape(skill.name)}(?![\w-])", read(manifest)):
                    names.add(skill.name)
    return names


def findings(root):
    root = Path(root)
    found = []
    for path in sorted(instruction_files(root)):
        relative = path.relative_to(root).as_posix()
        if path.name == "AGENTS.md" and not bridged(path):
            found.append(("bridge", relative, "no CLAUDE.md beside it imports @AGENTS.md"))
        agents = path.with_name("AGENTS.md")
        if path.name == "CLAUDE.md" and agents.exists() and path.resolve() == agents.resolve():
            continue
        for token in referenced_paths(read(path)):
            if token.startswith(HOME):
                found.append(("machine-path", relative, token))
            elif token.startswith("/"):
                continue
            elif token.split("/")[0] in HOST_DIRS:
                continue
            elif not ((path.parent / token).exists() or (root / token).exists()):
                found.append(("missing", relative, token))
    agents_skills = root / ".agents/skills"
    if agents_skills.is_dir():
        for skill in sorted(agents_skills.iterdir()):
            link = root / ".claude/skills" / skill.name
            if (skill / "SKILL.md").exists() and not link.exists():
                found.append(("skill-link", f".agents/skills/{skill.name}", f"no .claude/skills/{skill.name} entry"))
    for name in sorted(colliding_skills(root)):
        found.append(("name", name, f"same name as a host built-in; name /{name} in the description or rename"))
    return found


def glossary(root):
    for name in ("GLOSSARY.md", "CONTEXT.md"):
        if (Path(root) / name).exists():
            return name
    return None


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    found = findings(root)
    for kind, where, detail in found:
        print(f"{kind}: {where}: {detail}")
    name = glossary(root)
    if name is None:
        print("note: no glossary (GLOSSARY.md, or the older CONTEXT.md); add one when domain language is confirmed")
    elif name == "CONTEXT.md":
        print("note: the glossary is under its old name; git mv CONTEXT.md GLOSSARY.md and leave a stub that points to it")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
