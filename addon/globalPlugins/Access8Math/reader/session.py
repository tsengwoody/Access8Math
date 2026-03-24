import re

from .rules import load_math_rule, load_unicode_dic
from .tree import (
	check_type_allnode,
	clean_allnode,
	clear_type_allnode,
	create_node,
	includes_unicode_range,
	mathml2etree,
	set_braillemathrule_allnode,
	set_mathcontent_allnode,
	set_mathrule_allnode,
)


def _compile_symbol_pattern(symbol):
	symbol_list = sorted(list(symbol.keys()), key=lambda item: -len(item))
	symbol_list = [item.replace("|", "\\|") for item in symbol_list if not includes_unicode_range(item, 124, 125)]
	restring = "|".join(symbol_list).translate({
		ord("$"): "\\$",
		ord("("): "\\(",
		ord(")"): "\\)",
		ord("*"): "\\*",
		ord("+"): "\\+",
		ord("-"): "\\-",
		ord("."): "\\.",
		ord("?"): "\\?",
		ord("["): "\\[",
		ord("\\"): "\\\\",
		ord("]"): "\\]",
		ord("^"): "\\^",
		ord("{"): "\\{",
		ord("}"): "\\}",
	})
	restring += "|\\|"
	return re.compile(restring)


class MathContent(object):
	def __init__(self, language, mathMl):
		self.raw_mathMl = mathMl
		et = mathml2etree(mathMl)
		self.root = self._pointer = self._history = create_node(et)

		clean_allnode(self.root)
		set_mathcontent_allnode(self.root, self)

		self.set_symbol(load_unicode_dic(language=language, category="speech", NVDASymbol=True))
		self.set_mathrule(load_math_rule(language=language))
		self.set_braillesymbol(load_unicode_dic(language=language, category="braille"))
		self.set_braillemathrule(load_math_rule(language=language, category="braille"))

	@property
	def mathML(self):
		mathmlNamespace = 'xmlns="http://www.w3.org/1998/Math/MathML"'
		result = self.pointer.get_mathml()
		if not result.startswith("<math"):
			result = f"<math {mathmlNamespace}>{result}</math>"
		return result

	def set_mathrule(self, mathrule):
		self.mathrule = mathrule
		set_mathrule_allnode(self.root, mathrule)
		clear_type_allnode(self.root)
		check_type_allnode(self.root)
		set_mathrule_allnode(self.root, mathrule)
		set_mathcontent_allnode(self.root, self)

	def set_braillemathrule(self, mathrule):
		self.braillemathrule = mathrule
		set_braillemathrule_allnode(self.root, mathrule)
		clear_type_allnode(self.root)
		check_type_allnode(self.root)
		set_braillemathrule_allnode(self.root, mathrule)
		set_mathcontent_allnode(self.root, self)

	def set_symbol(self, symbol):
		self.symbol = symbol
		self.symbol_repattern = _compile_symbol_pattern(symbol)

	def set_braillesymbol(self, symbol):
		self.braillesymbol = symbol
		self.braillesymbol_repattern = _compile_symbol_pattern(symbol)

	def navigate(self, action):
		pointer = None
		if action == "downArrow":
			pointer = self.pointer.down
		elif action == "upArrow":
			pointer = self.pointer.up
		elif action == "leftArrow":
			pointer = self.pointer.previous_sibling
		elif action == "rightArrow":
			pointer = self.pointer.next_sibling
		elif action == "home":
			pointer = self.root

		if pointer is not None:
			self.pointer = pointer
			return True

		return False

	def table_navigate(self, action):
		if action == "downArrow":
			pointer = self.pointer.vertical_down
		elif action == "upArrow":
			pointer = self.pointer.vertical_up
		elif action == "leftArrow":
			pointer = self.pointer.previous_sibling
		elif action == "rightArrow":
			pointer = self.pointer.next_sibling
		else:
			pointer = None

		if pointer is not None:
			self.pointer = pointer
			return True

		return False

	def symbol_translate(self, string):
		try:
			return self.symbol_repattern.sub(lambda match: self.symbol[match.group(0)], string)
		except BaseException:
			return string

	def braillesymbol_translate(self, string):
		try:
			return self.braillesymbol_repattern.sub(lambda match: self.braillesymbol[match.group(0)], string)
		except BaseException:
			return string

	@property
	def pointer(self):
		return self._pointer

	@pointer.setter
	def pointer(self, node):
		self._history = self._pointer
		self._pointer = node

	@property
	def hint(self):
		if self._history.tag == "mtd" and self._pointer.tag == "mtd" \
		and self._history.parent.parent == self._pointer.parent.parent \
		and self._history.parent.index_in_parent() != self._pointer.parent.index_in_parent():
			return [self._pointer.parent.des]
		return []

__all__ = ["MathContent"]
