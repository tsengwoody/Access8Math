import importlib
import os
import sys
import unittest


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLUGIN_ROOT = os.path.join(PROJECT_ROOT, "addon", "globalPlugins", "Access8Math")


DEMO_CASES = {
	# 範例一：兩分數相乘 \(\frac{1}{2}\times\frac{3}{4}\)
	"fractions_mul": {
		"mathml": "<math><mrow><mfrac><mn>1</mn><mn>2</mn></mfrac><mo>×</mo><mfrac><mn>3</mn><mn>4</mn></mfrac></mrow></math>",
		"expected_types": ["SingleFractionType"],
		"expected_snapshot": [
			("math", "", None),
			("mfrac", "", "SingleFractionType"),
			("mn", "1", None),
			("mn", "2", None),
			("mo", "×", None),
			("mfrac", "", "SingleFractionType"),
			("mn", "3", None),
			("mn", "4", None),
		],
	},
	# 範例2：畢氏定理 \(\sqrt[]{a^2+b^2} = c\)
	"pythagorean": {
		"mathml": "<math><mrow><msqrt><mrow><msup><mi>a</mi><mn>2</mn></msup><mo>+</mo><msup><mi>b</mi><mn>2</mn></msup></mrow></msqrt><mo>=</mo><mi>c</mi></mrow></math>",
		"expected_types": ["SquarePowerType"],
		"expected_snapshot": [
			("math", "", None),
			("msqrt", "", None),
			("msup", "", "SquarePowerType"),
			("mi", "a", None),
			("mn", "2", None),
			("mo", "+", None),
			("msup", "", "SquarePowerType"),
			("mi", "b", None),
			("mn", "2", None),
			("mo", "=", None),
			("mi", "c", None),
		],
	},
	# 範例3：一元二次方程式公式解 \(\frac{-b\pm\sqrt{b^2-4ac}}{2a}\)
	"quadratic_formula": {
		"mathml": "<math><mfrac><mrow><mo>-</mo><mi>b</mi><mo>±</mo><msqrt><mrow><msup><mi>b</mi><mn>2</mn></msup><mo>-</mo><mn>4</mn><mi>a</mi><mi>c</mi></mrow></msqrt></mrow><mrow><mn>2</mn><mi>a</mi></mrow></mfrac></math>",
		"expected_types": ["FirstNegativeSignType", "SquarePowerType"],
		"expected_snapshot": [
			("math", "", None),
			("mfrac", "", None),
			("mrow", "", None),
			("mo", "-", "FirstNegativeSignType"),
			("mi", "b", None),
			("mo", "±", None),
			("msqrt", "", None),
			("msup", "", "SquarePowerType"),
			("mi", "b", None),
			("mn", "2", None),
			("mo", "-", None),
			("mn", "4", None),
			("mi", "a", None),
			("mi", "c", None),
			("mrow", "", None),
			("mn", "2", None),
			("mi", "a", None),
		],
	},
	# 範例4：平方和公式 \(\sum_{k=1}^{n}k^2=\frac{n(n+1)(2n+1)}{6}\)
	"sum_of_squares": {
		"mathml": "<math><mrow><munderover><mo>∑</mo><mrow><mi>k</mi><mo>=</mo><mn>1</mn></mrow><mi>n</mi></munderover><msup><mi>k</mi><mn>2</mn></msup><mo>=</mo><mfrac><mrow><mi>n</mi><mo>(</mo><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow><mo>)</mo><mo>(</mo><mrow><mn>2</mn><mi>n</mi><mo>+</mo><mn>1</mn></mrow><mo>)</mo></mrow><mn>6</mn></mfrac></mrow></math>",
		"expected_types": ["MunderoverFromToType", "SquarePowerType"],
		"expected_snapshot": [
			("math", "", None),
			("munderover", "", "MunderoverFromToType"),
			("mo", "∑", None),
			("mrow", "", None),
			("mi", "k", None),
			("mo", "=", None),
			("mn", "1", None),
			("mi", "n", None),
			("msup", "", "SquarePowerType"),
			("mi", "k", None),
			("mn", "2", None),
			("mo", "=", None),
			("mfrac", "", None),
			("mrow", "", None),
			("mi", "n", None),
			("mo", "(", None),
			("mi", "n", None),
			("mo", "+", None),
			("mn", "1", None),
			("mo", ")", None),
			("mo", "(", None),
			("mn", "2", None),
			("mi", "n", None),
			("mo", "+", None),
			("mn", "1", None),
			("mo", ")", None),
			("mn", "6", None),
		],
	},
	# 範例5：線段平行與垂直 \(\overline{AB}\parallel\overline{EF}\perp\overline{CD}\)
	"parallel_perpendicular": {
		"mathml": "<math><mrow><mover><mrow><mi>A</mi><mi>B</mi></mrow><mo>¯</mo></mover><mo>∥</mo><mover><mrow><mi>E</mi><mi>F</mi></mrow><mo>¯</mo></mover><mo>⟂</mo><mover><mrow><mi>C</mi><mi>D</mi></mrow><mo>¯</mo></mover></mrow></math>",
		"expected_types": ["LineSegmentType"],
		"expected_snapshot": [
			("math", "", None),
			("mover", "", "LineSegmentType"),
			("mrow", "", None),
			("mi", "A", None),
			("mi", "B", None),
			("mo", "¯", None),
			("mo", "∥", None),
			("mover", "", "LineSegmentType"),
			("mrow", "", None),
			("mi", "E", None),
			("mi", "F", None),
			("mo", "¯", None),
			("mo", "⟂", None),
			("mover", "", "LineSegmentType"),
			("mrow", "", None),
			("mi", "C", None),
			("mi", "D", None),
			("mo", "¯", None),
		],
	},
	# 文字描述歧異 case1: \(\sqrt{\frac{b+c}{a}}\)
	"case1": {
		"mathml": "<math><msqrt><mfrac><mrow><mi>b</mi><mo>+</mo><mi>c</mi></mrow><mi>a</mi></mfrac></msqrt></math>",
		"expected_types": ["SingleSqrtType"],
		"expected_snapshot": [
			("math", "", None),
			("msqrt", "", "SingleSqrtType"),
			("mfrac", "", None),
			("mrow", "", None),
			("mi", "b", None),
			("mo", "+", None),
			("mi", "c", None),
			("mi", "a", None),
		],
	},
	# case2: \(\sqrt{\frac{b}{a}+c}\)
	"case2": {
		"mathml": "<math><msqrt><mrow><mfrac><mi>b</mi><mi>a</mi></mfrac><mo>+</mo><mi>c</mi></mrow></msqrt></math>",
		"expected_types": ["SingleFractionType"],
		"expected_snapshot": [
			("math", "", None),
			("msqrt", "", None),
			("mfrac", "", "SingleFractionType"),
			("mi", "b", None),
			("mi", "a", None),
			("mo", "+", None),
			("mi", "c", None),
		],
	},
	# case3: \(\sqrt{\frac{b}{a}}+c\)
	"case3": {
		"mathml": "<math><mrow><msqrt><mfrac><mi>b</mi><mi>a</mi></mfrac></msqrt><mo>+</mo><mi>c</mi></mrow></math>",
		"expected_types": ["SingleFractionType", "SingleSqrtType"],
		"expected_snapshot": [
			("math", "", None),
			("msqrt", "", "SingleSqrtType"),
			("mfrac", "", "SingleFractionType"),
			("mi", "b", None),
			("mi", "a", None),
			("mo", "+", None),
			("mi", "c", None),
		],
	},
	# case4: \(\frac{b+c}{\sqrt{a}}\)
	"case4": {
		"mathml": "<math><mfrac><mrow><mi>b</mi><mo>+</mo><mi>c</mi></mrow><msqrt><mi>a</mi></msqrt></mfrac></math>",
		"expected_types": ["SingleSqrtType"],
		"expected_snapshot": [
			("math", "", None),
			("mfrac", "", None),
			("mrow", "", None),
			("mi", "b", None),
			("mo", "+", None),
			("mi", "c", None),
			("msqrt", "", "SingleSqrtType"),
			("mi", "a", None),
		],
	},
	# case5: \(\frac{b}{\sqrt{a}}+c\)
	"case5": {
		"mathml": "<math><mrow><mfrac><mi>b</mi><msqrt><mi>a</mi></msqrt></mfrac><mo>+</mo><mi>c</mi></mrow></math>",
		"expected_types": ["SingleSqrtType"],
		"expected_snapshot": [
			("math", "", None),
			("mfrac", "", None),
			("mi", "b", None),
			("msqrt", "", "SingleSqrtType"),
			("mi", "a", None),
			("mo", "+", None),
			("mi", "c", None),
		],
	},
}


