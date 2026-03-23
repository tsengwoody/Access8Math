import re
import weakref

AUTO_GENERATE = 0
DIC_GENERATE = 1


class Node(object):
	def __init__(self, child=None, attrib=None, data=None):
		self._mathcontent = None
		self._parent = None

		self.child = list(child) if child else []
		for c in self.child:
			if isinstance(c, Node):
				c.parent = self

		self.attrib = attrib if attrib else {}
		self.data = str(data.strip()) if data else ''

		self.mathrule = {}
		self.rule = []
		self.role = []

		self.braillemathrule = {}
		self.braillerule = []
		self.braillerole = []

		self.type = None
		self.role_level = None

	def check_type(self):
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

	def set_mathrule(self, mathrule):
		self.mathrule = mathrule
		self.set_role()
		self.set_rule()
		if self.type:
			self.type.set_mathrule(self.mathrule)

	def set_role(self):
		self.role = self.mathrule[self.name].role if self.name in self.mathrule else [self.mathcontent.symbol_translate('item')]
		d = len(self.child) - len(self.role)
		if d > 0:
			append = self.role[-1]
			try:
				before, after = append.split(".")
			except ValueError:
				before, after = f"{append}.".split(".")
			self.role = self.role[:-1]
			for i in range(d + 1):
				self.role.append(f"{before}{i+1}{after}")
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
				before_empty = (rule[1][0].isspace() or rule[1][0] == '')
				after_empty = (rule[1][1].isspace() or rule[1][1] == '')
				if not (before_empty and after_empty):
					result.append('{0}{1}{2}'.format(rule[1][0], i + 1, rule[1][1]))
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
		self.braillerole = self.braillemathrule[self.name].role if self.name in self.braillemathrule else [self.mathcontent.symbol_translate('item')]
		d = len(self.child) - len(self.braillerole)
		if d > 0:
			append = self.braillerole[-1]
			self.braillerole = self.braillerole[:-1]
			for i in range(d + 1):
				self.braillerole.append('{0}{1}'.format(append, i + 1))
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
				before_empty = (braillerule[1][0].isspace() or braillerule[1][0] == '')
				after_empty = (braillerule[1][1].isspace() or braillerule[1][1] == '')
				if not (before_empty and after_empty):
					result.append('{0}{1}{2}'.format(braillerule[1][0], i + 1, braillerule[1][1]))
				result.append(i)

			braillerule = braillerule[0:1] + result + braillerule[-1:]

		self.braillerule = braillerule

	def serialized(self):
		serialized = []
		for r in self.rule:
			if isinstance(r, int):
				serialized.append(self.child[r].serialized())
			elif r == '*':
				for c in self.child:
					if c:
						serialized.append(c.serialized())
			elif isinstance(r, str):
				serialized.append([r])
			else:
				raise TypeError('rule element type error : expect int or str (get {0})'.format(type(r)))
		return serialized

	def brailleserialized(self):
		serialized = []
		for r in self.braillerule:
			if isinstance(r, int):
				serialized.append(self.child[r].brailleserialized())
			elif r == '*':
				for c in self.child:
					if c:
						serialized.append(c.brailleserialized())
			elif isinstance(r, str):
				serialized.append([r])
			else:
				raise TypeError('rule element type error : expect int or str (get {0})'.format(type(r)))
		return serialized

	def get_mathml(self):
		mathml = ''
		if len(self.child) > 0:
			for c in self.child:
				mathml = mathml + c.get_mathml()
		else:
			mathml = mathml + " "

		attrib = ''
		for k, v in self.attrib.items():
			attrib = attrib + ' {0}="{1}"'.format(k, v)

		if len(attrib) > 0:
			result = f'<{self.tag} {attrib}>{mathml}</{self.tag}>'
		else:
			result = f'<{self.tag}>{mathml}</{self.tag}>'

		return result

	@property
	def mathcontent(self):
		return None if self._mathcontent is None else self._mathcontent()

	@mathcontent.setter
	def mathcontent(self, mathcontent):
		# self._mathcontent = mathcontent
		self._mathcontent = weakref.ref(mathcontent)

	@property
	def des(self):
		return self.parent.role[self.index_in_parent()] if self.parent else self.mathcontent.symbol_translate('math')

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
				raise IndexError('index out of range')
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
				raise IndexError('index out of range')
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
		mathml = ''
		mathml = mathml + self.data if self.data else mathml

		attrib = ''
		for k, v in self.attrib.items():
			attrib = attrib + ' {0}="{1}"'.format(k, v)

		if len(attrib) > 0:
			result = f'<{self.tag} {attrib}>{mathml}</{self.tag}>'
		else:
			result = f'<{self.tag}>{mathml}</{self.tag}>'

		return result


