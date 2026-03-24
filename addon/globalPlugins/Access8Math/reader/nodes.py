import re
import weakref

from .metadata import AUTO_GENERATE, DIC_GENERATE


class Node(object):
	def __init__(self, child=None, attrib=None, data=None):
		self._mathcontent = None
		self._parent = None

		self.child = list(child) if child else []
		for c in self.child:
			if isinstance(c, Node):
				c.parent = self

		self.attrib = attrib if attrib else {}
		self.data = str(data.strip()) if data else ""

		self.mathrule = {}
		self.rule = []
		self.role = []

		self.braillemathrule = {}
		self.braillerule = []
		self.braillerole = []

		self.type = None
		self.role_level = None

	def set_mathrule(self, mathrule):
		self.mathrule = mathrule
		self.set_role()
		self.set_rule()
		if self.type:
			self.type.set_mathrule(self.mathrule)

	def set_role(self):
		self.role = (
			self.mathrule[self.name].role
			if self.name in self.mathrule
			else [self.mathcontent.symbol_translate("item")]
		)
		d = len(self.child) - len(self.role)
		if d > 0:
			append = self.role[-1]
			try:
				before, after = append.split(".")
			except ValueError:
				before, after = f"{append}.".split(".")
			self.role = self.role[:-1]
			for i in range(d + 1):
				self.role.append(f"{before}{i + 1}{after}")
			self.role_level = AUTO_GENERATE
		else:
			self.role_level = DIC_GENERATE

	def set_rule(self):
		if self.type and self.type.rule:
			rule = self.type.rule
		else:
			rule = self.mathrule[self.name].serialized_order
		if len(rule) >= 2 and isinstance(rule[1], tuple):
			result = []
			for i in range(len(self.child)):
				before_empty = rule[1][0].isspace() or rule[1][0] == ""
				after_empty = rule[1][1].isspace() or rule[1][1] == ""
				if not (before_empty and after_empty):
					result.append(f"{rule[1][0]}{i + 1}{rule[1][1]}")
				result.append(i)

			rule = rule[0:1] + result + rule[-1:]
		self.rule = rule

	def set_braillemathrule(self, braillemathrule):
		self.braillemathrule = braillemathrule
		self.set_braillerole()
		self.set_braillerule()
		if self.type:
			self.type.set_braillemathrule(self.braillemathrule)

	def set_braillerole(self):
		self.braillerole = (
			self.braillemathrule[self.name].role
			if self.name in self.braillemathrule
			else [self.mathcontent.symbol_translate("item")]
		)
		d = len(self.child) - len(self.braillerole)
		if d > 0:
			append = self.braillerole[-1]
			self.braillerole = self.braillerole[:-1]
			for i in range(d + 1):
				self.braillerole.append(f"{append}{i + 1}")
			self.braillerole_level = AUTO_GENERATE
		else:
			self.braillerole_level = DIC_GENERATE

	def set_braillerule(self):
		if self.type and self.type.braillerule:
			braillerule = self.type.braillerule
		else:
			braillerule = self.braillemathrule[self.name].serialized_order

		if len(braillerule) >= 2 and isinstance(braillerule[1], tuple):
			result = []
			for i in range(len(self.child)):
				before_empty = braillerule[1][0].isspace() or braillerule[1][0] == ""
				after_empty = braillerule[1][1].isspace() or braillerule[1][1] == ""
				if not (before_empty and after_empty):
					result.append(f"{braillerule[1][0]}{i + 1}{braillerule[1][1]}")
				result.append(i)

			braillerule = braillerule[0:1] + result + braillerule[-1:]

		self.braillerule = braillerule

	def serialized(self):
		serialized = []
		for r in self.rule:
			if isinstance(r, int):
				serialized.append(self.child[r].serialized())
			elif r == "*":
				for c in self.child:
					if c:
						serialized.append(c.serialized())
			elif isinstance(r, str):
				serialized.append([r])
			else:
				raise TypeError(f"rule element type error : expect int or str (get {type(r)})")
		return serialized

	def brailleserialized(self):
		serialized = []
		for r in self.braillerule:
			if isinstance(r, int):
				serialized.append(self.child[r].brailleserialized())
			elif r == "*":
				for c in self.child:
					if c:
						serialized.append(c.brailleserialized())
			elif isinstance(r, str):
				serialized.append([r])
			else:
				raise TypeError(f"rule element type error : expect int or str (get {type(r)})")
		return serialized

	def get_mathml(self):
		mathml = ""
		if len(self.child) > 0:
			for c in self.child:
				mathml = mathml + c.get_mathml()
		else:
			mathml = mathml + " "

		attrib = ""
		for k, v in self.attrib.items():
			attrib = attrib + f' {k}="{v}"'

		if len(attrib) > 0:
			result = f"<{self.tag} {attrib}>{mathml}</{self.tag}>"
		else:
			result = f"<{self.tag}>{mathml}</{self.tag}>"

		return result

	@property
	def mathcontent(self):
		return None if self._mathcontent is None else self._mathcontent()

	@mathcontent.setter
	def mathcontent(self, mathcontent):
		self._mathcontent = weakref.ref(mathcontent)

	@property
	def des(self):
		return self.parent.role[self.index_in_parent()] if self.parent else self.mathcontent.symbol_translate("math")

	@property
	def name(self):
		return self.type.name if self.type else self.tag

	@property
	def tag(self):
		return self.__class__.__name__.lower()

	@property
	def parent(self):
		return None if self._parent is None else self._parent()

	@parent.setter
	def parent(self, node):
		self._parent = weakref.ref(node)

	def index_in_parent(self):
		try:
			return self.parent.child.index(self)
		except BaseException:
			return None

	@property
	def next_sibling(self):
		try:
			index = self.index_in_parent() + 1
			if index < 0:
				raise IndexError("index out of range")
		except BaseException:
			index = None

		try:
			return self.parent.child[index]
		except BaseException:
			return None

	@property
	def previous_sibling(self):
		try:
			index = self.index_in_parent() - 1
			if index < 0:
				raise IndexError("index out of range")
		except BaseException:
			index = None

		try:
			return self.parent.child[index]
		except BaseException:
			return None

	@property
	def next(self):
		current = self
		_next = current.next_sibling
		while not _next:
			current = current.parent
			if not current:
				return None
			_next = current.next_sibling
		return _next

	@property
	def previous(self):
		current = self
		previous = current.previous_sibling
		while not previous:
			current = current.parent
			if not current:
				return None
			previous = current.previous_sibling
		return previous

	@property
	def down(self):
		try:
			return self.child[0]
		except BaseException:
			return None

	@property
	def up(self):
		try:
			return self.parent
		except BaseException:
			return None

	@property
	def vertical_down(self):
		if self.tag == "mtd":
			index = self.index_in_parent()
			if index >= 0:
				parent_next_sibling = self.parent.next_sibling
				if parent_next_sibling:
					try:
						return parent_next_sibling.child[index]
					except IndexError:
						pass

		return None

	@property
	def vertical_up(self):
		if self.tag == "mtd":
			index = self.index_in_parent()
			if index >= 0:
				parent_previous_sibling = self.parent.previous_sibling
				if parent_previous_sibling:
					try:
						return parent_previous_sibling.child[index]
					except IndexError:
						pass

		return None


