from pathlib import Path
import re
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_FILE = PROJECT_ROOT / "addon/globalPlugins/Access8Math/__init__.py"
SOURCE_FILES = [
	BOOTSTRAP_FILE,
	PROJECT_ROOT / "addon/globalPlugins/Access8Math/regularExpression.py",
	PROJECT_ROOT / "addon/globalPlugins/Access8Math/editor.py",
	PROJECT_ROOT / "addon/globalPlugins/Access8Math/interaction.py",
	PROJECT_ROOT / "addon/globalPlugins/Access8Math/command/action.py",
	PROJECT_ROOT / "addon/globalPlugins/Access8Math/command/autocomplete.py",
	PROJECT_ROOT / "addon/globalPlugins/Access8Math/command/latex.py",
	PROJECT_ROOT / "addon/globalPlugins/Access8Math/command/translate.py",
	PROJECT_ROOT / "addon/globalPlugins/Access8Math/lib/mathProcess.py",
	PROJECT_ROOT / "addon/globalPlugins/Access8Math/lib/viewHTML.py",
	PROJECT_ROOT / "addon/globalPlugins/Access8Math/lib/latex/latexData.py",
	PROJECT_ROOT / "addon/globalPlugins/Access8Math/reader/rules.py",
	PROJECT_ROOT / "addon/globalPlugins/Access8Math/writer/__init__.py",
	PROJECT_ROOT / "addon/globalPlugins/Access8Math/writer/actions.py",
	PROJECT_ROOT / "addon/globalPlugins/Access8Math/writer/session.py",
]

TEST_FILES = [
	PROJECT_ROOT / "tests/test_writer_behavior.py",
	PROJECT_ROOT / "tests/test_viewhtml_rendering.py",
	PROJECT_ROOT / "tests/test_storage_explorer.py",
	PROJECT_ROOT / "tests/test_a8m_pm_package.py",
	PROJECT_ROOT / "tests/test_a8m_pm_demo_corpus.py",
	PROJECT_ROOT / "tests/test_a8m_pm_synthetic_coverage.py",
	PROJECT_ROOT / "tests/test_provider_runtime.py",
	PROJECT_ROOT / "tests/test_access8math_entrypoints.py",
]

BOOTSTRAP_TEST_FILES = [
	PROJECT_ROOT / "tests/test_provider_runtime.py",
	PROJECT_ROOT / "tests/test_access8math_entrypoints.py",
]

FORBIDDEN_SOURCE_PREFIXES = (
	"from delimiter import",
	"from command.",
	"from lib.",
	"from regularExpression import",
	"from python.",
)

SYS_PATH_INSERTION_PATTERNS = (
	re.compile(r"\bsys\.path\.insert\(\s*\d+\s*,\s*(?P<expr>.+?)\s*\)\s*$"),
	re.compile(r"\bsys\.path\.append\(\s*(?P<expr>.+?)\s*\)\s*$"),
	re.compile(r"\bsys\.path\.extend\(\s*(?P<expr>.+?)\s*\)\s*$"),
	re.compile(r"\bsys\.path\s*\[\s*:\s*0\s*\]\s*=\s*(?P<expr>.+?)\s*$"),
	re.compile(r"\bsys\.path\s*\+\=\s*(?P<expr>.+?)\s*$"),
	re.compile(r"\bsys\.path\s*=\s*(?P<expr>.+?)\s*$"),
)
ASSIGNMENT_PATTERN = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+?)\s*$")
ROOT_LIKE_NAME_PATTERN = re.compile(r"(?:^|_)(?:ROOT|PATH|DIR)(?:$|_)")


