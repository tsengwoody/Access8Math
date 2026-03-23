import importlib
import importlib.util
import os
import sys
import unittest


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLUGIN_ROOT = os.path.join(PROJECT_ROOT, "addon", "globalPlugins", "Access8Math")
LEGACY_SHIM_PATH = os.path.join(PLUGIN_ROOT, "A8M_PM.py")


class TestA8MPMPackageCompatibility(unittest.TestCase):
	def setUp(self):
		if PLUGIN_ROOT not in sys.path:
			sys.path.insert(0, PLUGIN_ROOT)
		for name in list(sys.modules):
			if name == "A8M_PM" or name.startswith("A8M_PM."):
				sys.modules.pop(name, None)

	def test_a8m_pm_is_package_backed_facade(self):
		module = importlib.import_module("A8M_PM")
		self.assertTrue(module.__file__.endswith(os.path.join("A8M_PM", "__init__.py")))
		self.assertTrue(hasattr(module, "MathContent"))

	def test_legacy_shim_file_is_not_required_for_import(self):
		self.assertFalse(os.path.exists(LEGACY_SHIM_PATH))
		module = importlib.import_module("A8M_PM")
		self.assertTrue(module.__file__.endswith(os.path.join("A8M_PM", "__init__.py")))

	def test_package_import_does_not_load_legacy_runtime_module(self):
		importlib.import_module("A8M_PM")
		self.assertNotIn("A8M_PM._legacy_impl", sys.modules)

	def test_package_import_does_not_load_core_impl_module(self):
		importlib.import_module("A8M_PM")
		self.assertNotIn("A8M_PM._core_impl", sys.modules)

	def test_core_impl_module_is_not_importable(self):
		self.assertIsNone(importlib.util.find_spec("A8M_PM._core_impl"))

	def test_facade_exports_boundary_owned_symbols(self):
		module = importlib.import_module("A8M_PM")
		expected_modules = {
			"MathContent": "A8M_PM.session",
			"initialize": "A8M_PM.semantics",
			"MathRule": "A8M_PM.rules",
			"includes_unicode_range": "A8M_PM.tree",
			"Node": "A8M_PM.nodes",
		}
		for name, expected_module in expected_modules.items():
			with self.subTest(name=name):
				self.assertEqual(getattr(module, name).__module__, expected_module)
		self.assertEqual(module.LOCALE_DIR, importlib.import_module("A8M_PM.rules").LOCALE_DIR)

	def test_internal_boundaries_are_importable(self):
		for name in ["tree", "nodes", "semantics", "rules", "session"]:
			with self.subTest(name=name):
				submodule = importlib.import_module(f"A8M_PM.{name}")
				self.assertIsNotNone(submodule)

	def test_rule_and_language_api_is_provided_by_rules_boundary(self):
		module = importlib.import_module("A8M_PM")
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
				self.assertEqual(getattr(module, name).__module__, "A8M_PM.rules")

	def test_tree_and_node_api_is_provided_by_extracted_boundaries(self):
		module = importlib.import_module("A8M_PM")
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
				self.assertEqual(getattr(module, name).__module__, "A8M_PM.tree")

		for name in ["Node", "NonTerminalNode", "TerminalNode", "Math", "Mrow", "Mi", "Mo", "Mn"]:
			with self.subTest(name=name):
				self.assertEqual(getattr(module, name).__module__, "A8M_PM.nodes")

	def test_tree_and_node_behavior_remains_usable(self):
		module = importlib.import_module("A8M_PM")
		root = module.create_node(
			module.mathml2etree("<math><mrow><mi>x</mi><mo>+</mo><mi>y</mi></mrow></math>")
		)
		module.clean_allnode(root)
		self.assertEqual(root.__class__.__module__, "A8M_PM.nodes")
		self.assertEqual(root.tag, "math")
		self.assertEqual(root.down.tag, "mi")
		self.assertEqual(root.down.next_sibling.tag, "mo")
		self.assertEqual(root.down.next_sibling.next_sibling.tag, "mi")
		self.assertIn("<mi>x</mi>", root.get_mathml())

	def test_semantics_api_and_registry_are_provided_by_semantics_boundary(self):
		module = importlib.import_module("A8M_PM")
		self.assertEqual(module.NodeType.__module__, "A8M_PM.semantics")
		self.assertEqual(module.TerminalNodeType.__module__, "A8M_PM.semantics")
		self.assertEqual(module.NonTerminalNodeType.__module__, "A8M_PM.semantics")
		self.assertEqual(module.SiblingNodeType.__module__, "A8M_PM.semantics")
		self.assertEqual(module.CompoundNodeType.__module__, "A8M_PM.semantics")
		self.assertEqual(module.initialize.__module__, "A8M_PM.semantics")
		self.assertGreater(len(module.nodetypes), 0)
		self.assertEqual(module.nodetypes[0].__module__, "A8M_PM.semantics")
		self.assertEqual(module.all_nodetypes_dict["object"], object)

	def test_initialize_uses_explicit_semantics_registry(self):
		module = importlib.import_module("A8M_PM")
		config = {
			"settings": {"analyze_math_meaning": True},
			"rules": {nodetype.__name__: True for nodetype in module.nodetypes},
		}
		module.initialize(config)
		self.assertGreater(len(module.nodetypes_check), 0)
		self.assertTrue(all(nodetype.__module__ == "A8M_PM.semantics" for nodetype in module.nodetypes_check))

	def test_mathcontent_is_provided_by_session_boundary(self):
		module = importlib.import_module("A8M_PM")
		self.assertEqual(module.MathContent.__module__, "A8M_PM.session")

	def test_mathcontent_orchestrates_extracted_boundaries(self):
		module = importlib.import_module("A8M_PM")
		config = {
			"settings": {"analyze_math_meaning": True},
			"rules": {nodetype.__name__: True for nodetype in module.nodetypes},
		}
		module.initialize(config)
		content = module.MathContent("en", "<math><mrow><mi>x</mi><mo>+</mo><mi>y</mi></mrow></math>")
		self.assertEqual(content.root.__class__.__module__, "A8M_PM.nodes")
		self.assertEqual(content.pointer.__class__.__module__, "A8M_PM.nodes")
		self.assertEqual(module.load_math_rule.__module__, "A8M_PM.rules")
		self.assertEqual(module.mathml2etree.__module__, "A8M_PM.tree")
		self.assertTrue(content.navigate("downArrow"))
		self.assertEqual(content.pointer.tag, "mi")

	def test_quadratic_formula_is_not_misclassified_as_matrix(self):
		module = importlib.import_module("A8M_PM")
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
		module = importlib.import_module("A8M_PM")
		expected_modules = {
			"MathContent": "A8M_PM.session",
			"initialize": "A8M_PM.semantics",
			"exist_language": "A8M_PM.rules",
			"export_language": "A8M_PM.rules",
			"clean_user_data": "A8M_PM.rules",
			"available_languages": "A8M_PM.rules",
			"add_language": "A8M_PM.rules",
			"remove_language": "A8M_PM.rules",
			"load_unicode_dic": "A8M_PM.rules",
			"save_unicode_dic": "A8M_PM.rules",
			"load_math_rule": "A8M_PM.rules",
			"save_math_rule": "A8M_PM.rules",
		}
		for name, expected_module in expected_modules.items():
			with self.subTest(name=name):
				self.assertEqual(getattr(module, name).__module__, expected_module)

		self.assertEqual(module.AUTO_GENERATE, 0)
		self.assertEqual(module.DIC_GENERATE, 1)
		self.assertTrue(module.LOCALE_DIR.endswith(os.path.join("Access8Math", "locale")))

	def test_lightweight_metadata_is_package_owned(self):
		importlib.import_module("A8M_PM")
		nodes = importlib.import_module("A8M_PM.nodes")
		rules = importlib.import_module("A8M_PM.rules")
		semantics = importlib.import_module("A8M_PM.semantics")
		self.assertEqual(nodes.AUTO_GENERATE, 0)
		self.assertEqual(nodes.DIC_GENERATE, 1)
		self.assertEqual(rules.NVDASymbolsFetch.__module__, "A8M_PM.rules")
		self.assertEqual(semantics.mathrule_info["generics"]["node"], [3, 1, "*"])


if __name__ == "__main__":
	unittest.main()