class NonTerminalNode(Node):
	def set_rule(self):
		try:
			super().set_rule()
		except BaseException:
			self.rule = range(len(self.child))

	def set_role(self):
		try:
			super().set_role()
		except BaseException:
			self.rule = range(len(self.child))

	def set_braillerule(self):
		try:
			super().set_braillerule()
		except BaseException:
			self.braillerule = range(len(self.child))

	def set_braillerole(self):
		try:
			super().set_braillerole()
		except BaseException:
			self.braillerule = range(len(self.child))


class TerminalNode(Node):
	def set_rule(self):
		try:
			super().set_rule()
		except BaseException:
			self.rule = [str(self.mathcontent.symbol_translate(self.data))]

	def set_braillerule(self):
		try:
			super().set_braillerule()
		except BaseException:
			self.braillerule = [str(self.mathcontent.braillesymbol_translate(self.data))]

	def get_mathml(self):
		mathml = ""
		mathml = mathml + self.data if self.data else mathml

		attrib = ""
		for k, v in self.attrib.items():
			attrib = attrib + f' {k}="{v}"'

		if len(attrib) > 0:
			result = f"<{self.tag} {attrib}>{mathml}</{self.tag}>"
		else:
			result = f"<{self.tag}>{mathml}</{self.tag}>"

		return result


