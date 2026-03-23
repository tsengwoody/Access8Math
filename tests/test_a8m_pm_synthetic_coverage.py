import importlib
import os
import sys
import unittest


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLUGIN_ROOT = os.path.join(PROJECT_ROOT, "addon", "globalPlugins", "Access8Math")


SYNTHETIC_TYPE_CASES = {
	"binomial": {
		"mathml": '<math><mfrac linethickness="0"><mi>n</mi><mi>k</mi></mfrac></math>',
		"expected_types": ["BinomialType"],
	},
	"matrix": {
		"mathml": "<math><mrow><mo>[</mo><mtable><mtr><mtd><mi>a</mi></mtd><mtd><mi>b</mi></mtd></mtr><mtr><mtd><mi>c</mi></mtd><mtd><mi>d</mi></mtd></mtr></mtable><mo>]</mo></mrow></math>",
		"expected_types": ["MatrixType"],
	},
	"determinant": {
		"mathml": "<math><mrow><mo>|</mo><mtable><mtr><mtd><mi>a</mi></mtd><mtd><mi>b</mi></mtd></mtr><mtr><mtd><mi>c</mi></mtd><mtd><mi>d</mi></mtd></mtr></mtable><mo>|</mo></mrow></math>",
		"expected_types": ["DeterminantType"],
	},
	"simultaneous_equations": {
		"mathml": "<math><mrow><mo>{</mo><mtable><mtr><mtd><mi>x</mi><mo>+</mo><mi>y</mi><mo>=</mo><mn>1</mn></mtd></mtr><mtr><mtd><mi>x</mi><mo>-</mo><mi>y</mi><mo>=</mo><mn>0</mn></mtd></mtr></mtable></mrow></math>",
		"expected_types": ["SimultaneousEquationsType"],
	},
	"vector_single": {
		"mathml": '<math><mover><mi>v</mi><mo stretchy="false">→</mo></mover></math>',
		"expected_types": ["VectorSingleType"],
	},
	"vector_double": {
		"mathml": '<math><mover><mrow><mi>A</mi><mi>B</mi></mrow><mo stretchy="false">→</mo></mover></math>',
		"expected_types": ["VectorDoubleType"],
	},
	"ray": {
		"mathml": "<math><mover><mrow><mi>A</mi><mi>B</mi></mrow><mo>→</mo></mover></math>",
		"expected_types": ["RayType"],
	},
	"arrow_single": {
		"mathml": "<math><mover><mi>A</mi><mo>→</mo></mover></math>",
		"expected_types": ["ArrowOverSingleSymbolType"],
	},
	"frown": {
		"mathml": "<math><mover><mrow><mi>A</mi><mi>B</mi></mrow><mo>⌢</mo></mover></math>",
		"expected_types": ["FrownType"],
	},
	"degree": {
		"mathml": "<math><msup><mi>x</mi><mo>°</mo></msup></math>",
		"expected_types": ["DegreeType"],
	},
	"power": {
		"mathml": "<math><msup><mi>x</mi><mi>n</mi></msup></math>",
		"expected_types": ["PowerType"],
	},
	"cube_power": {
		"mathml": "<math><msup><mi>x</mi><mn>3</mn></msup></math>",
		"expected_types": ["CubePowerType"],
	},
	"single_msub": {
		"mathml": "<math><msub><mi>a</mi><mi>i</mi></msub></math>",
		"expected_types": ["SingleMsubType"],
	},
	"msup_to": {
		"mathml": "<math><msup><mo>∑</mo><mi>n</mi></msup></math>",
		"expected_types": ["MsupToType"],
	},
	"msub_from": {
		"mathml": "<math><msub><mo>∑</mo><mi>i</mi></msub></math>",
		"expected_types": ["MsubFromType"],
	},
	"msubsup_from_to": {
		"mathml": "<math><msubsup><mo>∑</mo><mi>i</mi><mi>n</mi></msubsup></math>",
		"expected_types": ["MsubsupFromToType"],
	},
	"munder_from": {
		"mathml": "<math><munder><mo>∫</mo><mi>a</mi></munder></math>",
		"expected_types": ["MunderFromType"],
	},
	"mover_to": {
		"mathml": "<math><mover><mo>∫</mo><mi>b</mi></mover></math>",
		"expected_types": ["MoverToType"],
	},
	"msub_log": {
		"mathml": "<math><msub><mi>log</mi><mi>2</mi></msub></math>",
		"expected_types": ["MsubLogType"],
	},
	"single_munderover": {
		"mathml": "<math><munderover><mi>X</mi><mi>a</mi><mi>b</mi></munderover></math>",
		"expected_types": ["SingleMunderoverType"],
	},
	"single_munder": {
		"mathml": "<math><munder><mi>X</mi><mi>a</mi></munder></math>",
		"expected_types": ["SingleMunderType"],
	},
	"single_mover": {
		"mathml": "<math><mover><mi>X</mi><mi>b</mi></mover></math>",
		"expected_types": ["SingleMoverType"],
	},
	"add_integer_fraction": {
		"mathml": "<math><mrow><mn>1</mn><mfrac><mn>1</mn><mn>2</mn></mfrac></mrow></math>",
		"expected_types": ["AddIntegerFractionType"],
	},
	"negative_sign_after_operator": {
		"mathml": "<math><mrow><mi>a</mi><mo>×</mo><mo>-</mo><mi>b</mi></mrow></math>",
		"expected_types": ["NegativeSignType"],
	},
	"positive_sign_first": {
		"mathml": "<math><mrow><mo>+</mo><mi>x</mi></mrow></math>",
		"expected_types": ["FirstPositiveSignType"],
	},
	"positive_sign_after_operator": {
		"mathml": "<math><mrow><mi>a</mi><mo>=</mo><mo>+</mo><mi>b</mi></mrow></math>",
		"expected_types": ["PositiveSignType"],
	},
}