class TestA8MPMDemoCorpus(unittest.TestCase):
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

	def test_demo_mathml_snapshots_are_stable(self):
		for name, case in DEMO_CASES.items():
			with self.subTest(name=name):
				self.assertEqual(self._snapshot(case["mathml"]), case["expected_snapshot"])

	def test_demo_type_sets_are_stable(self):
		for name, case in DEMO_CASES.items():
			with self.subTest(name=name):
				snapshot = self._snapshot(case["mathml"])
				seen_types = sorted({type_name for _, _, type_name in snapshot if type_name})
				self.assertEqual(seen_types, case["expected_types"])

	def test_demo_corpus_covers_key_nodes_and_nodetypes(self):
		all_tags = set()
		all_types = set()
		for case in DEMO_CASES.values():
			for tag, _, type_name in self._snapshot(case["mathml"]):
				all_tags.add(tag)
				if type_name:
					all_types.add(type_name)

		self.assertTrue(
			{"math", "mfrac", "msqrt", "msup", "munderover", "mover", "mrow", "mi", "mn", "mo"}.issubset(all_tags)
		)
		self.assertTrue(
			{
				"SingleFractionType",
				"SingleSqrtType",
				"SquarePowerType",
				"FirstNegativeSignType",
				"MunderoverFromToType",
				"LineSegmentType",
			}.issubset(all_types)
		)


if __name__ == "__main__":
	unittest.main()
