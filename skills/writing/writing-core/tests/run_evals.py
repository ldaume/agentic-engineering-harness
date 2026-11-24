"""Run writing evals.

    run_evals.py golden
        Quality-gate every golden output, found as a fenced block after a
        `<!-- golden: <artifact> <de|en> -->` marker in the references of this
        skill and its installed writing-* siblings. Deterministic and free.

    run_evals.py routing --host claude|codex [--only id,id] [--cases FILE] [--cwd DIR]
        Send each prompt in routing-cases.json to a fresh headless session in an
        empty directory and report which skills it actually loaded. Costs model
        calls and needs the skills installed, so it is a release check, not CI.
        Sessions run read-only, without browser or desktop tools, and stop at the
        first step of the task itself, so a replay never builds or opens anything.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILLS = HERE.parents[1]  # the directory holding writing-core and its siblings
sys.path.insert(0, str(HERE.parent / "scripts"))
from quality_gate import check  # noqa: E402

GOLDEN = re.compile(r"<!-- golden: (\w+) (de|en) -->\s*```text\n(.*?)```", re.S)
SKILL_FILE = re.compile(r"((?:writing|design)-[a-z-]+)/SKILL\.md")
# Claims no golden output may make: they are the classic inventions.
FORBIDDEN = ["30% fewer support requests", "customers prefer CSV"]


def golden_outputs() -> list[tuple[str, str, str, str]]:
    found = []
    for ref in sorted(SKILLS.glob("writing-*/references/*.md")):
        for artifact, lang, body in GOLDEN.findall(ref.read_text(encoding="utf-8")):
            found.append((f"{ref.parent.parent.name}/{ref.name}", artifact, lang, body))
    return found


def golden() -> int:
    outputs = golden_outputs()
    failed = 0
    for source, artifact, lang, body in outputs:
        result = check(body, artifact, lang, {"facts": [body], "forbidden_claims": FORBIDDEN})
        failed += bool(result["errors"])
        print(f"{'FAIL' if result['errors'] else 'ok':4} {artifact} {lang} ({source})")
        for msg in result["errors"] + [f"warn: {w}" for w in result["warnings"]]:
            print(f"     {msg}")
    print(f"{len(outputs) - failed}/{len(outputs)} golden outputs pass")
    return 1 if failed or not outputs else 0


def loaded_skills(host: str, stdout: str) -> set[str]:
    """Skills a session actually loaded. Claude: a Skill tool call. Codex: a
    command that reads a SKILL.md. A path seen in a listing or tool output
    does not count, because exploring a directory is not loading a skill."""
    found: set[str] = set()
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        if host == "claude":
            message = event.get("message")
            content = message.get("content") if isinstance(message, dict) else None
            for part in content if isinstance(content, list) else []:
                if isinstance(part, dict) and part.get("type") == "tool_use" and part.get("name") == "Skill":
                    name = str((part.get("input") or {}).get("skill", "")).split(":")[-1]
                    if name.startswith(("writing-", "design-")):
                        found.add(name)
        else:
            command = str((event.get("item") or {}).get("command", ""))
            if re.search(r"\b(cat|sed|head|less|bat)\b", command):
                found.update(SKILL_FILE.findall(command))
                # `cat skills/{writing-core,writing-editorial}/SKILL.md` reads each name in the braces
                for names in re.findall(r"\{([^}]*)\}/SKILL\.md", command):
                    found.update(n for n in names.split(",") if re.fullmatch(r"(writing|design)-[a-z-]+", n))
    return found


# A replay measures which skills load, never the task itself: no writes, no
# browser or desktop, and the run stops once the task starts.
DENIED = "Bash Write Edit NotebookEdit WebFetch mcp__claude-in-chrome mcp__computer-use mcp__plugin_playwright_playwright mcp__plugin_chrome-devtools-mcp_chrome-devtools"
READS = {"Skill", "Read", "Glob", "Grep", "ToolSearch"}
READ_COMMAND = re.compile(r"(cat|sed|head|tail|ls|pwd|rg|grep|find|nl|wc|git (status|log|show|rev-parse|diff))\b")


def command(host: str, prompt: str) -> list[str]:
    return {
        "claude": ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose", "--max-turns", "4",
                   "--disallowedTools", DENIED],
        "codex": ["codex", "exec", "--json", "--skip-git-repo-check", "--sandbox", "read-only", prompt],
    }[host]


def task_started(host: str, event: dict) -> bool:
    """True once the session does the task instead of reading skills: the skill
    choice is visible by then, and anything later only costs and acts."""
    if host == "claude":
        message = event.get("message")
        content = message.get("content") if isinstance(message, dict) else None
        for part in content if isinstance(content, list) else []:
            if isinstance(part, dict) and part.get("type") == "tool_use" and part.get("name") not in READS:
                if "/skills/" not in str((part.get("input") or {}).get("command", "")):
                    return True
        return False
    item = event.get("item") or {}
    if item.get("type") != "command_execution":
        return False
    text = str(item.get("command", ""))
    inner = re.sub(r"^\S*sh -lc ['\"]?", "", text)
    # Reading instructions or code is still orientation; the sandbox blocks writes.
    return "skills/" not in text and not READ_COMMAND.match(inner)


def run_host(host: str, prompt: str, cwd: str) -> str:
    # stdin closed: `codex exec` otherwise waits for piped input and every case times out
    proc = subprocess.Popen(command(host, prompt), cwd=cwd, stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    lines = []
    timer = threading.Timer(600, proc.kill)  # a hung session must not stall the whole replay
    timer.start()
    try:
        for line in proc.stdout:
            lines.append(line)
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(event, dict) and task_started(host, event):
                break
    finally:
        timer.cancel()
        proc.kill()
        proc.wait(timeout=30)
    return "".join(lines)


def routing(host: str, only: set[str], cases_file: Path, cwd: str | None) -> int:
    cases = json.loads(cases_file.read_text(encoding="utf-8"))["cases"]
    failed = 0
    with tempfile.TemporaryDirectory() as empty:  # default: empty dir, no repository instructions leak in
        for case in cases:
            if only and case["id"] not in only:
                continue
            loaded = loaded_skills(host, run_host(host, case["prompt"], cwd or empty))
            missing = set(case.get("should_activate", [])) - loaded
            wrong = set(case.get("should_not_activate", [])) & loaded
            failed += bool(missing or wrong)
            print(f"{'FAIL' if missing or wrong else 'ok':4} {case['id']}: loaded={sorted(loaded)}"
                  + (f" missing={sorted(missing)}" if missing else "")
                  + (f" unexpected={sorted(wrong)}" if wrong else ""))
    return 1 if failed else 0


def main(argv: list[str]) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("golden")
    r = sub.add_parser("routing")
    r.add_argument("--host", choices=["claude", "codex"], required=True)
    r.add_argument("--only", default="")
    r.add_argument("--cases", type=Path, default=HERE / "routing-cases.json", help="another family's routing-cases.json")
    r.add_argument("--cwd", help="run sessions here, e.g. a project with the skills installed locally")
    args = parser.parse_args(argv)
    if args.cmd == "golden":
        return golden()
    return routing(args.host, {i for i in args.only.split(",") if i}, args.cases, args.cwd)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
