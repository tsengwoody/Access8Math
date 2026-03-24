## Context

The math core has already been extracted into a package-backed architecture with clear internal modules:

- `nodes.py`
- `tree.py`
- `semantics.py`
- `rules.py`
- `session.py`
- `metadata.py`

The remaining issue is naming rather than ownership. The package still uses the historical name `A8M_PM`, which is opaque and no longer matches the package's current role.

Current in-repo callers are limited and well-known:

- `addon/globalPlugins/Access8Math/__init__.py`
- `addon/globalPlugins/Access8Math/dialogs.py`
- `addon/globalPlugins/Access8Math/interaction.py`
- package regression tests

This makes a full rename feasible without introducing a compatibility alias.

## Goals

- Rename the package directory from `A8M_PM` to `reader`.
- Update all in-repo callers to import `reader`.
- Preserve current behavior for parsing, semantics, rules, and `MathContent`.
- Make `A8M_PM` unavailable after the rename so the repo has a single canonical import path.

## Non-Goals

- Preserve compatibility for external callers that still import `A8M_PM`.
- Redesign the package internals in the same change.
- Change `MathContent`, `initialize()`, registry ordering, or semantic behavior.
- Rename tests purely for aesthetics if their content already validates the new import path.

## Approach

1. Add rename-focused regression tests:
   - `import reader` succeeds
   - `A8M_PM` is no longer importable
   - package ownership expectations now point at `reader.*`
2. Rename the package directory from `A8M_PM` to `reader`.
3. Update all in-repo imports and package references to the new package name.
4. Re-run package compatibility, teaching-demo corpus, and synthetic coverage tests.
5. Run a repository caller audit to ensure no `A8M_PM` imports remain.

## Design Notes

### No compatibility alias

This change intentionally does not keep an alias package or shim module for `A8M_PM`.

The reasons are:

- the repo already has a comprehensive regression suite
- in-repo callers are few and easy to update
- leaving a compatibility alias would keep the rename only half-finished

The end state should have exactly one canonical package name: `reader`.

### Package path expectations

The current tests assert package ownership via module names such as:

- `A8M_PM.nodes`
- `A8M_PM.rules`
- `A8M_PM.semantics`

After this change, those expectations should become:

- `reader.nodes`
- `reader.rules`
- `reader.semantics`

That is a public-path rename, not a behavior change.

### Caller audit boundary

The in-repo caller boundary for this change is:

- addon runtime callers in `addon/globalPlugins/Access8Math/`
- regression tests under `tests/`

Archived OpenSpec documents may continue to contain historical `A8M_PM` references and are not part of the runtime caller surface.

## Risks

- A relative or absolute import may still reference `A8M_PM` after the directory rename.
- Test helpers may still clear or inspect `sys.modules` using the old package name.
- Deleting the old package path may expose hidden assumptions in import ordering.

## Mitigations

- Add failing rename regression tests before changing the package path.
- Run repository-wide `A8M_PM` caller audit before claiming completion.
- Keep verification scoped to the existing package, demo corpus, and synthetic coverage suites.
