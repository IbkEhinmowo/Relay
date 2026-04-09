<!-- @format -->

# Relay Observability + Runtime Control Roadmap

## Why this matters (resume ROI)

Build this as an "LLM Runtime Observability + Control Plane" project, not just a dashboard.

What this demonstrates:

- You can operate and debug async AI systems in real time.
- You can design structured telemetry across LLM, tools, scheduler, and infrastructure.
- You can build a production-style feedback loop (observe -> detect -> act).

---

## Product definition (what to build)

A daemon-driven observability layer that captures and streams:

- LLM lifecycle events (request started/completed/failed, latency, tokens if available)
- Tool call events (start/end/error, args summary, duration)
- Scheduler events (cron/timer job added/fired/succeeded/failed/missed)
- System/runtime signals (CPU, memory, disk, queue depth)
- Infra logs (Docker container logs, Redis health/signals)

Operator surface:

- Live event stream (terminal UI first, web UI optional later)
- Text command box for control operations (filter, replay, retry, pause, cancel)
- Alert feed for actionable failures and slowdowns

---

## Scope split (recommended)

Keep this as a separate scope from Relay feature development.

Track A: Relay core (stability only)

- Only add minimal instrumentation hooks.
- Avoid major refactors while building observability.
- Keep current app behavior unchanged.

Track B: AgentOps sidecar (new deliverable)

- Build observability daemon, CLI, and rules engine as a separate package/process.
- Treat Relay as an event producer, not the place where all logic lives.
- Ship this as a standalone demo artifact that can later integrate with any agent app.

Why this split helps:

- Reduces risk from existing code quality concerns.
- Lets you show architecture and reliability skills without rewriting Relay first.
- Produces a resume-ready project even if Relay internals evolve later.

---

## Minimal coupling contract (so it does not get messy)

Use a tiny adapter boundary between Relay and observability.

Required Relay changes only:

- Emit structured events via one helper function.
- Propagate run_id through LLM and tool execution flow.
- Emit scheduler lifecycle events.
- Emit cron metadata for scheduled tasks (task name, cron expression, next run, one_off flag).

Everything else lives in sidecar:

- Event ingestion, correlation, alerts, retries, and recovery policies.
- CLI operator console and replay/filter logic.
- Docker/Redis collectors and health polling.

Rule of thumb:

- If functionality can run from the event stream, keep it out of Relay.
- If functionality requires domain context already inside Relay, add only a thin producer hook.

---

## Target architecture

1. Event producers (inside existing services)

- Emit structured JSON events from:
  - Core/Processor/LLMAGENT.py
  - Core/Integrations/Schedular.py
  - Any tool wrappers in Core/Processor/ToolSet.py (or per tool implementation)

2. Event transport

- Redis Streams as the canonical event bus.
- Suggested stream key: relay:events

3. Observability daemon (new process)

- Reads from relay:events continuously.
- Normalizes, enriches, computes rolling metrics, and stores short-term aggregates.
- Emits alerts to relay:alerts stream and optionally Discord.

4. Consumer surfaces

- CLI/TUI (phase 1): tail stream + command box.
- WebSocket API (phase 2): serve realtime events to frontend.
- Dashboard (phase 3): timeline, traces, health cards.

---

## Event schema (first version)

Use one schema everywhere:

```json
{
  "event_id": "uuid",
  "ts": "2026-04-08T18:22:11.120Z",
  "run_id": "uuid",
  "source": "llm|tool|scheduler|system|infra",
  "event_type": "started|completed|failed|queued|fired|timeout|alert",
  "name": "openrouter_chat|websearch|redbeat_job|docker_log",
  "status": "ok|error|warn",
  "latency_ms": 1234,
  "severity": "info|warning|critical",
  "meta": {
    "tool_name": "websearch",
    "task_name": "Core.Processor.LLMAGENT.llmagent_process",
    "container": "app",
    "redis_db": 5,
    "error": "timeout",
    "summary": "short human-readable message"
  }
}
```

Rules:

- Keep payload small and structured.
- Redact secrets/tokens by default.
- Use run_id to correlate one user request across all events.

---

## How to capture Docker + Redis logs (practical)

### Option A (recommended now): Log collector daemon using Docker SDK + Redis client

Build a Python daemon that:

- Connects to Docker daemon and tails selected container logs (app, redis, workers).
- Emits each parsed line as source=infra events.
- Periodically polls Redis INFO and LLEN/XLEN stats for health metrics.

Implementation notes:

- Install docker Python package and use docker.from_env().
- For each container, use container.logs(stream=True, follow=True, tail=100).
- Parse severity from line patterns (ERROR, WARN, traceback).
- Poll Redis every 2-5 seconds for:
  - INFO memory
  - INFO stats
  - keyspace hits/misses
  - stream length (relay:events)
  - queue depth keys (if used)

Pros:

- Fastest to implement.
- No extra infra required.
- Good enough for demo + interviews.

### Option B (later): OTEL/Fluent Bit pipeline

Use OpenTelemetry Collector or Fluent Bit for log/metric shipping, then forward into your stream/dashboard.

Pros:

- More production-like.
- Better for multi-host environments.

Cons:

- Higher setup complexity.

---

## Daemon responsibilities (single binary/process)

Create one daemon process (suggested file: Core/Integrations/observability_daemon.py) with modules:

1. ingest

- Reads app-level events from relay:events.
- Reads Docker logs.
- Polls Redis health.

2. correlate

- Maintains in-memory map by run_id.
- Computes stage durations and end-to-end latency.

3. detect

