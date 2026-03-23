import re

AUTO_GENERATE = 0
DIC_GENERATE = 1


class Node(object):
	pass


class NonTerminalNode(Node):
	pass


class TerminalNode(Node):
	pass


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
	pass


class Mfenced(AlterNode):
	pass


class Menclose(AlterNode):
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
	pass


class Mlabeledtr(AlterNode):
	pass


class Mtr(AlterNode):
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


class Math(AlterNode):
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
	pass


class Ms(TerminalNode):
	pass


class Mmultiscripts(AlterNode):
	pass


class Mprescripts(TerminalNode):
	pass


class Nones(TerminalNode):
	pass


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
