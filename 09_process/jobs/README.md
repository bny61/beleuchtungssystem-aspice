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

## Using them

```
python3 tools/jobs.py serve          # serve the browser and capture jobs from it
python3 tools/jobs.py list           # open jobs
python3 tools/jobs.py show JOB-001
python3 tools/jobs.py run JOB-001    # shows the command, asks, runs on branch job/JOB-001
```

`run` never commits and never pushes. It leaves the changes in the working tree so you
review them like any other work, and writes the outcome back into the job record.

Without the server the browser still captures: the panel offers **Copy job** and
**Download**, and the file goes into this folder by hand.

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
branch: ""                # written by the runner
result: ""                # written by the runner
---
```

Jobs are committed, so what was asked and what came back stay visible. They live outside the
directories `tools/trace_check.py` scans, so they never enter the trace graph — a job is not
a work product.

## One caution

A job file is data that becomes an instruction to an agent. `run` always shows the job and
the exact command and waits for confirmation, and the server listens on loopback only. Read
any job that arrived from someone else — through a pull request, say — before running it,
and do not run jobs in CI.
