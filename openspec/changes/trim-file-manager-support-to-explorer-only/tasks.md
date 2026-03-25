## 1. Lock current Explorer selection behavior with tests

- [x] 1.1 Add or update regression tests for Windows Explorer selected-item lookup
- [x] 1.2 Add or update regression coverage for Access8Math entrypoints that consume `explorer.get_selected_file()`

## 2. Trim file manager support to Explorer only

- [x] 2.1 Remove Total Commander support from the storage layer
- [x] 2.2 Remove xplorer2 support from the storage layer
- [x] 2.3 Keep `lib/explorer.py` as the Explorer-only lookup module

## 3. Remove copied generic helper leftovers

- [x] 3.1 Remove `lib/generic` modules that are no longer used after Explorer-only cleanup
- [x] 3.2 Verify no remaining runtime imports depend on deleted helper modules

## 4. Verify no regression

- [x] 4.1 Run focused Explorer/storage regression tests
- [x] 4.2 Run the relevant Access8Math test suite
- [x] 4.3 Run compile verification for touched modules and tests