class AlterNode(NonTerminalNode):
	pass


class FixNode(NonTerminalNode):
	pass


class BlockNode(AlterNode):
	pass


class Mphantom(AlterNode):
	def set_rule(self):
		return []

	def set_braillerule(self):
		return []


class Mfenced(AlterNode):
	def set_rule(self):
		super().set_rule()
		rule = self.rule
		if not self.type:
			if "open" in self.attrib:
				start_text = [self.mathcontent.symbol_translate(self.attrib["open"]), rule[0]]
			else:
				start_text = [self.mathcontent.symbol_translate("("), rule[0]]
			if "close" in self.attrib:
				end_text = [self.mathcontent.symbol_translate(self.attrib["close"]), rule[-1]]
			else:
				end_text = [self.mathcontent.symbol_translate(")"), rule[-1]]
			rule = start_text + rule[1:-1] + end_text

		self.rule = rule

	def set_braillerule(self):
		super().set_braillerule()
		braillerule = self.braillerule
		if not self.type:
			if "open" in self.attrib:
				start_text = [self.mathcontent.braillesymbol_translate(self.attrib["open"]), braillerule[0]]
			else:
				start_text = [self.mathcontent.braillesymbol_translate("("), braillerule[0]]
			if "close" in self.attrib:
				end_text = [self.mathcontent.braillesymbol_translate(self.attrib["close"]), braillerule[-1]]
			else:
				end_text = [self.mathcontent.braillesymbol_translate(")"), braillerule[-1]]
			braillerule = start_text + braillerule[1:-1] + end_text

		self.braillerule = braillerule


class Menclose(AlterNode):
	def set_rule(self):
		super().set_rule()
		rule = self.rule

		value2description = {
			"longdiv": "long division symbol",
			"actuarial": "actuarial symbol",
			"radical": "radical",
			"box": "box",
			"roundedbox": "round box",
			"circle": "circle",
			"left": "line on left",
			"right": "line on right",
			"top": "line on top",
			"bottom": "line on bottom",
			"updiagonalstrike": "up diagonal cross out",
			"downdiagonalstrike": "down diagonal cross out",
			"verticalstrike": "vertical cross out",
			"horizontalstrike": "horizontal cross out",
			"madruwb": "Arabic factorial symbol",
			"updiagonalarrow": "diagonal arrow",
			"phasorangle": "phasor angle",
		}
		try:
			notation = self.attrib["notation"]
		except BaseException:
			notation = "longdiv"

		try:
			description = self.mathcontent.symbol_translate(f"notation:{value2description[notation]}")
		except BaseException:
			description = ""

		head = rule[0].replace("{start}", description)
		cell = rule[1:-1]
		tail = rule[-1].replace("{end}", description)
		self.rule = [head] + cell + [tail]

	def set_braillerule(self):
		pass


class Mtable(AlterNode):
	def set_rule(self):
		super().set_rule()

		rule = self.rule

		if not self.type:
			row_count = len(self.child)
			column_count_list = [len(i.child) for i in self.child]
			column_count = max(column_count_list)
			table_head = [
				rule[0]
				+ f"{self.mathcontent.symbol_translate('has')}{row_count}"
				+ f"{self.mathcontent.symbol_translate('row')}{column_count}"
				+ f"{self.mathcontent.symbol_translate('column')}"
			]
		else:
			table_head = [rule[0]]
		cell = rule[1:-1]
		table_tail = rule[-1:]
		self.rule = table_head + cell + table_tail

	def set_braillerule(self):
		super().set_braillerule()
		braillerule = self.braillerule

		if not self.type:
			row_count = len(self.child)
			column_count_list = [len(i.child) for i in self.child]
			column_count = max(column_count_list)
			table_head = [
				braillerule[0]
				+ f"{self.mathcontent.braillesymbol_translate('')}{row_count}"
				+ f"{self.mathcontent.braillesymbol_translate('r')}{column_count}"
				+ f"{self.mathcontent.braillesymbol_translate('c')}⠀"
			]
		else:
			table_head = [braillerule[0]]
		cell = braillerule[1:-1]
		table_tail = braillerule[-1:]
		self.braillerule = table_head + cell + table_tail


