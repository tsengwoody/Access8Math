## 1. Lock current writer behavior with tests

- [x] 1.1 Add regression tests for section and delimiter detection
- [x] 1.2 Add regression tests for core writer navigation behavior
- [x] 1.3 Add regression tests for review/display/interact writer actions

## 2. Extract internal writer session logic

- [x] 2.1 Move section and delimiter logic into a dedicated writer session module
- [x] 2.2 Preserve `SectionManager` behavior through the new internal boundary

## 3. Extract internal writer navigation logic

- [x] 3.1 Move pointer and line movement logic into a dedicated navigation module
- [x] 3.2 Preserve current caret and selection behavior

## 4. Extract internal writer action logic

- [x] 4.1 Move review/display/interact actions into a dedicated action module
- [x] 4.2 Keep `writer.py` as the NVDA-facing integration entrypoint

## 5. Verify no regression

- [x] 5.1 Run the new writer regression tests
- [x] 5.2 Run any existing related writer/package tests
- [x] 5.3 Run compile verification for touched modules and tests
