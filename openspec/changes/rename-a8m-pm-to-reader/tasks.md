## 1. Lock rename behavior with tests

- [x] 1.1 Add a failing package test that verifies `reader` imports successfully
- [x] 1.2 Add a failing package test that verifies `A8M_PM` is no longer importable
- [x] 1.3 Update demo and synthetic regression tests to target the future `reader` package name first

## 2. Rename the package

- [x] 2.1 Rename `addon/globalPlugins/Access8Math/A8M_PM/` to `addon/globalPlugins/Access8Math/reader/`
- [x] 2.2 Keep the package public API intact under `reader`
- [x] 2.3 Do not retain a compatibility shim or alias for `A8M_PM`

## 3. Update runtime callers

- [x] 3.1 Update `addon/globalPlugins/Access8Math/__init__.py` to import `reader`
- [x] 3.2 Update `addon/globalPlugins/Access8Math/dialogs.py` to import `reader`
- [x] 3.3 Update `addon/globalPlugins/Access8Math/interaction.py` to import `reader`

## 4. Update regression suites

- [x] 4.1 Update `tests/test_a8m_pm_package.py` ownership and import-path assertions to `reader`
- [x] 4.2 Update `tests/test_a8m_pm_demo_corpus.py` to import `reader`
- [x] 4.3 Update `tests/test_a8m_pm_synthetic_coverage.py` to import `reader`

## 5. Audit remaining references

- [x] 5.1 Run a repository caller audit for `A8M_PM` references
- [x] 5.2 Remove or update remaining in-repo `A8M_PM` import references

## 6. Verify no regression

- [x] 6.1 Run package compatibility tests
- [x] 6.2 Run the teaching-demo corpus tests
- [x] 6.3 Run the synthetic node/nodetype coverage tests
- [x] 6.4 Run compile verification for touched modules and tests
