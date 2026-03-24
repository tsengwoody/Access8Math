## Why

The Access8Math core package has already been refactored into a clean package structure, but it still uses the historical name `A8M_PM`.

That name is no longer a good fit:

- it does not communicate the package's role to maintainers
- it leaks historical implementation detail rather than current architecture
- it makes code search and onboarding harder than necessary

The package now owns MathML parsing, tree construction, semantics, rules, and session orchestration. A clearer package name should reflect the addon's reading-oriented use directly.

This change renames the package from `A8M_PM` to `reader` and updates all in-repo callers to use the new import path without preserving a compatibility alias.

## What Changes

- Rename `addon/globalPlugins/Access8Math/A8M_PM/` to `addon/globalPlugins/Access8Math/reader/`.
- Update all in-repo imports and package references from `A8M_PM` to `reader`.
- Update tests so the package is imported through `reader` and `A8M_PM` is no longer expected to resolve.
- Preserve current parsing, semantic, rule-loading, and navigation behavior after the rename.
- Do not add a compatibility shim or alias package for `A8M_PM`.

## Capabilities

### Modified Capabilities

- `reader-package-name`: The Access8Math math package is exposed under the canonical package name `reader` instead of the legacy name `A8M_PM`.

## Impact

- Affected code:
  - `addon/globalPlugins/Access8Math/A8M_PM/` -> `addon/globalPlugins/Access8Math/reader/`
  - `addon/globalPlugins/Access8Math/__init__.py`
  - `addon/globalPlugins/Access8Math/dialogs.py`
  - `addon/globalPlugins/Access8Math/interaction.py`
  - `tests/test_a8m_pm_package.py`
  - `tests/test_a8m_pm_demo_corpus.py`
  - `tests/test_a8m_pm_synthetic_coverage.py`
- Affected systems:
  - Addon package import graph
  - Caller import paths
  - Package-name regression expectations
