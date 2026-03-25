## Context

`writer.py` is currently one of the largest remaining behavior-layer modules in Access8Math. It includes:

- `SectionManager` state and delimiter logic
- pointer and line navigation behavior
- gesture map toggles and mode switching
- NVDA `script_*` handlers
- review/export and interaction entrypoints

The module does useful work, but the current structure obscures which parts are pure behavior and which parts are NVDA integration.

## Goals

- Preserve current writer behavior and external script surface.
- Make the writer behavior layer easier to understand and test.
- Separate section/session logic from navigation logic.
- Separate NVDA script routing from reusable behavior operations.

## Non-Goals

- Redesign writer behavior or gesture semantics in this change.
- Change reader core behavior in this change.
- Rewrite editor or command subsystems in this change.
- Introduce new user-visible writer features in this change.

## Approach

1. Add focused regression tests for current writer behavior.
2. Extract section and delimiter logic into a session-oriented module.
3. Extract pointer and line movement into a navigation-oriented module.
4. Extract display/review/interact actions into a dedicated action module.
5. Keep `writer.py` as the public integration entrypoint for NVDA-facing script handlers.

## Proposed Internal Boundaries

### `writer_session.py`

- section discovery
- pointer lookup
- delimiter lookup
- in-section / in-math / in-text predicates
- command token selection helpers

### `writer_navigation.py`

- block movement
- line movement
- home/end style navigation
- caret range updates driven by session state

### `writer_actions.py`

- review/export entrypoints
- display block formatting
- interact action conversion

### `writer.py`

- NVDA-facing `TextMathEditField`
- gesture map toggles and mode coordination
- script handlers delegating into extracted helpers

## Risks

- `writer.py` likely has implicit shared state assumptions between navigation and script code.
- Refactoring may accidentally move code without actually reducing coupling.
- Writer behavior currently has much less direct regression coverage than reader core.

## Mitigations

- Write tests first for the behavior we rely on most.
- Keep the public `writer` entrypoint stable.
- Extract in small layers instead of performing a full rewrite.
- Verify behavior through focused tests before and after each extraction step.
