---
name: vibe2spec-flow
description: Run a lightweight Spec-first Vibe2Spec workflow inside Codex without launching codex-agent-harness. Use when the user says Vibe2Spec, Spec 工作流, lightweight harness, 不跑 harness, harness 太慢, 内化为 skill, or wants Codex to create/update doc/proposal.md, doc/detailed-design.md, doc/tasks, doc/prompt.md, or implement from those artifacts directly.
---

# Vibe2Spec Flow

Use this skill as the lightweight default path. Do not run `codex-harness`, `./harness`, or `harness` unless the user explicitly asks for the CLI audit workflow.

## Modes

Pick the smallest mode that satisfies the user:

- **Spec only**: create/update `doc/proposal.md`, and optionally `doc/specs/index.md` plus `doc/specs/YYYY-MM-DD-topic.md`.
- **Design**: create/update `doc/detailed-design.md` from `doc/proposal.md` and existing code.
- **Tasks**: create/update `doc/tasks/progress.md` and `doc/tasks/<module-name>.md`.
- **Implement**: read existing docs/tasks, code sequentially by default, test, update checklists, and report verification.
- **Prompt only**: generate `doc/prompt.md` when the user wants a reusable implementation prompt instead of immediate coding.

## Core Rules

1. Prefer direct Codex edits over running the harness CLI.
2. Keep artifacts as the source of truth; do not rely on chat memory for durable decisions.
3. Write Spec-first docs:
   - EARS requirements: `WHEN <trigger> THE SYSTEM SHALL <action>`.
   - ADR decisions: `Decision`, `Why`, `Alternatives / Tradeoffs`.
   - Acceptance criteria: `GIVEN / WHEN / THEN`.
   - Always include Non-Goals / Out of Scope.
4. Mark uncertain items as `Open Questions` or `建议假设`; do not present guesses as confirmed decisions.
5. Default implementation is a single agent working through `doc/tasks/progress.md`. Use subagents only when tasks are independent, file ownership is clear, and context size justifies it.
6. If implementation changes behavior, schema, API contracts, or key decisions, backfill the relevant spec/design/task docs.
7. Run the repo's existing verification commands. If a command is unavailable, record the reason and use the best focused alternative.

## Artifact Shapes

`doc/proposal.md` should include:

- Context
- Goals & Non-Goals
- User Stories
- Functional Requirements (EARS)
- Key Decisions / ADR Candidates
- Acceptance Criteria (GIVEN-WHEN-THEN)
- Out of Scope
- Constraints
- Risks
- Open Questions

`doc/detailed-design.md` should include:

- Context and design scope
- Module responsibilities
- Data model, state machine, or key workflows when relevant
- API / local contracts
- ADRs
- Acceptance-criteria mapping
- Test strategy
- Spec backfill notes

Each `doc/tasks/<module-name>.md` should include:

- Module goal
- Dependencies
- Out of Scope
- Checklist
- Traceability to EARS / ADR / Acceptance Criteria
- Test requirements
- `AFK` or `HITL`
- `Blocked by`
- Likely file scope

## When To Ask

Ask before proceeding only when the missing answer affects product commitments, data/security/privacy, paid services, external credentials, destructive operations, or public behavior that cannot be inferred from existing artifacts. Otherwise make a conservative MVP assumption and record it.