def _find_package_root_sys_path_mutations(text):
	tainted_names = {"PATH"}
	non_tainted_names = {"PYTHON_PATH", "PACKAGE_PATH"}
	violations = []
	for lineno, line in enumerate(text.splitlines(), start=1):
		assignment_match = ASSIGNMENT_PATTERN.match(line)
		if assignment_match:
			name, expr = assignment_match.groups()
			if name not in non_tainted_names:
				expr_uses_path = re.search(r"\bPATH\b", expr) is not None
				expr_tainted = any(re.search(rf"\b{re.escape(var)}\b", expr) for var in tainted_names if var != "PATH")
				if expr_uses_path:
					tainted_names.add(name)
				elif expr_tainted and ROOT_LIKE_NAME_PATTERN.search(name):
					tainted_names.add(name)
				elif "__file__" in expr and (name == "PATH" or ROOT_LIKE_NAME_PATTERN.search(name)):
					tainted_names.add(name)

		for pattern in SYS_PATH_INSERTION_PATTERNS:
			match = pattern.search(line)
			if not match:
				continue
			expr = match.group("expr")
			if any(token in expr for token in non_tainted_names):
				continue
			if "__file__" in expr:
				violations.append((lineno, line.strip()))
				break
			if any(re.search(rf"\b{re.escape(var)}\b", expr) for var in tainted_names):
				violations.append((lineno, line.strip()))
				break
	return violations

FORBIDDEN_TEST_PATTERNS = (
	re.compile(r"\bimport\s+reader\b"),
	re.compile(r"\bfrom\s+reader\s+import\b"),
	re.compile(r"\bimport\s+writer\b"),
	re.compile(r"\bfrom\s+writer\s+import\b"),
	re.compile(r"\bimport\s+lib\.explorer\b"),
	re.compile(r"\bfrom\s+lib\.viewHTML\s+import\b"),
	re.compile(r"\bimportlib\.import_module\s*\(\s*['\"]reader['\"]\s*\)"),
	re.compile(r"\bimportlib\.import_module\s*\(\s*['\"]writer['\"]\s*\)"),
	re.compile(r"\bimportlib\.import_module\s*\(\s*['\"]lib\."),
)


class ImportBoundaryTests(unittest.TestCase):
	def test_project_sources_do_not_use_top_level_self_imports(self):
		violations = []
		for path in SOURCE_FILES:
			for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
				stripped = line.lstrip()
				if stripped.startswith(FORBIDDEN_SOURCE_PREFIXES):
					violations.append(f"{path}:{lineno}: {stripped}")

		self.assertEqual(
			violations,
			[],
			"Found forbidden top-level self-imports:\n" + "\n".join(violations),
		)

	def test_bootstrap_does_not_insert_package_root_into_sys_path(self):
		text = BOOTSTRAP_FILE.read_text(encoding="utf-8")
		violations = [
			f"{BOOTSTRAP_FILE}:{lineno}: {line}"
			for lineno, line in _find_package_root_sys_path_mutations(text)
		]

		self.assertEqual(
			violations,
			[],
			"Found forbidden package-root sys.path injection in bootstrap:\n" + "\n".join(violations),
		)

	def test_bootstrap_registers_config_spec_before_importing_writer(self):
		text = BOOTSTRAP_FILE.read_text(encoding="utf-8")
		spec_index = text.find('config.conf.spec["Access8Math"] = {')
		writer_import_index = text.find("from .writer import TextMathEditField")

		self.assertNotEqual(spec_index, -1, "bootstrap must declare Access8Math config spec")
		self.assertNotEqual(writer_import_index, -1, "bootstrap must import TextMathEditField")
		self.assertLess(
			spec_index,
			writer_import_index,
			"bootstrap must register config defaults before importing writer",
		)

	def test_bootstrap_tests_do_not_insert_package_root_into_sys_path(self):
		violations = []
		for path in BOOTSTRAP_TEST_FILES:
			text = path.read_text(encoding="utf-8")
			for lineno, line in _find_package_root_sys_path_mutations(text):
				violations.append(f"{path}:{lineno}: {line}")

		self.assertEqual(
			violations,
			[],
			"Found forbidden package-root sys.path injection in bootstrap tests:\n" + "\n".join(violations),
		)

	def test_tests_do_not_use_legacy_top_level_project_imports(self):
		violations = []
		for path in TEST_FILES:
			for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
				stripped = line.lstrip()
				if any(pattern.search(stripped) for pattern in FORBIDDEN_TEST_PATTERNS):
					violations.append(f"{path}:{lineno}: {stripped}")

		self.assertEqual(
			violations,
			[],
			"Found forbidden top-level project imports in tests:\n" + "\n".join(violations),
		)


if __name__ == "__main__":
	unittest.main()