class AlterNode(NonTerminalNode):
	pass


class FixNode(NonTerminalNode):
	pass


class BlockNode(AlterNode):
	pass


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
			if 'open' in self.attrib:
				start_text = [self.mathcontent.symbol_translate(self.attrib['open']), rule[0]]
			else:
				start_text = [self.mathcontent.symbol_translate("("), rule[0]]
			if 'close' in self.attrib:
				end_text = [self.mathcontent.symbol_translate(self.attrib['close']), rule[-1]]
			else:
				end_text = [self.mathcontent.symbol_translate(")"), rule[-1]]
			rule = start_text + rule[1:-1] + end_text

		self.rule = rule

	def set_braillerule(self):
		super().set_braillerule()
		braillerule = self.braillerule
		if not self.type:
			if 'open' in self.attrib:
				start_text = [self.mathcontent.braillesymbol_translate(self.attrib['open']), braillerule[0]]
			else:
				start_text = [self.mathcontent.braillesymbol_translate("("), braillerule[0]]
			if 'close' in self.attrib:
				end_text = [self.mathcontent.braillesymbol_translate(self.attrib['close']), braillerule[-1]]
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
			description = self.mathcontent.symbol_translate("notation:{}".format(value2description[notation]))
		except BaseException:
			description = ""

		head = rule[0].replace("{start}", description)
		cell = rule[1:-1]
		tail = rule[-1].replace("{end}", description)
		self.rule = [head] + cell + [tail]

	def set_braillerule(self):
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


class Mtable(AlterNode):
	def set_rule(self):
		super().set_rule()

		rule = self.rule

		if not self.type:
			row_count = len(self.child)
			column_count_list = [len(i.child) for i in self.child]
			column_count = max(column_count_list)
			table_head = [rule[0] + '{0}{1}{2}{3}{4}'.format(
				self.mathcontent.symbol_translate('has'),
				row_count, self.mathcontent.symbol_translate('row'),
				column_count, self.mathcontent.symbol_translate('column')
			)]
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
			table_head = [braillerule[0] + '{0}{1}{2}{3}{4}⠀'.format(
				self.mathcontent.braillesymbol_translate(''),
				row_count, self.mathcontent.braillesymbol_translate('r'),
				column_count, self.mathcontent.braillesymbol_translate('c')
			)]
		else:
			table_head = [braillerule[0]]
		cell = braillerule[1:-1]
		table_tail = braillerule[-1:]
		self.braillerule = table_head + cell + table_tail


class Mlabeledtr(AlterNode):
	pass


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


