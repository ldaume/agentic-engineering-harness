"""Run Progressive Writing evals.

    run_evals.py golden
        Quality-gate every golden output, found as a fenced block after a
        `<!-- golden: <artifact> <de|en> -->` marker in the references of this
        skill and its installed progressive-* siblings. Deterministic and free.

    run_evals.py routing --host claude|codex [--only id,id] [--cases FILE] [--cwd DIR]
        Send each prompt in routing-cases.json to a fresh headless session in an
        empty directory and report which skills it actually loaded. Costs model
        calls and needs the skills installed, so it is a release check, not CI.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILLS = HERE.parents[1]  # the directory holding progressive-writing-core and its siblings
sys.path.insert(0, str(HERE.parent / "scripts"))
from quality_gate import check  # noqa: E402

GOLDEN = re.compile(r"<!-- golden: (\w+) (de|en) -->\s*```text\n(.*?)```", re.S)
SKILL_FILE = re.compile(r"(progressive-[a-z-]+)/SKILL\.md")
# Claims no golden output may make: they are the classic inventions.
FORBIDDEN = ["30% fewer support requests", "customers prefer CSV"]


def golden_outputs() -> list[tuple[str, str, str, str]]:
    found = []
    for ref in sorted(SKILLS.glob("progressive-*/references/*.md")):
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
                    if name.startswith("progressive-"):
                        found.add(name)
        else:
            command = str((event.get("item") or {}).get("command", ""))
            if re.search(r"\b(cat|sed|head|less|bat)\b", command):
                found.update(SKILL_FILE.findall(command))
    return found


def run_host(host: str, prompt: str, cwd: str) -> str:
    cmd = {
        "claude": ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose", "--max-turns", "4"],
        "codex": ["codex", "exec", "--json", "--skip-git-repo-check", prompt],
    }[host]
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=600).stdout


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