NODE_ONLY_CASES = {
	"menclose": {
		"mathml": '<math><menclose notation="box"><mi>x</mi></menclose></math>',
		"expected_snapshot": [("math", "", None), ("menclose", "", None), ("mi", "x", None)],
	},
	"mfenced": {
		"mathml": '<math><mfenced open="[" close="]"><mi>x</mi><mi>y</mi></mfenced></math>',
		"expected_snapshot": [("math", "", None), ("mfenced", "", None), ("mi", "x", None), ("mi", "y", None)],
	},
	"mroot": {
		"mathml": "<math><mroot><mi>x</mi><mn>3</mn></mroot></math>",
		"expected_snapshot": [("math", "", None), ("mroot", "", None), ("mi", "x", None), ("mn", "3", None)],
	},
	"mmultiscripts": {
		"mathml": "<math><mmultiscripts><mi>T</mi><mi>a</mi><mi>b</mi><mprescripts/><mi>c</mi><mi>d</mi></mmultiscripts></math>",
		"expected_snapshot": [
			("math", "", None),
			("mmultiscripts", "", None),
			("mi", "T", None),
			("mi", "a", None),
			("mi", "b", None),
			("mprescripts", "", None),
			("mi", "c", None),
			("mi", "d", None),
		],
	},
}


NODETYPE_PROBES = [
	("matrix", "mo", "[", "OpenMatrixType"),
	("matrix", "mo", "]", "CloseMatrixType"),
	("matrix", "mtable", None, "MtableType"),
	("matrix", "mtable", None, "MatrixType"),
	("absolute_probe", "mo", "|", "VerticalBarType"),
	("absolute_probe", "mn", "5", "MnOperandType"),
	("line", "mo", "↔", "MoLineType"),
	("line", "mover", None, "LineType"),
	("line", "mrow", None, "TwoMiOperandItemType"),
	("line_segment", "mo", "¯", "MoLineSegmentType"),
	("line_segment", "mover", None, "LineSegmentType"),
	("vector_single", "mo", "→", "MoVectorType"),
	("vector_single", "mover", None, "VectorSingleType"),
	("ray", "mo", "→", "MoRayType"),
	("ray", "mover", None, "RayType"),
	("frown", "mo", "⌢", "MoFrownType"),
	("frown", "mover", None, "FrownType"),
	("degree", "mo", "°", "MoDegreeType"),
	("degree", "msup", None, "DegreeType"),
	("msub_log", "mi", "log", "LogOperatorType"),
	("msub_log", "msub", None, "MsubLogType"),
	("msubsup_from_to", "mo", "∑", "FromToOperatorType"),
	("msubsup_from_to", "msubsup", None, "MsubsupFromToType"),
	("negative_sign_after_operator", "mo", "×", "SignPreviousMoType"),
	("negative_sign_after_operator", "mo", "-", "MinusType"),
	("negative_sign_after_operator", "mo", "-", "NegativeSignType"),
	("positive_sign_after_operator", "mo", "+", "PlusType"),
	("positive_sign_after_operator", "mo", "+", "PositiveSignType"),
]