- Rules engine:
  - LLM latency > threshold
  - tool failure rate over rolling window
  - scheduler misses or long queue delay
  - cron drift (actual fire time minus expected fire time)
  - repeated cron job failures within rolling window
  - Redis memory pressure

4. output

- Writes alerts to relay:alerts.
- Sends optional Discord alert via existing integration.
- Provides status endpoint or local socket for CLI.

5. retention

- Keep raw events in Redis stream with maxlen cap.
- Keep minute-level aggregates for charts.

6. remediate (optional self-healing scope)

- Execute safe automated actions (retry, requeue, pause noisy job, controlled restart).
- Verify recovery and emit recovered/failed-recovery events.
- Escalate to operator when remediation policy budget is exhausted.

---

## Build phases (execution order)

## Phase 0 - Foundation (1-2 days)

- Add shared event emitter utility (JSON + Redis Streams).
- Add run_id propagation from message entry point.
- Instrument LLM start/end/fail in Core/Processor/LLMAGENT.py.
- Instrument tool call start/end/fail around each tool invocation.

Done when:

- You can tail relay:events and see a full request trace.

## Phase 1 - Scheduler + Infra visibility (1-2 days)

- Instrument Core/Integrations/Schedular.py task lifecycle events.
- Track cron-specific events: scheduled, due, fired, completed, failed, removed.
- Capture cron metadata: expression fields, next_run_at, run_lag_ms, one_off.
- Build first daemon loop that tails Docker logs + Redis health stats.
- Emit normalized infra/system events to relay:events.

Done when:

- You can see app + redis + scheduler activity in one stream.

## Phase 2 - CLI operator console (2-3 days)

- Build TUI using Textual (or prompt_toolkit) with:
  - live event table
  - filters (run_id/source/status)
  - alert panel
  - command input box
- Commands: help, filter, trace <run_id>, replay <minutes>, retry <task>, pause_scheduler, resume_scheduler.

Done when:

- You can triage a failed run without reading raw container logs.

## Phase 3 - Alerts and reliability (1-2 days)

- Add rule engine and threshold configs.
- Add alert suppression (cooldown/dedup).
- Add reconnect and backoff for Docker/Redis disconnects.

Done when:

- Failures generate actionable alerts with low noise.

## Phase 3.5 - Self-healing (separate scope, optional) (1-2 days)

- Add policy-based remediation engine in daemon only.
- Add bounded retries with exponential backoff and jitter.
- Add circuit breaker per tool/provider.
- Add recovery verification checks and escalation path.

Done when:

- System can auto-recover from common transient failures and records audit events for every action.

## Phase 4 - Optional dashboard/websocket (later)

- Add small FastAPI WebSocket gateway to stream events.
- Replace frontend placeholder page with timeline and trace views.

Done when:

- Browser dashboard mirrors CLI stream.

---

## Minimum viable interview demo

Scenario:

1. Start stack and daemon.
2. Submit user request that triggers tools.
3. Show live run trace in CLI.
4. Force a tool error/timeout.
5. Show alert + retry command from command box.
6. Show recovered run and final success.

Talking points:

- Correlated tracing with run_id.
- Structured event model across heterogeneous components.
- Reliability features (retry, backoff, dedup alerts).

---

## Suggested file additions

- Core/Observability/event_schema.py
- Core/Observability/emitter.py
- Core/Observability/context.py
- Core/Integrations/observability_daemon.py
- Core/Observability/rules.py
- Core/Observability/cli_console.py
- Core/Observability/remediation.py
- docs/observability.md

Suggested edits:

- Core/Processor/LLMAGENT.py
- Core/Integrations/Schedular.py
- docker-compose.yml
- requirements.txt

---

## Dependencies to add

Python packages:

- psutil
- docker
- textual (or prompt_toolkit)
- tenacity

Optional later:

- fastapi
- uvicorn
- websockets

---

## Docker and process layout

Add services (later):

- observability-daemon (new)
- worker (if split from app)
- beat (if split from app)

Example role split:

- app: core runtime
- worker: celery worker
- beat: redbeat scheduler
- observability-daemon: event ingestion/correlation/alerts

---

## Success metrics for this project

Track these metrics and include them in your README:

- p50/p95 LLM latency
- tool error rate by tool
- scheduler execution delay
- mean time to detect (MTTD) for injected failures
- mean time to resolve (MTTR) using CLI commands

If you can show before/after numbers, your resume impact increases significantly.

---

## Risks and mitigations

Risk: Too much scope in UI

- Mitigation: CLI first, dashboard later.

Risk: Noisy logs and alert fatigue

- Mitigation: structured schema + dedup + severity tiers.

Risk: Event volume growth

- Mitigation: capped stream length + sampled debug events.

Risk: Missing correlation context

- Mitigation: enforce run_id propagation in every producer.

Risk: Relay codebase complexity slows progress

- Mitigation: keep observability as sidecar scope with minimal producer hooks.

---

## 7-day implementation plan

Day 1:

- Add emitter utility + schema + run_id propagation.

Day 2:

- Instrument LLM + tool calls.

Day 3:

- Instrument scheduler events.

Day 4:

- Build daemon for Docker logs + Redis health polling.

Day 5:

- Build CLI stream viewer + filtering.

Day 6:

- Add command box actions + retry/pause/resume operations.

Day 7:

- Add alerts, failure injection script, and record demo.

---

## Resume-ready project title ideas

- Relay Ops: Real-Time Observability and Control Plane for Autonomous LLM Workflows
- Relay Runtime: Event-Driven Tracing and Incident Response for AI Agents
- AgentOps for Relay: Live Telemetry, Alerting, and Operator Controls
