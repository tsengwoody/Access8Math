## Why

`addon/globalPlugins/Access8Math/writer.py` has grown into a large mixed-responsibility module that currently combines:

- delimiter and section detection
- caret and pointer navigation
- gesture and script handlers
- review/display/interact actions

This makes the behavior layer harder to understand, test, and extend. Small changes to navigation or script routing can easily affect unrelated parts of the writer flow because state and logic are not cleanly separated.

The reader core has already been extracted and stabilized. The next maintainability gain is to give the writer behavior layer clearer boundaries without changing the public gesture surface or current writer behavior.

## What Changes

- Add regression tests that lock the current `writer` behavior for section detection, navigation, and review/display entrypoints.
- Refactor `writer.py` so the current mixed logic is split into focused internal modules for:
  - writer session state
  - navigation behavior
  - script/gesture routing
  - review/display actions
- Preserve the existing `writer` import surface and external NVDA script behavior.

## Capabilities

### Modified Capabilities

- `writer-behavior-layer`: Access8Math writer behavior becomes maintainable through clearer internal module boundaries while preserving current behavior.

## Impact

- Affected code:
  - `addon/globalPlugins/Access8Math/writer.py`
  - new internal writer behavior modules under `addon/globalPlugins/Access8Math/`
  - tests covering writer behavior
- Affected systems:
  - section detection and delimiter handling
  - writer navigation behavior
  - gesture/script routing
  - review/display/interact entrypoints