class Mtr(AlterNode):
	def set_rule(self):
		super().set_rule()
		rule = self.rule
		cell = rule[1:-1]
		self.rule = rule[:1] + cell + rule[-1:]

	def set_braillerule(self):
		super().set_braillerule()
		braillerule = self.braillerule
		cell = braillerule[1:-1]
		self.braillerule = braillerule[:1] + cell + braillerule[-1:]


class Math(AlterNode):
	def get_mathml(self):
		mathml = ""
		mathml_namespace = 'xmlns="http://www.w3.org/1998/Math/MathML"'
		for c in self.child:
			mathml = mathml + c.get_mathml()

		attrib = ""
		for k, v in self.attrib.items():
			k = re.sub(r"\{.*\}", "", k)
			attrib = attrib + f' {k}="{v}"'

		if len(attrib) > 0:
			result = f"<{self.tag} {mathml_namespace} {attrib}>{mathml}</{self.tag}>"
		else:
			result = f"<{self.tag} {mathml_namespace}>{mathml}</{self.tag}>"

		return result


class Mmultiscripts(AlterNode):
	def set_rule(self):
		super().set_rule()
		self.role_level = DIC_GENERATE
		rule = self.rule

		mmrule = []

		index = range(self.mprescripts_index_in_child() + 1, len(self.child))
		index_odd = index[0::2]
		index_even = index[1::2]
		index_mix = zip(index_odd, index_even)
		for count, item in enumerate(index_mix):
			temp = [
				f"{self.mathcontent.symbol_translate('mmultiscripts:order')}{count + 1}{self.mathcontent.symbol_translate('mmultiscripts:pre-subscript')}",
				item[0],
				f"{self.mathcontent.symbol_translate('mmultiscripts:order')}{count + 1}{self.mathcontent.symbol_translate('mmultiscripts:pre-superscript')}",
				item[1],
			]
			mmrule.extend(temp)

		index = range(1, self.mprescripts_index_in_child())
		index_odd = index[0::2]
		index_even = index[1::2]
		index_mix = zip(index_odd, index_even)
		for count, item in enumerate(index_mix):
			temp = [
				f"{self.mathcontent.symbol_translate('mmultiscripts:order')}{count + 1}{self.mathcontent.symbol_translate('mmultiscripts:post-subscript')}",
				item[0],
				f"{self.mathcontent.symbol_translate('mmultiscripts:order')}{count + 1}{self.mathcontent.symbol_translate('mmultiscripts:post-superscript')}",
				item[1],
			]
			mmrule.extend(temp)

		mmrule.insert(0, 0)

		rule = rule[:1] + mmrule + rule[-1:]
		self.rule = rule

	def set_braillerule(self):
		pass

	def set_role(self):
		super().set_role()
		mmrole = [self.mathcontent.symbol_translate("main")]

		index = range(1, self.mprescripts_index_in_child())
		index_odd = index[0::2]
		index_even = index[1::2]
		index_mix = zip(index_odd, index_even)
		for count, item in enumerate(index_mix):
			temp = [
				f"{self.mathcontent.symbol_translate('mmultiscripts:order')}{count + 1}{self.mathcontent.symbol_translate('mmultiscripts:post-subscript')}",
				f"{self.mathcontent.symbol_translate('mmultiscripts:order')}{count + 1}{self.mathcontent.symbol_translate('mmultiscripts:post-superscript')}",
			]
			mmrole.extend(temp)

		mmrole.append(self.mathcontent.symbol_translate("mmultiscripts:mprescripts"))

		index = range(self.mprescripts_index_in_child() + 1, len(self.child))
		index_odd = index[0::2]
		index_even = index[1::2]
		index_mix = zip(index_odd, index_even)
		for count, item in enumerate(index_mix):
			temp = [
				f"{self.mathcontent.symbol_translate('mmultiscripts:order')}{count + 1}{self.mathcontent.symbol_translate('mmultiscripts:pre-subscript')}",
				f"{self.mathcontent.symbol_translate('mmultiscripts:order')}{count + 1}{self.mathcontent.symbol_translate('mmultiscripts:pre-superscript')}",
			]
			mmrole.extend(temp)

		self.role = mmrole

	def mprescripts_index_in_child(self):
		for c in self.child:
			if isinstance(c, Mprescripts):
				return self.child.index(c)
		return None


