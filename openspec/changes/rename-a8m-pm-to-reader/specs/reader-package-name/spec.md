# reader-package-name Specification

## Purpose
Define the canonical package name for the Access8Math reading package.

## Requirements
### Requirement: The canonical package name is `reader`

The Access8Math reading package SHALL be importable through the package name `reader`.

#### Scenario: Package import resolves through the new name

- **WHEN** an in-repo caller imports `reader`
- **THEN** the package SHALL resolve successfully
- **AND** callers SHALL be able to access the existing public API such as `MathContent`, `initialize()`, rule loading, and tree helpers

### Requirement: The legacy package name is removed

The Access8Math repository SHALL not retain `A8M_PM` as a compatibility package name after the rename is complete.

#### Scenario: Legacy import availability is inspected

- **WHEN** a maintainer attempts to import `A8M_PM`
- **THEN** the import SHALL not resolve
- **AND** the repository SHALL expose `reader` as the single canonical package name

### Requirement: In-repo callers use `reader`

All in-repo runtime callers and regression tests SHALL import the package through `reader`.

#### Scenario: Caller imports are audited

- **WHEN** a maintainer audits addon runtime callers and regression tests
- **THEN** those callers SHALL import `reader`
- **AND** they SHALL not depend on `A8M_PM` imports or module paths

### Requirement: Rename preserves current behavior

Renaming the package to `reader` SHALL not change current parsing, semantic, rule-loading, or navigation behavior.

#### Scenario: Existing regression suites are re-run after the rename

- **WHEN** the package compatibility tests, teaching-demo corpus tests, and synthetic coverage tests are executed after the package rename
- **THEN** the expected public package behavior, node snapshots, nodetype assignments, and predicate outcomes SHALL remain stable
