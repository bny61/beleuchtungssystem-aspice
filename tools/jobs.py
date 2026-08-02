#!/usr/bin/env python3
"""Capture tasks from the requirements browser and run them through the Claude Code CLI.

A *job* is a working note that produces work: something noticed while reading a requirement,
an analysis or a diagram, written down against that element and handed to the subagent that
owns it. Jobs live as records in 09_process/jobs/ and are committed, so what was asked and
what came back stay visible.

A job is NOT a replacement for an open point (`OP-xx`) or a GitHub issue. Those are the
project's tracking mechanisms; a job carries an optional `relates_to` pointing at one.

Nothing is changed until a plan has been written, read and approved:

    open --plan--> planned --approve--> approved --run--> done

Commands:
    python3 tools/jobs.py serve [--port 8787]   serve the repo and accept jobs from the page
    python3 tools/jobs.py list [--all]          open jobs (--all includes finished ones)
    python3 tools/jobs.py show JOB-001
    python3 tools/jobs.py adopt                     take hand-placed jobs into the numbering
    python3 tools/jobs.py plan JOB-001 [--replan]    agent states its intent, read-only
    python3 tools/jobs.py approve JOB-001           after you have read and edited the plan
    python3 tools/jobs.py run JOB-001 [--dry-run] [--yes] [--model ...]

Standard library only, like the other tools here, which keeps the tool-qualification
argument small (ISO 26262-8, Clause 11) - see 09_process/plans/tool_qualification.md.

SAFETY: a job file is data that becomes an instruction to an agent. `run` therefore always
prints the job and the exact command and waits for confirmation. The server binds to
loopback only and never accepts a path from the client. Do not run a job that arrived from
someone else without reading it first, and do not run jobs in CI.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trace_check import parse_front_matter  # noqa: E402

JOBS_REL = "09_process/jobs"
AGENTS_REL = ".claude/agents"
BROWSER_REL = "07_verification/reports/requirements_browser.html"

# open --plan--> planned --approve--> approved --run--> done | failed
STATUSES = ("open", "planned", "approved", "running", "done", "failed", "dropped")
TARGET_KINDS = ("record", "document", "diagram", "area", "general")

MAX_PROMPT = 8000
MAX_FIELD = 500
MAX_CONTEXT = 20000

# Print mode still needs a permission decision for file edits. acceptEdits is the useful
# default for a job that has just been confirmed by a human and runs on its own branch; it
# is always shown in the printed command, never applied silently.
DEFAULT_PERMISSION_MODE = "acceptEdits"

# The generated page falls back to this port when it was opened from disk rather than
# served, so the two must agree. It is defined here and imported by gen_req_browser.py.
DEFAULT_PORT = 8787


# --------------------------------------------------------------------------- helpers


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def known_agents(root: Path) -> list[dict]:
    """Agent name and one-line description from .claude/agents/*.md."""
    out = []
    base = root / AGENTS_REL
    if not base.is_dir():
        return out
    for path in sorted(base.glob("*.md")):
        fm = parse_front_matter(path.read_text(encoding="utf-8")) or {}
        desc = str(fm.get("description", "")).strip()
        out.append({
            "name": str(fm.get("name", path.stem)).strip() or path.stem,
            "description": desc[:200],
        })
    return out


def job_files(root: Path) -> list[Path]:
    base = root / JOBS_REL
    return sorted(base.glob("JOB-*.md")) if base.is_dir() else []


def record_body(text: str) -> str:
    """Everything after the closing front-matter delimiter.

    Written out rather than chained splits: the body contains no "---" of its own, so a
    split-based version raised IndexError on every well-formed job record.
    """
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    if end == -1:
        return ""
    return text[end + 4:].lstrip("\n")


def split_body(body: str) -> tuple[str, str, str]:
    """Return (task, context, plan) from a job body.

    The plan is a section of the record on purpose: reviewing it is opening the file, and
    editing it needs no tool of ours.
    """
    rest, plan = (body.split("## Plan", 1) + [""])[:2]
    task, context = (rest.split("## Context", 1) + [""])[:2]
    return (task.replace("## Task", "", 1).strip(), context.strip(), plan.strip())


def load_jobs(root: Path) -> list[dict]:
    jobs = []
    for path in job_files(root):
        text = path.read_text(encoding="utf-8")
        fm = parse_front_matter(text) or {}
        if "id" not in fm:
            continue
        fm["_file"] = str(path.relative_to(root))
        fm["_body"] = record_body(text)
        jobs.append(fm)
    return sorted(jobs, key=lambda j: str(j["id"]))


def next_job_id(root: Path, ignore: Path | None = None) -> str:
    """Lowest free JOB number.

    `ignore` leaves a file out of the scan, which adopt needs: a file already named
    JOB-003.md was counting itself as taken and being bumped to JOB-004, leaving a gap in
    a numbering the user had chosen correctly.
    """
    used = set()
    for path in job_files(root):
        if ignore is not None and path == ignore:
            continue
        m = re.match(r"JOB-(\d+)", path.stem)
        if m:
            used.add(int(m.group(1)))
    n = 1
    while n in used:
        n += 1
    return f"JOB-{n:03d}"


def yaml_scalar(value: str) -> str:
    """Quote a scalar when it could otherwise be misread as YAML."""
    s = str(value)
    if s == "":
        return '""'
    if re.search(r'[:#\[\]{}"\'\n]|^\s|\s$', s):
        return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'
    return s


def write_job(root: Path, data: dict, path: Path | None = None) -> Path:
    """Write a job record. Content comes from the caller; a path only from this module."""
    jid = data["id"]
    path = path or (root / JOBS_REL / f"{jid}.md")
    path.parent.mkdir(parents=True, exist_ok=True)

    rel = data.get("relates_to") or []
    lines = [
        "---",
        f"id: {jid}",
        f"created: {data.get('created') or datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"status: {data.get('status', 'open')}",
        f"target: {yaml_scalar(data.get('target', ''))}",
        f"target_kind: {data.get('target_kind', 'general')}",
        f"agent: {yaml_scalar(data.get('agent', ''))}",
        "relates_to: " + ("[]" if not rel else "[" + ", ".join(str(r) for r in rel) + "]"),
        f"planned_at: {yaml_scalar(data.get('planned_at', ''))}",
        f"approved_at: {yaml_scalar(data.get('approved_at', ''))}",
        f"branch: {yaml_scalar(data.get('branch', ''))}",
        f"result: {yaml_scalar(data.get('result', ''))}",
        "---",
        "",
        "## Task",
        "",
        data.get("prompt", "").strip(),
        "",
    ]
    context = (data.get("context") or "").strip()
    if context:
        lines += ["## Context", "", context, ""]
    plan = (data.get("plan") or "").strip()
    if plan:
        lines += ["## Plan", "", plan, ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def job_path(root: Path, jid: str) -> Path:
    """The file a job actually lives in.

    Not simply JOBS_REL/<id>.md: a job downloaded from the browser carries the placeholder
    id JOB-xxx and whatever filename you saved it under. Deriving the path from the id wrote
    a second record and orphaned the original.
    """
    for path in job_files(root):
        fm = parse_front_matter(path.read_text(encoding="utf-8")) or {}
        if str(fm.get("id", "")).strip() == jid:
            return path
    return root / JOBS_REL / f"{jid}.md"


def update_job(root: Path, jid: str, **changes) -> None:
    """Rewrite a job record with changed front-matter fields, keeping the body."""
    path = job_path(root, jid)
    text = path.read_text(encoding="utf-8")
    fm = parse_front_matter(text) or {}
    task, context, plan = split_body(record_body(text))

    data = {
        "id": jid,
        "created": fm.get("created", ""),
        "status": fm.get("status", "open"),
        "target": fm.get("target", ""),
        "target_kind": fm.get("target_kind", "general"),
        "agent": fm.get("agent", ""),
        "relates_to": fm.get("relates_to", []),
        "planned_at": fm.get("planned_at", ""),
        "approved_at": fm.get("approved_at", ""),
        "branch": fm.get("branch", ""),
        "result": fm.get("result", ""),
        "prompt": task,
        "context": context,
        "plan": plan,
    }
    data.update(changes)
    write_job(root, data, path)


def validate(root: Path, payload: dict) -> tuple[dict | None, str]:
    """Check a job posted by the page. Returns (clean, error)."""
    prompt = str(payload.get("prompt", "")).strip()
    if not prompt:
        return None, "the task text is empty"
    if len(prompt) > MAX_PROMPT:
        return None, f"the task text exceeds {MAX_PROMPT} characters"

    agent = str(payload.get("agent", "")).strip()
    if agent and agent not in {a["name"] for a in known_agents(root)}:
        return None, f"unknown agent '{agent}'"

    kind = str(payload.get("target_kind", "general")).strip() or "general"
    if kind not in TARGET_KINDS:
        return None, f"unknown target kind '{kind}'"

    target = str(payload.get("target", "")).strip()
    if len(target) > MAX_FIELD:
        return None, "target too long"

    # relates_to is the human's decision to act on an agent's open point, so it has to
    # survive the round trip. Constrained to id-shaped tokens: it ends up in YAML.
    relates = payload.get("relates_to") or []
    if isinstance(relates, str):
        relates = re.split(r"[,\s]+", relates)
    relates = [r for r in (str(x).strip() for x in relates)
               if r and re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]{0,30}", r)][:10]

    return {
        "prompt": prompt,
        "agent": agent,
        "target": target,
        "target_kind": kind,
        "relates_to": relates,
        "context": str(payload.get("context", ""))[:MAX_CONTEXT],
        "status": "open",
    }, ""


# ---------------------------------------------------------------------------- serve


def make_handler(root: Path):
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(root), **kw)

        def log_message(self, fmt, *args):  # quieter than the default
            if self.command == "POST":
                sys.stderr.write("  %s\n" % (fmt % args))

        def _json(self, code: int, payload: dict) -> None:
            body = json.dumps(payload).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            # Allows the page to post when it was opened from file:// (origin "null").
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):  # noqa: N802
            if self.path.rstrip("/") == "/api/agents":
                return self._json(200, {"agents": known_agents(root)})
            if self.path.rstrip("/") == "/api/jobs":
                return self._json(200, {"jobs": [
                    {k: v for k, v in j.items() if not k.startswith("_")} for j in load_jobs(root)
                ]})
            return super().do_GET()

        def do_POST(self):  # noqa: N802
            if self.path.rstrip("/") != "/api/jobs":
                return self._json(404, {"error": "unknown endpoint"})
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length <= 0 or length > MAX_PROMPT + MAX_CONTEXT + 4096:
                    return self._json(413, {"error": "payload size not accepted"})
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
            except (ValueError, UnicodeDecodeError) as exc:
                return self._json(400, {"error": f"malformed request: {exc}"})

            clean, err = validate(root, payload)
            if clean is None:
                return self._json(400, {"error": err})

            clean["id"] = next_job_id(root)
            path = write_job(root, clean)
            print(f"  + {clean['id']}  {clean['target'] or '(no target)'}"
                  f"  -> {path.relative_to(root)}", file=sys.stderr)
            return self._json(201, {"id": clean["id"], "file": str(path.relative_to(root))})

    return Handler


def cmd_serve(root: Path, args) -> int:
    handler = make_handler(root)
    # Loopback only. This process writes files into the repository; it must never be
    # reachable from another machine.
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    url = f"http://127.0.0.1:{args.port}/{BROWSER_REL}"
    print(f"Serving {root}")
    print(f"  browser : {url}")
    print(f"  jobs    : {JOBS_REL}/")
    print("  Ctrl-C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()
    return 0


# ----------------------------------------------------------------------- list / show


def cmd_list(root: Path, args) -> int:
    jobs = load_jobs(root)
    if not args.all:
        jobs = [j for j in jobs if j.get("status") in ("open", "running")]
    if not jobs:
        print("No jobs." if args.all else "No open jobs.")
        return 0
    width = max(len(str(j["id"])) for j in jobs)
    for j in jobs:
        target = str(j.get("target", "")) or "-"
        agent = str(j.get("agent", "")) or "(default)"
        print(f"{str(j['id']):<{width}}  {str(j.get('status','')):<8}  {target:<32}  {agent}")
    return 0


def cmd_show(root: Path, args) -> int:
    path = root / JOBS_REL / f"{args.job}.md"
    if not path.is_file():
        print(f"No such job: {args.job}", file=sys.stderr)
        return 2
    print(path.read_text(encoding="utf-8"))
    return 0


# ------------------------------------------------------------------------------ run


def compose_prompt(job: dict) -> str:
    """Task text plus a preamble naming what it is about.

    CLAUDE.md is loaded by the CLI itself, so the project rules are not restated here.
    """
    parts = []
    target = str(job.get("target", "")).strip()
    if target:
        parts.append(
            f"This task concerns {target} "
            f"({job.get('target_kind', 'element')}) of the lighting-system project."
        )
    body = str(job.get("_body", ""))
    if "## Context" in body:
        context = body.split("## Context", 1)[1].strip()
        if context:
            parts.append("Context captured when the task was written:\n" + context)
    parts.append(str(job.get("_task", "")).strip())
    plan = str(job.get("_plan", "")).strip()
    if plan:
        parts.append(
            "This plan was reviewed and approved by the human who wrote the task. Follow it.\n"
            "If you find it wrong or incomplete, STOP and report that instead of improvising - "
            "silently doing something else defeats the point of the approval.\n\n" + plan
        )
    parts.append(
        "Do not commit or push. Leave the changes in the working tree for review, and "
        "finish by summarising what you changed and anything you deliberately left out."
    )
    return "\n\n".join(p for p in parts if p)


def invoke(root: Path, cmd: list[str]) -> tuple[bool, str]:
    """Run the CLI and return (ok, text). The JSON envelope carries the reply in 'result'."""
    proc = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
    out = proc.stdout.strip()
    text = out
    try:
        parsed = json.loads(out)
        if isinstance(parsed, dict):
            text = str(parsed.get("result", out))
    except ValueError:
        pass
    return proc.returncode == 0, (text or proc.stderr.strip())


def base_cmd(job: dict, args, permission_mode: str) -> list[str]:
    cmd = ["claude", "-p", "--output-format", "json", "--permission-mode", permission_mode]
    agent = str(job.get("agent", "")).strip()
    if agent:
        cmd += ["--agent", agent]
    if getattr(args, "model", None):
        cmd += ["--model", args.model]
    return cmd


PLACEHOLDER = re.compile(r"^JOB-\d{3,}$")


def cmd_adopt(root: Path, args) -> int:
    """Take jobs that arrived by hand into the numbering.

    The browser cannot know the next free number while it is offline, so a downloaded job
    carries `id: JOB-xxx` and whatever filename you saved it under. This assigns the next
    free id, renames the file to match and rewrites the record.
    """
    stray = []
    for path in job_files(root):
        fm = parse_front_matter(path.read_text(encoding="utf-8")) or {}
        jid = str(fm.get("id", "")).strip()
        if not PLACEHOLDER.match(jid) or path.stem != jid:
            stray.append((path, jid))

    if not stray:
        print("Every job has a proper id and matching filename.")
        return 0

    for path, jid in stray:
        text = path.read_text(encoding="utf-8")
        task, context, plan = split_body(record_body(text))
        fm = parse_front_matter(text) or {}
        # Keep the number the file was already named with when it is free.
        stem_ok = re.match(r"^JOB-\d{3,}$", path.stem)
        candidate = path.stem if stem_ok else None
        free = next_job_id(root, ignore=path)
        new_id = candidate if candidate and candidate <= free else free
        target = root / JOBS_REL / f"{new_id}.md"

        data = {k: fm.get(k, "") for k in
                ("created", "status", "target", "target_kind", "agent",
                 "planned_at", "approved_at", "branch", "result")}
        data.update({"id": new_id, "relates_to": fm.get("relates_to", []),
                     "prompt": task, "context": context, "plan": plan})
        write_job(root, data, target)
        if path != target:
            path.unlink()
        print(f"{path.name}  (id {jid or 'missing'})  ->  {new_id}   {target.relative_to(root)}")

    print("\nNext: python3 tools/jobs.py plan <id>")
    return 0


def cmd_plan(root: Path, args) -> int:
    """Ask the agent what it intends to do, without letting it do any of it."""
    jobs = {str(j["id"]): j for j in load_jobs(root)}
    if args.job not in jobs:
        print(f"No such job: {args.job}", file=sys.stderr)
        return 2
    job = jobs[args.job]
    task, _ctx, existing = split_body(str(job.get("_body", "")))
    job["_task"] = task

    if existing and not args.replan:
        print(f"{args.job} already has a plan. Edit it, then approve - or use --replan.",
              file=sys.stderr)
        return 2
    if not shutil.which("claude"):
        print("The 'claude' CLI was not found on PATH.", file=sys.stderr)
        return 2

    prompt = (
        compose_prompt(job)
        + "\n\nProduce a PLAN only. State what you would change, which files and IDs, which "
          "values, what you would deliberately not touch, and anything that needs deciding "
          "first. Do not change anything. Keep it proportional to the task."
    )
    # plan mode is read-only: the agent cannot write even if it decides to.
    cmd = base_cmd(job, args, "plan") + [prompt]
    print(f"Planning {args.job} ({job.get('agent') or 'default agent'}) - read-only ...\n")
    ok, text = invoke(root, cmd)
    print(text)
    if not ok:
        update_job(root, args.job, status="open")
        print(f"\n{args.job} -> planning failed, still open", file=sys.stderr)
        return 1

    update_job(root, args.job, status="planned", plan=text,
               planned_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
               approved_at="")
    print(f"\n{args.job} -> planned")
    print(f"Review and edit:  {JOBS_REL}/{args.job}.md   (## Plan section)")
    print(f"Then:             python3 tools/jobs.py approve {args.job}")
    return 0


def cmd_approve(root: Path, args) -> int:
    """Record that a human read the plan and accepted it."""
    jobs = {str(j["id"]): j for j in load_jobs(root)}
    if args.job not in jobs:
        print(f"No such job: {args.job}", file=sys.stderr)
        return 2
    job = jobs[args.job]
    _task, _ctx, plan = split_body(str(job.get("_body", "")))
    if not plan:
        print(f"{args.job} has no plan yet. Run: python3 tools/jobs.py plan {args.job}",
              file=sys.stderr)
        return 2
    if job.get("status") == "approved":
        print(f"{args.job} is already approved.")
        return 0

    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    update_job(root, args.job, status="approved", approved_at=stamp)
    print(f"{args.job} -> approved  {stamp}")
    print(f"Then: python3 tools/jobs.py run {args.job}")
    return 0


def cmd_run(root: Path, args) -> int:
    jobs = {str(j["id"]): j for j in load_jobs(root)}
    if args.job not in jobs:
        print(f"No such job: {args.job}", file=sys.stderr)
        return 2
    job = jobs[args.job]

    if len(job_files(root)) != len({p.stem for p in job_files(root)}):
        print("Duplicate job ids present; resolve them before running.", file=sys.stderr)
        return 2

    task, _context, plan = split_body(str(job.get("_body", "")))
    job["_task"] = task
    job["_plan"] = plan

    status = job.get("status")
    # The gate: work only ever follows a plan a human read and accepted.
    if status == "open":
        print(f"{args.job} has no plan. Run: python3 tools/jobs.py plan {args.job}",
              file=sys.stderr)
        return 2
    if status == "planned":
        print(f"{args.job} has a plan that is not approved. Review "
              f"{JOBS_REL}/{args.job}.md, then: python3 tools/jobs.py approve {args.job}",
              file=sys.stderr)
        return 2
    if status in ("done", "running") and not args.force:
        print(f"{args.job} is '{status}'. Re-run with --force if that is intended.",
              file=sys.stderr)
        return 2
    if status not in ("approved", "failed") and not args.force:
        print(f"{args.job} is '{status}'; only an approved job runs.", file=sys.stderr)
        return 2

    if not shutil.which("claude"):
        print("The 'claude' CLI was not found on PATH.", file=sys.stderr)
        return 2

    prompt = compose_prompt(job)
    agent = str(job.get("agent", "")).strip()
    branch = f"job/{args.job}"

    cmd = base_cmd(job, args, args.permission_mode) + [prompt]

    print(f"\n{args.job}  target {job.get('target') or '-'}  agent {agent or '(default)'}"
          f"  approved {job.get('approved_at') or '-'}")
    print("\n  " + "\n  ".join(task.splitlines()))
    print("\nwill run:")
    printable = list(cmd[:-1]) + ["<composed prompt>"]
    print("  " + " ".join(printable))
    print(f"  on branch {branch}, changes left uncommitted\n")

    if args.dry_run:
        print("Dry run - nothing executed.")
        return 0

    if not args.yes:
        try:
            answer = input("run this? [y/N] ").strip().lower()
        except EOFError:
            answer = ""
        if answer not in ("y", "yes"):
            print("Not run.")
            return 0

    # Own branch, so a job never mixes with whatever was in progress.
    current = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                             cwd=root, capture_output=True, text=True).stdout.strip()
    if current != branch:
        exists = subprocess.run(["git", "rev-parse", "--verify", "--quiet", branch],
                                cwd=root, capture_output=True).returncode == 0
        sw = subprocess.run(["git", "switch"] + ([branch] if exists else ["-c", branch]),
                            cwd=root, capture_output=True, text=True)
        if sw.returncode != 0:
            print(f"Could not switch to {branch}: {sw.stderr.strip()}", file=sys.stderr)
            return 2

    update_job(root, args.job, status="running", branch=branch)
    print(f"Running {args.job} on {branch} ...\n")

    ok, summary = invoke(root, cmd)
    print(summary)
    update_job(
        root, args.job,
        status="done" if ok else "failed",
        branch=branch,
        result=" ".join(summary.split())[:MAX_FIELD] if summary else "no output",
    )
    print(f"\n{args.job} -> {'done' if ok else 'failed'} (branch {branch}, nothing committed)")
    if ok:
        print("Review with: git status && git diff")
    return 0 if ok else 1


# ----------------------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=None, help="repository root")
    sub = ap.add_subparsers(dest="command", required=True)

    p = sub.add_parser("serve", help="serve the repo and accept jobs from the browser")
    p.add_argument("--port", type=int, default=DEFAULT_PORT)

    p = sub.add_parser("list", help="list jobs")
    p.add_argument("--all", action="store_true", help="include finished and dropped jobs")

    p = sub.add_parser("show", help="print a job record")
    p.add_argument("job")

    sub.add_parser("adopt", help="give hand-placed jobs a real id and matching filename")

    p = sub.add_parser("plan", help="ask the agent for a plan, changing nothing")
    p.add_argument("job")
    p.add_argument("--replan", action="store_true", help="discard an existing plan")
    p.add_argument("--model", default=None, help="model alias passed to the CLI")

    p = sub.add_parser("approve", help="accept the plan so the job may run")
    p.add_argument("job")

    p = sub.add_parser("run", help="run an approved job through the Claude Code CLI")
    p.add_argument("job")
    p.add_argument("--dry-run", action="store_true", help="print the command, run nothing")
    p.add_argument("--yes", action="store_true", help="skip the confirmation prompt")
    p.add_argument("--force", action="store_true", help="re-run a job that is done or running")
    p.add_argument("--model", default=None, help="model alias passed to the CLI")
    p.add_argument("--permission-mode", default=DEFAULT_PERMISSION_MODE)

    args = ap.parse_args()
    root = Path(args.root).resolve() if args.root else repo_root()

    return {
        "serve": cmd_serve, "list": cmd_list, "show": cmd_show,
        "adopt": cmd_adopt, "plan": cmd_plan, "approve": cmd_approve, "run": cmd_run,
    }[args.command](root, args)


if __name__ == "__main__":
    sys.exit(main())
