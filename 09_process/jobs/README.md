# Jobs — tasks written by the human for an agent

A **job** is something you noticed while reading a requirement, an analysis or a diagram,
written down against that element and handed to the subagent that owns it. Jobs are captured
from the requirements browser and run with `tools/jobs.py`.

## Jobs and open points are not the same list

They are written by different people and point in opposite directions:

| | Written by | Direction | Says |
|---|---|---|---|
| `OP-xx` open point | an agent, during its work | agent → human | "I found this, or left it undone" |
| `JOB-xxx` | **you**, while reading | human → agent | "do this" |

An open point is an agent reporting on its own work — that is what makes it worth trusting
as a record of where the project stands. A job is an instruction going the other way.

So a job never creates an open point, and an open point is never generated from a job: doing
either would put words in the agent's mouth. **The loop between them runs through you.** An
agent raises `OP-34`, you read it while browsing `SM-02`, decide it is worth acting on, and
write a job that says so. `relates_to: [OP-34]` records that decision, and nothing more.

Jobs are also not a replacement for a GitHub issue. If a finding needs tracking beyond the
work itself, raise a problem report or change request from `.github/ISSUE_TEMPLATE/`
(ASPICE SUP.9 and SUP.10) and point the job at it.

## Nothing changes before you have approved a plan

```
open  --plan-->  planned  --approve-->  approved  --run-->  done
```

```
python3 tools/jobs.py serve            # serve the browser and capture jobs from it
python3 tools/jobs.py list             # jobs and where they stand
python3 tools/jobs.py plan JOB-001     # the agent states its intent - read-only
#   read it, edit the ## Plan section in JOB-001.md
python3 tools/jobs.py approve JOB-001  # records that you accepted it
python3 tools/jobs.py run JOB-001      # only an approved job runs
```

`plan` uses the CLI's own plan mode, so the agent **cannot** write during it even if it
decides to. What comes back lands in the `## Plan` section of the record; reviewing it means
opening the file, and editing it needs no tool of ours. `approve` stamps `approved_at`, so
the record shows a plan existed and was accepted before any work started.

`run` refuses anything that is not approved, carries the approved plan into the prompt as the
authority, and instructs the agent to stop and report rather than improvise if the plan turns
out to be wrong. It never commits and never pushes: changes are left in the working tree on
branch `job/JOB-001` for review, and the outcome is written back into the record.

Why the extra step is worth it: the first job run without one produced good work that also
cited a requirement excluded from the base variant, and proposed three findings of which one
survived checking. A plan states the intent before the diff exists, which is the only point
where a wrong reading is cheap. The second job never needed to run at all - its plan showed
the work was already done.

Without the server the browser still captures: the panel offers **Copy job** and
**Download**. Put the file in this folder and run:

```
python3 tools/jobs.py adopt
```

A page that is offline cannot know which id is free, so it writes the placeholder `JOB-xxx`.
`adopt` assigns the next free number, renames the file to match and rewrites the record. Until
then the id and the filename disagree, which is worth not leaving lying around: the tools key
on the id.

## Record format

```yaml
---
id: JOB-001
created: 2026-08-02T09:14:00Z
status: open              # open | running | done | failed | dropped
target: SYS-REQ-025       # record id, document path, or diagram name
target_kind: record       # record | document | diagram | area | general
agent: systems-engineer   # a name from .claude/agents/, or empty for the default
relates_to: [OP-29]       # open points or issues this serves, filled by you
planned_at: ""            # written by `plan`
approved_at: ""           # written by `approve` - the audit trail
branch: ""                # written by the runner
result: ""                # written by the runner
---
```

The body carries `## Task`, an optional `## Context` captured by the browser, and `## Plan`
once planned:

```
```

Jobs are committed, so what was asked and what came back stay visible. They live outside the
directories `tools/trace_check.py` scans, so they never enter the trace graph — a job is not
a work product.

## One caution

A job file is data that becomes an instruction to an agent. `run` always shows the job and
the exact command and waits for confirmation, and the server listens on loopback only. Read
any job that arrived from someone else — through a pull request, say — before running it,
and do not run jobs in CI.