class Math(AlterNode):
	def get_mathml(self):
		mathml = ''
		# the xml namespace for mathml. Needed to ensure newer versions of word recognise and render the mathml
		mathmlNamespace = 'xmlns="http://www.w3.org/1998/Math/MathML"'
		for c in self.child:
			mathml = mathml + c.get_mathml()

		attrib = ''
		for k, v in self.attrib.items():
			k = re.sub(r"\{.*\}", "", k)
			attrib = attrib + ' {0}="{1}"'.format(k, v)

		if len(attrib) > 0:
			result = f'<{self.tag} {mathmlNamespace} {attrib}>{mathml}</{self.tag}>'
		else:
			result = f'<{self.tag} {mathmlNamespace}>{mathml}</{self.tag}>'

		return result


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
				'{0}{1}{2}'.format(self.mathcontent.symbol_translate('mmultiscripts:order'), count + 1, self.mathcontent.symbol_translate('mmultiscripts:pre-subscript')),
				item[0],
				'{0}{1}{2}'.format(self.mathcontent.symbol_translate('mmultiscripts:order'), count + 1, self.mathcontent.symbol_translate('mmultiscripts:pre-superscript')),
				item[1],
			]
			mmrule.extend(temp)

		index = range(1, self.mprescripts_index_in_child())
		index_odd = index[0::2]
		index_even = index[1::2]
		index_mix = zip(index_odd, index_even)
		for count, item in enumerate(index_mix):
			temp = [
				'{0}{1}{2}'.format(self.mathcontent.symbol_translate('mmultiscripts:order'), count + 1, self.mathcontent.symbol_translate('mmultiscripts:post-subscript')),
				item[0],
				'{0}{1}{2}'.format(self.mathcontent.symbol_translate('mmultiscripts:order'), count + 1, self.mathcontent.symbol_translate('mmultiscripts:post-superscript')),
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
		mmrole = [self.mathcontent.symbol_translate('main')]

		index = range(1, self.mprescripts_index_in_child())
		index_odd = index[0::2]
		index_even = index[1::2]
		index_mix = zip(index_odd, index_even)
		for count, item in enumerate(index_mix):
			temp = [
				'{0}{1}{2}'.format(self.mathcontent.symbol_translate('mmultiscripts:order'), count + 1, self.mathcontent.symbol_translate('mmultiscripts:post-subscript')),
				'{0}{1}{2}'.format(self.mathcontent.symbol_translate('mmultiscripts:order'), count + 1, self.mathcontent.symbol_translate('mmultiscripts:post-superscript')),
			]
			mmrole.extend(temp)

		mmrole.append(self.mathcontent.symbol_translate('mmultiscripts:mprescripts'))

		index = range(self.mprescripts_index_in_child() + 1, len(self.child))
		index_odd = index[0::2]
		index_even = index[1::2]
		index_mix = zip(index_odd, index_even)
		for count, item in enumerate(index_mix):
			temp = [
				'{0}{1}{2}'.format(self.mathcontent.symbol_translate('mmultiscripts:order'), count + 1, self.mathcontent.symbol_translate('mmultiscripts:pre-subscript')),
				'{0}{1}{2}'.format(self.mathcontent.symbol_translate('mmultiscripts:order'), count + 1, self.mathcontent.symbol_translate('mmultiscripts:pre-superscript')),
			]
			mmrole.extend(temp)

		self.role = mmrole

	def mprescripts_index_in_child(self):
		for c in self.child:
			if isinstance(c, Mprescripts):
				return self.child.index(c)
		return None


class Mprescripts(TerminalNode):
	pass


class Nones(TerminalNode):
	def set_rule(self):
		self.rule = [self.mathcontent.symbol_translate('none')]


class NodeType(object):
	tag = object
	child = ['object', '*']
	attrib = {}
	data = re.compile(r".*")
	name = 'nodetype'
	priority = 0

	def __init__(self):
		self.mathrule = {}
		self.rule = []
		self.role = []
		self.braillerule = []
		self.braillerole = []

	@classmethod
	def check(cls, obj):
		if not issubclass(obj.__class__, cls.tag):
			return False

		return True

	def set_mathrule(self, mathrule):
		self.mathrule = mathrule
		self.set_rule()

	def set_rule(self):
		try:
			self.rule = self.mathrule[self.name].serialized_order
		except BaseException:
			self.rule = None

	def set_braillemathrule(self, braillemathrule):
		self.braillemathrule = braillemathrule
		self.set_braillerule()

	def set_braillerule(self):
		try:
			self.braillerule = self.braillemathrule[self.name].serialized_order
		except BaseException:
			self.braillerule = None


class TerminalNodeType(NodeType):
	@classmethod
	def check(cls, obj):
		if not issubclass(obj.__class__, cls.tag):
			return False

		# check attrib
		for key, value in cls.attrib.items():
			if key not in obj.attrib:
				return False
			elif not value.search(obj.attrib[key]) is not None:
				return False

		# check data
		if not obj.data == '':
			try:
				if not cls.data.search(obj.data) is not None:
					return False
			except BaseException:
				return False
		return True


class NonTerminalNodeType(NodeType):
	@classmethod
	def check(cls, obj):
		if not issubclass(obj.__class__, cls.tag):
			return False

		# check attrib
		for key, value in cls.attrib.items():
			if key not in obj.attrib:
				return False
			elif not value.search(obj.attrib[key]) is not None:
				return False

		# check child
		if cls.child[-1] == '*' and len(cls.child) > 1:
			d = len(obj.child) - (len(cls.child) - 1)
			type_list = cls.child[:-1] + [cls.child[-2]] * d
		else:
			type_list = cls.child
		if not len(type_list) == len(obj.child):
			return False

		# change type
		type_list_str = [t if isinstance(t, str) else t.__name__ for t in type_list]
		type_list = [all_nodetypes_dict[t] for t in type_list_str]

		# check child type
		for mt, o in zip(type_list, obj.child):
			if not mt == object and not mt.check(o):
				return False

		return True


class SiblingNodeType(NodeType):
	previous_siblings = []
	next_siblings = []
	self_ = NodeType

	@classmethod
	def check(cls, obj):
		self_index = obj.index_in_parent()
		if self_index is None:
			return False

		cls_previous_siblings = cls.previous_siblings
		cls_next_siblings = cls.next_siblings

		cpsl = len(cls_previous_siblings)
		cnsl = len(cls_next_siblings)

		start_index = self_index - cpsl
		end_index = self_index + cnsl

		if cpsl > 0 and cls_previous_siblings[0] is None:
			cls_previous_siblings = cls_previous_siblings[1:]
			cpsl = len(cls_previous_siblings)
			start_index = self_index - cpsl
			if not start_index == 0:
				return False
		elif start_index < 0:
			return False

		if cnsl > 0 and cls_next_siblings[-1] is None:
			cls_next_siblings = cls_next_siblings[:-1]
			cnsl = len(cls_next_siblings)
			end_index = self_index + cnsl
			if not end_index == len(obj.parent.child) - 1:
				return False
		elif end_index >= len(obj.parent.child):
			return False

		# change type
		type_list = cls_previous_siblings + [cls.self_] + cls_next_siblings
		type_list_str = [t if isinstance(t, str) else t.__name__ for t in type_list]
		type_list = [all_nodetypes_dict[t] for t in type_list_str]
		objs = obj.parent.child[start_index:end_index + 1]
		for mt, o in zip(type_list, objs):
			if not mt == object and not mt.check(o):
				return False

		return True


class CompoundNodeType(NodeType):
	compound = []

	@classmethod
	def check(cls, obj):
		for mt in cls.compound:
			if mt.check(obj):
				return True
		return False


class FractionType(NonTerminalNodeType):
	tag = Mfrac


class MiOperandType(TerminalNodeType):
	tag = Mi
	data = re.compile(r"^[\d\w]+$")


class MnOperandType(TerminalNodeType):
	tag = Mn
	data = re.compile(r"^[\d\w]+$")


class OperandType(CompoundNodeType):
	compound = [MiOperandType, MnOperandType, FractionType, ]


class OperatorType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^[u'\u2200'-u'\u22FF']$")


class FromToOperatorType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^[∑∫]$")


class LogOperatorType(TerminalNodeType):
	tag = Mi
	data = re.compile(r"^log$")


class MiType(TerminalNodeType):
	tag = Mi


class MnType(TerminalNodeType):
	tag = Mn


class MoType(TerminalNodeType):
	tag = Mo


class MtableType(NonTerminalNodeType):
	tag = Mtable


class TwoMnType(TerminalNodeType):
	tag = Mn
	data = re.compile(r"^[2]$")


class ThreeMnType(TerminalNodeType):
	tag = Mn
	data = re.compile(r"^[3]$")


class TwoMiOperandItemType(NonTerminalNodeType):
	tag = Mrow
	child = [MiOperandType, MiOperandType]


class MoLineType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^[↔]$")


class LineType(NonTerminalNodeType):
	tag = Mover
	child = [TwoMiOperandItemType, MoLineType]
	name = 'LineType'


class MoLineSegmentType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^[¯―]$")


class LineSegmentType(NonTerminalNodeType):
	tag = Mover
	child = [TwoMiOperandItemType, MoLineSegmentType]
	name = 'LineSegmentType'


class MoVectorType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^[→]$")
	attrib = {
		'stretchy': re.compile(r"^false$"),
	}


class VectorSingleType(NonTerminalNodeType):
	tag = Mover
	child = [MiOperandType, MoVectorType]
	name = 'VectorSingleType'


class VectorDoubleType(NonTerminalNodeType):
	tag = Mover
	child = [TwoMiOperandItemType, MoVectorType]
	name = 'VectorDoubleType'


# Arrow above 2 symbols denotes Ray in English notation and vector in French notation
# (equivalent of VectorDoubleType).
# Arrow above 1 symbol denotes also vector in French notation.
class MoRayType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^[→]$")


# Arrow above 2 symbols denotes Ray in English notation and vector in French notation
# (equivalent of VectorDoubleType).
class RayType(NonTerminalNodeType):
	tag = Mover
	child = [TwoMiOperandItemType, MoRayType]
	name = 'RayType'


# Arrow above single symbol denotes vector in French notation.
class ArrowOverSingleSymbolType(NonTerminalNodeType):
	tag = Mover
	child = [MiOperandType, MoRayType]
	name = 'ArrowOverSingleSymbolType'


class MoFrownType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^[⌢]$")


class FrownType(NonTerminalNodeType):
	tag = Mover
	child = [TwoMiOperandItemType, MoFrownType]
	name = 'FrownType'


class MoDegreeType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^[°∘]$")


class DegreeType(NonTerminalNodeType):
	tag = Msup
	child = [NodeType, MoDegreeType, ]
	name = 'DegreeType'


class SingleType(CompoundNodeType):
	compound = [MiType, MnType, MoType]


class SingleMsubsupType(NonTerminalNodeType):
	tag = Msubsup
	child = [SingleType, SingleType, SingleType]
	name = 'SingleMsubsup'


class SingleMsubType(NonTerminalNodeType):
	tag = Msub
	child = [SingleType, SingleType]
	name = 'SingleMsub'


class SingleMsupType(NonTerminalNodeType):
	tag = Msup
	child = [SingleType, SingleType]
	name = 'SingleMsup'


class SingleMunderoverType(NonTerminalNodeType):
	tag = Munderover
	child = [SingleType, SingleType, SingleType]
	name = 'SingleMunderover'


class SingleMunderType(NonTerminalNodeType):
	tag = Munder
	child = [SingleType, SingleType]
	name = 'SingleMunder'


class SingleMoverType(NonTerminalNodeType):
	tag = Mover
	child = [SingleType, SingleType]
	name = 'SingleMover'


class SingleFractionType(FractionType):
	tag = Mfrac
	child = [OperandType, OperandType, ]
	name = 'single_fraction'


class SingleSqrtType(NonTerminalNodeType):
	tag = Msqrt
	child = [OperandType]
	name = 'single_square_root'


class PowerType(SingleMsupType):
	tag = Msup
	child = [OperandType, OperandType, ]
	name = 'power'


class SquarePowerType(PowerType):
	tag = Msup
	child = [OperandType, TwoMnType, ]
	name = 'SquarePowerType'


class CubePowerType(PowerType):
	tag = Msup
	child = [OperandType, ThreeMnType]
	name = 'CubePowerType'


class MsubsupFromToType(SingleMsubsupType):
	tag = Msubsup
	child = [FromToOperatorType, NodeType, NodeType]
	name = 'from_to'


class MunderoverFromToType(SingleMunderoverType):
	tag = Munderover
	child = [FromToOperatorType, NodeType, NodeType]
	name = 'from_to'


class MsubFromType(SingleMsubType):
	tag = Msub
	child = [FromToOperatorType, NodeType]
	name = 'from'


class MunderFromType(SingleMunderType):
	tag = Munder
	child = [FromToOperatorType, NodeType]
	name = 'from'


class MsupToType(SingleMsupType):
	tag = Msup
	child = [FromToOperatorType, NodeType]
	name = 'to'


class MoverToType(SingleMoverType):
	tag = Mover
	child = [FromToOperatorType, NodeType]
	name = 'to'


class MsubLogType(SingleMsubType):
	tag = Msub
	child = [LogOperatorType, OperandType]
	name = 'LogType'


class VerticalBarType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^\|$")


class AbsoluteType(SiblingNodeType):
	previous_siblings = [VerticalBarType]
	self_ = MnOperandType
	next_siblings = [VerticalBarType]
	name = 'absolute'


class OpenMatrixType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^\[$")


class CloseMatrixType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^\]$")


class MatrixType(SiblingNodeType):
	previous_siblings = [OpenMatrixType]
	self_ = MtableType
	next_siblings = [CloseMatrixType]
	name = 'matrix'


class OpenSimultaneousEquationsType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^\{$")


class SimultaneousEquationsType(SiblingNodeType):
	previous_siblings = [OpenSimultaneousEquationsType]
	self_ = MtableType
	name = 'SimultaneousEquations'
	priority = 0

	def set_rule(self):
		super().set_rule()
		rule = self.rule

		row_count = len(self.child)

		table_head = [rule[0] + f'{self.mathcontent.symbol_translate("has")} {row_count} {self.mathcontent.symbol_translate("row")}']
		cell = rule[1:-1]
		table_tail = rule[-1:]
		self.rule = table_head + cell + table_tail


class DeterminantType(SiblingNodeType):
	tag = Mtable
	previous_siblings = [VerticalBarType]
	self_ = MtableType
	next_siblings = [VerticalBarType]
	name = 'determinant'
	priority = 1


class BinomialType(FractionType):
	tag = Mfrac
	attrib = {
		'linethickness': re.compile(r"^[0]$"),
	}
	name = 'BinomialType'
	priority = 1


# SiblingNodeType
class SingleNumberFractionType(SingleFractionType):
	child = [MnOperandType, MnOperandType]
	name = ''


class AddIntegerFractionType(SiblingNodeType):
	previous_siblings = [MnOperandType]
	self_ = SingleNumberFractionType
	name = 'AddIntegerFractionType'
	priority = 1


class SignPreviousMoType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^[(*+-\./:<=>±·×÷−∔]$")


class MinusType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^[-−]$")


class NegativeSignType(SiblingNodeType):
	previous_siblings = [SignPreviousMoType]
	self_ = MinusType
	name = 'NegativeSignType'


class FirstNegativeSignType(SiblingNodeType):
	previous_siblings = [None]
	self_ = MinusType
	name = 'NegativeSignType'


class PlusType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^[+∔]$")


class PositiveSignType(SiblingNodeType):
	previous_siblings = [SignPreviousMoType]
	self_ = PlusType
	name = 'PositiveSignType'


class FirstPositiveSignType(SiblingNodeType):
	previous_siblings = [None]
	self_ = PlusType
	name = 'PositiveSignType'
