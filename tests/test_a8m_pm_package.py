import importlib
import importlib.util
import os
import sys
import types
import unittest
from xml.etree import ElementTree as ET


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLUGIN_ROOT = os.path.join(PROJECT_ROOT, "addon", "globalPlugins", "Access8Math")
READER_PACKAGE_PATH = os.path.join(PLUGIN_ROOT, "reader")


class TestA8MPMPackageCompatibility(unittest.TestCase):
	def setUp(self):
		self._old_access8math = sys.modules.get("Access8Math")
		self._path_added = PLUGIN_ROOT not in sys.path
		access8math_pkg = types.ModuleType("Access8Math")
		access8math_pkg.__path__ = [PLUGIN_ROOT]

		if self._path_added:
			sys.path.insert(0, PLUGIN_ROOT)
		sys.modules["Access8Math"] = access8math_pkg
		for name in list(sys.modules):
			if name in {"A8M_PM", "Access8Math.reader"} or name.startswith("A8M_PM.") or name.startswith("Access8Math.reader."):
				sys.modules.pop(name, None)

	def tearDown(self):
		for name in list(sys.modules):
			if name in {"A8M_PM", "Access8Math.reader"} or name.startswith("A8M_PM.") or name.startswith("Access8Math.reader."):
				sys.modules.pop(name, None)
		if self._old_access8math is None:
			sys.modules.pop("Access8Math", None)
		else:
			sys.modules["Access8Math"] = self._old_access8math
		if self._path_added and PLUGIN_ROOT in sys.path:
			sys.path.remove(PLUGIN_ROOT)

	def test_reader_is_package_backed_facade(self):
		module = importlib.import_module("Access8Math.reader")
		self.assertTrue(module.__file__.endswith(os.path.join("reader", "__init__.py")))
		self.assertTrue(hasattr(module, "MathContent"))

	def test_reader_package_path_exists(self):
		self.assertTrue(os.path.isdir(READER_PACKAGE_PATH))
		module = importlib.import_module("Access8Math.reader")
		self.assertTrue(module.__file__.endswith(os.path.join("reader", "__init__.py")))

	def test_legacy_a8m_pm_package_is_not_importable(self):
		self.assertIsNone(importlib.util.find_spec("A8M_PM"))
		with self.assertRaises(ModuleNotFoundError):
			importlib.import_module("A8M_PM")

	def test_package_import_does_not_load_legacy_runtime_module(self):
		importlib.import_module("Access8Math.reader")
		self.assertNotIn("Access8Math.reader._legacy_impl", sys.modules)

	def test_core_impl_module_is_not_importable(self):
		importlib.import_module("Access8Math.reader")
		self.assertNotIn("Access8Math.reader._core_impl", sys.modules)
		self.assertIsNone(importlib.util.find_spec("Access8Math.reader._core_impl"))

	def test_facade_exports_boundary_owned_symbols(self):
		module = importlib.import_module("Access8Math.reader")
		expected_modules = {
			"MathContent": "Access8Math.reader.session",
			"initialize": "Access8Math.reader.semantics",
			"MathRule": "Access8Math.reader.rules",
			"includes_unicode_range": "Access8Math.reader.tree",
			"Node": "Access8Math.reader.nodes",
		}
		for name, expected_module in expected_modules.items():
			with self.subTest(name=name):
				self.assertEqual(getattr(module, name).__module__, expected_module)
		self.assertEqual(module.LOCALE_DIR, importlib.import_module("Access8Math.reader.rules").LOCALE_DIR)

	def test_internal_boundaries_are_importable(self):
		for name in ["tree", "nodes", "semantics", "rules", "session"]:
			with self.subTest(name=name):
				submodule = importlib.import_module(f"Access8Math.reader.{name}")
				self.assertIsNotNone(submodule)

	def test_rule_and_language_api_is_provided_by_rules_boundary(self):
		module = importlib.import_module("Access8Math.reader")
		for name in [
			"exist_language",
			"add_language",
			"remove_language",
			"export_language",
			"available_languages",
			"clean_user_data",
			"load_unicode_dic",
			"load_math_rule",
			"save_unicode_dic",
			"save_math_rule",
		]:
			with self.subTest(name=name):
				self.assertEqual(getattr(module, name).__module__, "Access8Math.reader.rules")

	def test_tree_and_node_api_is_provided_by_extracted_boundaries(self):
		module = importlib.import_module("Access8Math.reader")
		for name in [
			"mathml2etree",
			"create_node",
			"clean_allnode",
			"set_mathcontent_allnode",
			"set_mathrule_allnode",
			"set_braillemathrule_allnode",
			"clear_type_allnode",
			"check_type_allnode",
			"check_in_allnode",
		]:
			with self.subTest(name=name):
				self.assertEqual(getattr(module, name).__module__, "Access8Math.reader.tree")

		for name in ["Node", "NonTerminalNode", "TerminalNode", "Math", "Mrow", "Mi", "Mo", "Mn"]:
			with self.subTest(name=name):
				self.assertEqual(getattr(module, name).__module__, "Access8Math.reader.nodes")

	def test_tree_and_node_behavior_remains_usable(self):
		module = importlib.import_module("Access8Math.reader")
		root = module.create_node(
			module.mathml2etree("<math><mrow><mi>x</mi><mo>+</mo><mi>y</mi></mrow></math>")
		)
		module.clean_allnode(root)
		self.assertEqual(root.__class__.__module__, "Access8Math.reader.nodes")
		self.assertEqual(root.tag, "math")
		self.assertEqual(root.down.tag, "mi")
		self.assertEqual(root.down.next_sibling.tag, "mo")
		self.assertEqual(root.down.next_sibling.next_sibling.tag, "mi")
		self.assertIn("<mi>x</mi>", root.get_mathml())

	def test_invalid_mathml_preserves_parseerror(self):
		module = importlib.import_module("Access8Math.reader")
		with self.assertRaises(ET.ParseError):
			module.mathml2etree("<math><mrow><mi>x</mi>")

	def test_semantics_api_and_registry_are_provided_by_semantics_boundary(self):
		module = importlib.import_module("Access8Math.reader")
		self.assertEqual(module.NodeType.__module__, "Access8Math.reader.semantics")
		self.assertEqual(module.TerminalNodeType.__module__, "Access8Math.reader.semantics")
		self.assertEqual(module.NonTerminalNodeType.__module__, "Access8Math.reader.semantics")
		self.assertEqual(module.SiblingNodeType.__module__, "Access8Math.reader.semantics")
		self.assertEqual(module.CompoundNodeType.__module__, "Access8Math.reader.semantics")
		self.assertEqual(module.initialize.__module__, "Access8Math.reader.semantics")
		self.assertGreater(len(module.nodetypes), 0)
		self.assertEqual(module.nodetypes[0].__module__, "Access8Math.reader.semantics")
		self.assertEqual(module.all_nodetypes_dict["object"], object)

	def test_initialize_uses_explicit_semantics_registry(self):
		module = importlib.import_module("Access8Math.reader")
		config = {
			"settings": {"analyze_math_meaning": True},
			"rules": {nodetype.__name__: True for nodetype in module.nodetypes},
		}
		module.initialize(config)
		self.assertGreater(len(module.nodetypes_check), 0)
		self.assertTrue(all(nodetype.__module__ == "Access8Math.reader.semantics" for nodetype in module.nodetypes_check))

	def test_mathcontent_is_provided_by_session_boundary(self):
		module = importlib.import_module("Access8Math.reader")
		self.assertEqual(module.MathContent.__module__, "Access8Math.reader.session")

	def test_mathcontent_orchestrates_extracted_boundaries(self):
		module = importlib.import_module("Access8Math.reader")
		config = {
			"settings": {"analyze_math_meaning": True},
			"rules": {nodetype.__name__: True for nodetype in module.nodetypes},
		}
		module.initialize(config)
		content = module.MathContent("en", "<math><mrow><mi>x</mi><mo>+</mo><mi>y</mi></mrow></math>")
		self.assertEqual(content.root.__class__.__module__, "Access8Math.reader.nodes")
		self.assertEqual(content.pointer.__class__.__module__, "Access8Math.reader.nodes")
		self.assertEqual(module.load_math_rule.__module__, "Access8Math.reader.rules")
		self.assertEqual(module.mathml2etree.__module__, "Access8Math.reader.tree")
		self.assertTrue(content.navigate("downArrow"))
		self.assertEqual(content.pointer.tag, "mi")

	def test_quadratic_formula_is_not_misclassified_as_matrix(self):
		module = importlib.import_module("Access8Math.reader")
		config = {
			"settings": {"analyze_math_meaning": True},
			"rules": {nodetype.__name__: True for nodetype in module.nodetypes},
		}
		module.initialize(config)
		mathml = (
			"<math><mrow><mi>x</mi><mo>=</mo><mfrac>"
			"<mrow><mo>-</mo><mi>b</mi><mo>+</mo><msqrt><mrow>"
			"<msup><mi>b</mi><mn>2</mn></msup><mo>-</mo><mn>4</mn><mi>a</mi><mi>c</mi>"
			"</mrow></msqrt></mrow>"
			"<mrow><mn>2</mn><mi>a</mi></mrow>"
			"</mfrac></mrow></math>"
		)
		content = module.MathContent("en", mathml)
		seen_types = []

		def walk(node):
			if node.type:
				seen_types.append(node.type.__class__.__name__)
			for child in node.child:
				walk(child)

		walk(content.root)
		self.assertNotIn("MatrixType", seen_types)
		self.assertNotIn("LineType", seen_types)

	def test_caller_audit_symbols_resolve_to_expected_boundaries(self):
		module = importlib.import_module("Access8Math.reader")
		expected_modules = {
			"MathContent": "Access8Math.reader.session",
			"initialize": "Access8Math.reader.semantics",
			"exist_language": "Access8Math.reader.rules",
			"export_language": "Access8Math.reader.rules",
			"clean_user_data": "Access8Math.reader.rules",
			"available_languages": "Access8Math.reader.rules",
			"add_language": "Access8Math.reader.rules",
			"remove_language": "Access8Math.reader.rules",
			"load_unicode_dic": "Access8Math.reader.rules",
			"save_unicode_dic": "Access8Math.reader.rules",
			"load_math_rule": "Access8Math.reader.rules",
			"save_math_rule": "Access8Math.reader.rules",
		}
		for name, expected_module in expected_modules.items():
			with self.subTest(name=name):
				self.assertEqual(getattr(module, name).__module__, expected_module)

		self.assertEqual(module.AUTO_GENERATE, 0)
		self.assertEqual(module.DIC_GENERATE, 1)
		self.assertTrue(module.LOCALE_DIR.endswith(os.path.join("Access8Math", "locale")))

	def test_lightweight_metadata_is_package_owned(self):
		importlib.import_module("Access8Math.reader")
		nodes = importlib.import_module("Access8Math.reader.nodes")
		rules = importlib.import_module("Access8Math.reader.rules")
		semantics = importlib.import_module("Access8Math.reader.semantics")
		self.assertEqual(nodes.AUTO_GENERATE, 0)
		self.assertEqual(nodes.DIC_GENERATE, 1)
		self.assertEqual(rules.NVDASymbolsFetch.__module__, "Access8Math.reader.rules")
		self.assertEqual(semantics.mathrule_info["generics"]["node"], [3, 1, "*"])


if __name__ == "__main__":
	unittest.main()