class Nones(TerminalNode):
	def set_rule(self):
		self.rule = [self.mathcontent.symbol_translate("none")]


class Mrow(BlockNode):
	pass


class Mfrac(FixNode):
	pass


class Msqrt(AlterNode):
	pass


class Mroot(FixNode):
	pass


class Mstyle(BlockNode):
	pass


class Merror(AlterNode):
	pass


class Mpadded(AlterNode):
	pass


class Msub(FixNode):
	pass


class Msup(FixNode):
	pass


class Msubsup(FixNode):
	pass


class Munder(FixNode):
	pass


class Mover(FixNode):
	pass


class Munderover(FixNode):
	pass


class Mlabeledtr(AlterNode):
	pass


class Mtd(AlterNode):
	pass


class Mstack(AlterNode):
	pass


class Mlongdiv(AlterNode):
	pass


class Msgroup(AlterNode):
	pass


class Msrow(AlterNode):
	pass


class Mscarries(AlterNode):
	pass


class Mscarry(AlterNode):
	pass


class Maction(AlterNode):
	pass


class Mi(TerminalNode):
	pass


class Mn(TerminalNode):
	pass


class Mo(TerminalNode):
	pass


class Mtext(TerminalNode):
	pass


class Mspace(TerminalNode):
	def set_rule(self):
		self.rule = []


class Ms(TerminalNode):
	pass


class Mprescripts(TerminalNode):
	pass

nodes = {
	"Node": Node,
	"NonTerminalNode": NonTerminalNode,
	"TerminalNode": TerminalNode,
	"AlterNode": AlterNode,
	"FixNode": FixNode,
	"BlockNode": BlockNode,
	"Mphantom": Mphantom,
	"Mfenced": Mfenced,
	"Menclose": Menclose,
	"Mtable": Mtable,
	"Mtr": Mtr,
	"Math": Math,
	"Mmultiscripts": Mmultiscripts,
	"Nones": Nones,
	"Mrow": Mrow,
	"Mfrac": Mfrac,
	"Msqrt": Msqrt,
	"Mroot": Mroot,
	"Mstyle": Mstyle,
	"Merror": Merror,
	"Mpadded": Mpadded,
	"Msub": Msub,
	"Msup": Msup,
	"Msubsup": Msubsup,
	"Munder": Munder,
	"Mover": Mover,
	"Munderover": Munderover,
	"Mlabeledtr": Mlabeledtr,
	"Mtd": Mtd,
	"Mstack": Mstack,
	"Mlongdiv": Mlongdiv,
	"Msgroup": Msgroup,
	"Msrow": Msrow,
	"Mscarries": Mscarries,
	"Mscarry": Mscarry,
	"Maction": Maction,
	"Mi": Mi,
	"Mn": Mn,
	"Mo": Mo,
	"Mtext": Mtext,
	"Mspace": Mspace,
	"Ms": Ms,
	"Mprescripts": Mprescripts,
}

def _check_type(self):
	from .semantics import nodetypes_check

	for nodetype in nodetypes_check:
		if nodetype.check(self) and nodetype.name in self.mathrule:
			if not self.type:
				self.type = nodetype()
				self.type.mathcontent = self.mathcontent
				self.type.set_mathrule(self.mathrule)
			elif self.type and issubclass(nodetype, self.type.__class__):
				self.type = nodetype()
				self.type.mathcontent = self.mathcontent
				self.type.set_mathrule(self.mathrule)


Node.check_type = _check_type


__all__ = ["AUTO_GENERATE", "DIC_GENERATE", "nodes", *nodes.keys()]
