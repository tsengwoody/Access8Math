import json
import os
import sys
import tempfile
import types
import unittest
from unittest import mock


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLUGIN_ROOT = os.path.join(PROJECT_ROOT, "addon", "globalPlugins", "Access8Math")
PACKAGE_ROOT = os.path.join(PLUGIN_ROOT, "package")


class TestViewHTMLRendering(unittest.TestCase):
	def setUp(self):
		if PLUGIN_ROOT not in sys.path:
			sys.path.insert(0, PLUGIN_ROOT)
		if PACKAGE_ROOT not in sys.path:
			sys.path.insert(0, PACKAGE_ROOT)

		addon_stub = types.ModuleType("addonHandler")
		addon_stub.initTranslation = lambda: None
		config_stub = types.ModuleType("config")
		config_stub.conf = {
			"Access8Math": {
				"settings": {
					"LaTeX_delimiter": "bracket",
				},
			},
		}
		command_action_stub = types.ModuleType("command.action")
		command_action_stub.batch = lambda _name: (lambda value: value)

		self.module_patches = [
			mock.patch.dict(sys.modules, {
				"addonHandler": addon_stub,
				"config": config_stub,
				"command.action": command_action_stub,
			}),
		]
		for patch in self.module_patches:
			patch.start()

		for name in list(sys.modules):
			if name == "lib.viewHTML" or name.startswith("lib.viewHTML."):
				sys.modules.pop(name, None)

	def tearDown(self):
		for patch in reversed(self.module_patches):
			patch.stop()

	def _render(self, source_text, title="Spec Title"):
		from lib.viewHTML import text2template

		with tempfile.TemporaryDirectory() as temp_dir:
			src = os.path.join(temp_dir, "input.txt")
			dst = os.path.join(temp_dir, "content-config.js")
			with open(src, "w", encoding="utf8") as file:
				file.write(source_text)
			text2template(src=src, dst=dst, title=title)
			with open(dst, "r", encoding="utf8") as file:
				return file.read()

	def _extract_config(self, rendered):
		prefix = "window.contentConfig = "
		self.assertTrue(rendered.startswith(prefix))
		payload = rendered[len(prefix):].strip()
		return json.loads(payload)

	def test_text2template_preserves_multiline_source_text(self):
		rendered = self._render("line1\nline2\nline3")
		config = self._extract_config(rendered)
		self.assertEqual(config["sourceText"], "line1\nline2\nline3")

	def test_text2template_safely_embeds_backticks_and_template_sequences(self):
		source = "before `${danger}` and `code` after"
		rendered = self._render(source)
		config = self._extract_config(rendered)
		self.assertEqual(config["sourceText"], source)
		self.assertNotIn("sourceText\":`", rendered)

	def test_text2template_preserves_numeric_html_entity_decoding(self):
		rendered = self._render("alpha: &#65; and hex: &#x42;")
		config = self._extract_config(rendered)
		self.assertEqual(config["sourceText"], "alpha: A and hex: B")

	def test_text2template_preserves_legacy_latex_delimiter_key(self):
		rendered = self._render("plain text")
		config = self._extract_config(rendered)
		self.assertIn("latexDelimiter", config)
		self.assertEqual(config["latexDelimiter"], "bracket")
		self.assertNotIn("LaTeX_delimiter", config)


if __name__ == "__main__":
	unittest.main()
