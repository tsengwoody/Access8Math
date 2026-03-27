from pathlib import Path
import ast
import re
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PO_FILES = sorted((PROJECT_ROOT / "addon/locale").glob("*/LC_MESSAGES/nvda.po"))
BRACE_PATTERN = re.compile(r"\{[A-Za-z0-9_]+\}")


class PoPlaceholderTests(unittest.TestCase):
	def test_python_brace_format_entries_preserve_placeholder_sets(self):
		violations = []
		for path in PO_FILES:
			lines = path.read_text(encoding="utf-8").splitlines()
			index = 0
			while index < len(lines):
				line = lines[index]
				if not line.startswith("msgid "):
					index += 1
					continue

				flags = set()
				lookback = index - 1
				while lookback >= 0 and lines[lookback].startswith("#, "):
					flags.update(flag.strip() for flag in lines[lookback][3:].split(","))
					lookback -= 1

				msgid_literal = line[len("msgid "):]
				msgid = "" if msgid_literal == '""' else ast.literal_eval(msgid_literal)
				index += 1
				while index < len(lines) and lines[index].startswith('"'):
					msgid += ast.literal_eval(lines[index])
					index += 1

				if index >= len(lines) or not lines[index].startswith("msgstr "):
					continue

				msgstr_literal = lines[index][len("msgstr "):]
				msgstr = "" if msgstr_literal == '""' else ast.literal_eval(msgstr_literal)
				index += 1
				while index < len(lines) and lines[index].startswith('"'):
					msgstr += ast.literal_eval(lines[index])
					index += 1

				if "python-brace-format" not in flags:
					continue

				msgid_braces = sorted(set(BRACE_PATTERN.findall(msgid)))
				msgstr_braces = sorted(set(BRACE_PATTERN.findall(msgstr)))
				if msgid_braces != msgstr_braces:
					violations.append(
						f"{path}: {msgid!r} msgid={msgid_braces} msgstr={msgstr_braces}"
					)

		self.assertEqual(
			violations,
			[],
			"python-brace-format placeholders must match:\n" + "\n".join(violations),
		)


if __name__ == "__main__":
	unittest.main()