PROBE_CASE_MATHML = {
	"absolute_probe": "<math><mrow><mo>|</mo><mn>5</mn><mo>|</mo></mrow></math>",
	"matrix": SYNTHETIC_TYPE_CASES["matrix"]["mathml"],
	"line": "<math><mover><mrow><mi>A</mi><mi>B</mi></mrow><mo>↔</mo></mover></math>",
	"line_segment": "<math><mover><mrow><mi>A</mi><mi>B</mi></mrow><mo>¯</mo></mover></math>",
	"vector_single": SYNTHETIC_TYPE_CASES["vector_single"]["mathml"],
	"ray": SYNTHETIC_TYPE_CASES["ray"]["mathml"],
	"frown": SYNTHETIC_TYPE_CASES["frown"]["mathml"],
	"degree": SYNTHETIC_TYPE_CASES["degree"]["mathml"],
	"msub_log": SYNTHETIC_TYPE_CASES["msub_log"]["mathml"],
	"msubsup_from_to": SYNTHETIC_TYPE_CASES["msubsup_from_to"]["mathml"],
	"negative_sign_after_operator": SYNTHETIC_TYPE_CASES["negative_sign_after_operator"]["mathml"],
	"positive_sign_after_operator": SYNTHETIC_TYPE_CASES["positive_sign_after_operator"]["mathml"],
}


class TestA8MPMSyntheticCoverage(unittest.TestCase):
	def setUp(self):
		if PLUGIN_ROOT not in sys.path:
			sys.path.insert(0, PLUGIN_ROOT)
		for name in list(sys.modules):
			if name == "A8M_PM" or name.startswith("A8M_PM."):
				sys.modules.pop(name, None)
		self.module = importlib.import_module("A8M_PM")
		config = {
			"settings": {"analyze_math_meaning": True},
			"rules": {nodetype.__name__: True for nodetype in self.module.nodetypes},
		}
		self.module.initialize(config)

	def _snapshot(self, mathml):
		content = self.module.MathContent("en", mathml)
		result = []

		def walk(node):
			result.append((node.tag, getattr(node, "data", ""), node.type.__class__.__name__ if node.type else None))
			for child in node.child:
				walk(child)

		walk(content.root)
		return result

	def _find_first(self, mathml, tag=None, data=None):
		content = self.module.MathContent("en", mathml)
		queue = [content.root]
		while queue:
			node = queue.pop(0)
			if (tag is None or node.tag == tag) and (data is None or getattr(node, "data", "") == data):
				return node
			queue[0:0] = node.child
		self.fail(f"node not found for tag={tag!r}, data={data!r}")

	def test_synthetic_type_assignments_are_stable(self):
		for name, case in SYNTHETIC_TYPE_CASES.items():
			with self.subTest(name=name):
				snapshot = self._snapshot(case["mathml"])
				seen_types = sorted({type_name for _, _, type_name in snapshot if type_name})
				self.assertEqual(seen_types, case["expected_types"])

	def test_special_node_snapshots_are_stable(self):
		for name, case in NODE_ONLY_CASES.items():
			with self.subTest(name=name):
				self.assertEqual(self._snapshot(case["mathml"]), case["expected_snapshot"])

	def test_synthetic_nodetype_predicates_match_expected_nodes(self):
		for case_name, tag, data, nodetype_name in NODETYPE_PROBES:
			with self.subTest(case=case_name, nodetype=nodetype_name):
				node = self._find_first(PROBE_CASE_MATHML[case_name], tag=tag, data=data)
				nodetype = getattr(self.module, nodetype_name)
				self.assertTrue(nodetype.check(node))

	def test_synthetic_suite_expands_node_and_nodetype_coverage(self):
		all_tags = set()
		all_types = set()
		for case in SYNTHETIC_TYPE_CASES.values():
			for tag, _, type_name in self._snapshot(case["mathml"]):
				all_tags.add(tag)
				if type_name:
					all_types.add(type_name)
		for case in NODE_ONLY_CASES.values():
			for tag, _, _ in self._snapshot(case["mathml"]):
				all_tags.add(tag)

		self.assertTrue(
			{
				"mroot",
				"mfenced",
				"menclose",
				"mtable",
				"mtr",
				"mtd",
				"msub",
				"msubsup",
				"munder",
				"mover",
				"munderover",
				"mmultiscripts",
				"mprescripts",
			}.issubset(all_tags)
		)
		self.assertTrue(
			{
				"BinomialType",
				"MatrixType",
				"DeterminantType",
				"SimultaneousEquationsType",
				"VectorSingleType",
				"VectorDoubleType",
				"RayType",
				"ArrowOverSingleSymbolType",
				"FrownType",
				"DegreeType",
				"PowerType",
				"CubePowerType",
				"SingleMsubType",
				"MsubsupFromToType",
				"MunderFromType",
				"MoverToType",
				"MsubLogType",
				"SingleMunderoverType",
				"SingleMunderType",
				"SingleMoverType",
				"AddIntegerFractionType",
				"NegativeSignType",
				"FirstPositiveSignType",
				"PositiveSignType",
			}.issubset(all_types)
		)


if __name__ == "__main__":
	unittest.main()
