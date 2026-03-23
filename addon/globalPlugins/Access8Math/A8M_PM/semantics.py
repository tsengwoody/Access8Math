import copy
import re

from . import _core_impl as _core
from .metadata import mathrule_info
from . import nodes as _nodes
from .rules import MathRule


_TYPE_CREATION_ORDER = [
	"NodeType",
	"TerminalNodeType",
	"NonTerminalNodeType",
	"SiblingNodeType",
	"CompoundNodeType",
	"FractionType",
	"MiOperandType",
	"MnOperandType",
	"OperandType",
	"OperatorType",
	"FromToOperatorType",
	"LogOperatorType",
	"MiType",
	"MnType",
	"MoType",
	"MtableType",
	"TwoMnType",
	"ThreeMnType",
	"TwoMiOperandItemType",
	"MoLineType",
	"LineType",
	"MoLineSegmentType",
	"LineSegmentType",
	"MoVectorType",
	"VectorSingleType",
	"VectorDoubleType",
	"MoRayType",
	"RayType",
	"ArrowOverSingleSymbolType",
	"MoFrownType",
	"FrownType",
	"MoDegreeType",
	"DegreeType",
	"SingleType",
	"SingleMsubsupType",
	"SingleMsubType",
	"SingleMsupType",
	"SingleMunderoverType",
	"SingleMunderType",
	"SingleMoverType",
	"SingleFractionType",
	"SingleSqrtType",
	"PowerType",
	"SquarePowerType",
	"CubePowerType",
	"MsubsupFromToType",
	"MunderoverFromToType",
	"MsubFromType",
	"MunderFromType",
	"MsupToType",
	"MoverToType",
	"MsubLogType",
	"VerticalBarType",
	"AbsoluteType",
	"OpenMatrixType",
	"CloseMatrixType",
	"MatrixType",
	"OpenSimultaneousEquationsType",
	"SimultaneousEquationsType",
	"DeterminantType",
	"BinomialType",
	"SingleNumberFractionType",
	"AddIntegerFractionType",
	"SignPreviousMoType",
	"MinusType",
	"NegativeSignType",
	"FirstNegativeSignType",
	"PlusType",
	"PositiveSignType",
	"FirstPositiveSignType",
]

_TYPE_PARENT_NAMES = {
	"NodeType": None,
	"TerminalNodeType": "NodeType",
	"NonTerminalNodeType": "NodeType",
	"SiblingNodeType": "NodeType",
	"CompoundNodeType": "NodeType",
	"FractionType": "NonTerminalNodeType",
	"MiOperandType": "TerminalNodeType",
	"MnOperandType": "TerminalNodeType",
	"OperandType": "CompoundNodeType",
	"OperatorType": "TerminalNodeType",
	"FromToOperatorType": "TerminalNodeType",
	"LogOperatorType": "TerminalNodeType",
	"MiType": "TerminalNodeType",
	"MnType": "TerminalNodeType",
	"MoType": "TerminalNodeType",
	"MtableType": "NonTerminalNodeType",
	"TwoMnType": "TerminalNodeType",
	"ThreeMnType": "TerminalNodeType",
	"TwoMiOperandItemType": "NonTerminalNodeType",
	"MoLineType": "TerminalNodeType",
	"LineType": "NonTerminalNodeType",
	"MoLineSegmentType": "TerminalNodeType",
	"LineSegmentType": "NonTerminalNodeType",
	"MoVectorType": "TerminalNodeType",
	"VectorSingleType": "NonTerminalNodeType",
	"VectorDoubleType": "NonTerminalNodeType",
	"MoRayType": "TerminalNodeType",
	"RayType": "NonTerminalNodeType",
	"ArrowOverSingleSymbolType": "NonTerminalNodeType",
	"MoFrownType": "TerminalNodeType",
	"FrownType": "NonTerminalNodeType",
	"MoDegreeType": "TerminalNodeType",
	"DegreeType": "NonTerminalNodeType",
	"SingleType": "CompoundNodeType",
	"SingleMsubsupType": "NonTerminalNodeType",
	"SingleMsubType": "NonTerminalNodeType",
	"SingleMsupType": "NonTerminalNodeType",
	"SingleMunderoverType": "NonTerminalNodeType",
	"SingleMunderType": "NonTerminalNodeType",
	"SingleMoverType": "NonTerminalNodeType",
	"SingleFractionType": "FractionType",
	"SingleSqrtType": "NonTerminalNodeType",
	"PowerType": "SingleMsupType",
	"SquarePowerType": "PowerType",
	"CubePowerType": "PowerType",
	"MsubsupFromToType": "SingleMsubsupType",
	"MunderoverFromToType": "SingleMunderoverType",
	"MsubFromType": "SingleMsubType",
	"MunderFromType": "SingleMunderType",
	"MsupToType": "SingleMsupType",
	"MoverToType": "SingleMoverType",
	"MsubLogType": "SingleMsubType",
	"VerticalBarType": "TerminalNodeType",
	"AbsoluteType": "SiblingNodeType",
	"OpenMatrixType": "TerminalNodeType",
	"CloseMatrixType": "TerminalNodeType",
	"MatrixType": "SiblingNodeType",
	"OpenSimultaneousEquationsType": "TerminalNodeType",
	"SimultaneousEquationsType": "SiblingNodeType",
	"DeterminantType": "SiblingNodeType",
	"BinomialType": "FractionType",
	"SingleNumberFractionType": "SingleFractionType",
	"AddIntegerFractionType": "SiblingNodeType",
	"SignPreviousMoType": "TerminalNodeType",
	"MinusType": "TerminalNodeType",
	"NegativeSignType": "SiblingNodeType",
	"FirstNegativeSignType": "SiblingNodeType",
	"PlusType": "TerminalNodeType",
	"PositiveSignType": "SiblingNodeType",
	"FirstPositiveSignType": "SiblingNodeType",
}

_REGISTERED_NODETYPE_NAMES = list(_TYPE_CREATION_ORDER)
_NODETYPE_CLASS_ATTRS = (
	"tag",
	"child",
	"attrib",
	"data",
	"name",
	"priority",
	"previous_siblings",
	"next_siblings",
	"self_",
	"compound",
)


class NodeType(object):
	tag = object
	child = ["object", "*"]
	attrib = {}
	data = re.compile(r".*")
	name = "nodetype"
	priority = 0

	def __init__(self):
		self.mathrule = {}
		self.rule = []
		self.role = []
		self.braillerule = []
		self.braillerole = []

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
	pass


class NonTerminalNodeType(NodeType):
	pass


class SiblingNodeType(NodeType):
	previous_siblings = []
	next_siblings = []
	self_ = NodeType


class CompoundNodeType(NodeType):
	compound = []


class MtableType(NonTerminalNodeType):
	tag = _nodes.Mtable


class TwoMiOperandItemType(NonTerminalNodeType):
	tag = _nodes.Mrow
	child = ["MiOperandType", "MiOperandType"]


class MoLineType(TerminalNodeType):
	tag = _nodes.Mo
	data = re.compile(r"^[↔]$")


class LineType(NonTerminalNodeType):
	tag = _nodes.Mover
	child = [TwoMiOperandItemType, MoLineType]
	name = "LineType"


class MoLineSegmentType(TerminalNodeType):
	tag = _nodes.Mo
	data = re.compile(r"^[¯―]$")


class LineSegmentType(NonTerminalNodeType):
	tag = _nodes.Mover
	child = [TwoMiOperandItemType, MoLineSegmentType]
	name = "LineSegmentType"


class MoVectorType(TerminalNodeType):
	tag = _nodes.Mo
	data = re.compile(r"^[→]$")
	attrib = {
		"stretchy": re.compile(r"^false$"),
	}


class VectorSingleType(NonTerminalNodeType):
	tag = _nodes.Mover
	child = ["MiOperandType", MoVectorType]
	name = "VectorSingleType"


class VectorDoubleType(NonTerminalNodeType):
	tag = _nodes.Mover
	child = [TwoMiOperandItemType, MoVectorType]
	name = "VectorDoubleType"


class MoRayType(TerminalNodeType):
	tag = _nodes.Mo
	data = re.compile(r"^[→]$")


class RayType(NonTerminalNodeType):
	tag = _nodes.Mover
	child = [TwoMiOperandItemType, MoRayType]
	name = "RayType"


class MoDegreeType(TerminalNodeType):
	tag = _nodes.Mo
	data = re.compile(r"^[°∘]$")


class DegreeType(NonTerminalNodeType):
	tag = _nodes.Msup
	child = [NodeType, MoDegreeType]
	name = "DegreeType"


class OpenMatrixType(TerminalNodeType):
	tag = _nodes.Mo
	data = re.compile(r"^\[$")


class CloseMatrixType(TerminalNodeType):
	tag = _nodes.Mo
	data = re.compile(r"^\]$")


class MatrixType(SiblingNodeType):
	previous_siblings = [OpenMatrixType]
	self_ = MtableType
	next_siblings = [CloseMatrixType]
	name = "matrix"


class VerticalBarType(TerminalNodeType):
	tag = _nodes.Mo
	data = re.compile(r"^\|$")


class OpenSimultaneousEquationsType(TerminalNodeType):
	tag = _nodes.Mo
	data = re.compile(r"^\{$")


class SimultaneousEquationsType(SiblingNodeType):
	previous_siblings = [OpenSimultaneousEquationsType]
	self_ = MtableType
	name = "SimultaneousEquations"
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
	tag = _nodes.Mtable
	previous_siblings = [VerticalBarType]
	self_ = MtableType
	next_siblings = [VerticalBarType]
	name = "determinant"
	priority = 1


class FractionType(NonTerminalNodeType):
	tag = _nodes.Mfrac


class MiOperandType(TerminalNodeType):
	tag = _nodes.Mi
	data = re.compile(r"^[\d\w]+$")


class MnOperandType(TerminalNodeType):
	tag = _nodes.Mn
	data = re.compile(r"^[\d\w]+$")


class OperandType(CompoundNodeType):
	compound = [MiOperandType, MnOperandType, FractionType]


class OperatorType(TerminalNodeType):
	tag = _nodes.Mo
	data = re.compile(r"^[u'\u2200'-u'\u22FF']$")


class FromToOperatorType(TerminalNodeType):
	tag = _nodes.Mo
	data = re.compile(r"^[∑∫]$")


class LogOperatorType(TerminalNodeType):
	tag = _nodes.Mi
	data = re.compile(r"^log$")


class MiType(TerminalNodeType):
	tag = _nodes.Mi


class MnType(TerminalNodeType):
	tag = _nodes.Mn


class MoType(TerminalNodeType):
	tag = _nodes.Mo


class TwoMnType(TerminalNodeType):
	tag = _nodes.Mn
	data = re.compile(r"^[2]$")


class ThreeMnType(TerminalNodeType):
	tag = _nodes.Mn
	data = re.compile(r"^[3]$")


class ArrowOverSingleSymbolType(NonTerminalNodeType):
	tag = _nodes.Mover
	child = [MiOperandType, MoRayType]
	name = "ArrowOverSingleSymbolType"


class MoFrownType(TerminalNodeType):
	tag = _nodes.Mo
	data = re.compile(r"^[⌢]$")


class FrownType(NonTerminalNodeType):
	tag = _nodes.Mover
	child = [TwoMiOperandItemType, MoFrownType]
	name = "FrownType"


class SingleType(CompoundNodeType):
	compound = [MiType, MnType, MoType]


class SingleMsubsupType(NonTerminalNodeType):
	tag = _nodes.Msubsup
	child = [SingleType, SingleType, SingleType]
	name = "SingleMsubsup"


class SingleMsubType(NonTerminalNodeType):
	tag = _nodes.Msub
	child = [SingleType, SingleType]
	name = "SingleMsub"


class SingleMsupType(NonTerminalNodeType):
	tag = _nodes.Msup
	child = [SingleType, SingleType]
	name = "SingleMsup"


class SingleMunderoverType(NonTerminalNodeType):
	tag = _nodes.Munderover
	child = [SingleType, SingleType, SingleType]
	name = "SingleMunderover"


class SingleMunderType(NonTerminalNodeType):
	tag = _nodes.Munder
	child = [SingleType, SingleType]
	name = "SingleMunder"


class SingleMoverType(NonTerminalNodeType):
	tag = _nodes.Mover
	child = [SingleType, SingleType]
	name = "SingleMover"


class SingleFractionType(FractionType):
	tag = _nodes.Mfrac
	child = [OperandType, OperandType]
	name = "single_fraction"


class SingleSqrtType(NonTerminalNodeType):
	tag = _nodes.Msqrt
	child = [OperandType]
	name = "single_square_root"


class PowerType(SingleMsupType):
	tag = _nodes.Msup
	child = [OperandType, OperandType]
	name = "power"


class SquarePowerType(PowerType):
	tag = _nodes.Msup
	child = [OperandType, TwoMnType]
	name = "SquarePowerType"


class CubePowerType(PowerType):
	tag = _nodes.Msup
	child = [OperandType, ThreeMnType]
	name = "CubePowerType"


class MsubLogType(SingleMsubType):
	tag = _nodes.Msub
	child = [LogOperatorType, OperandType]
	name = "LogType"


class AbsoluteType(SiblingNodeType):
	previous_siblings = [VerticalBarType]
	self_ = MnOperandType
	next_siblings = [VerticalBarType]
	name = "absolute"


class BinomialType(FractionType):
	tag = _nodes.Mfrac
	attrib = {
		"linethickness": re.compile(r"^[0]$"),
	}
	name = "BinomialType"
	priority = 1


class SingleNumberFractionType(SingleFractionType):
	child = [MnOperandType, MnOperandType]
	name = ""


class AddIntegerFractionType(SiblingNodeType):
	previous_siblings = [MnOperandType]
	self_ = SingleNumberFractionType
	name = "AddIntegerFractionType"
	priority = 1


for _name in _TYPE_CREATION_ORDER:
	if _name in {
		"NodeType",
		"TerminalNodeType",
		"NonTerminalNodeType",
		"SiblingNodeType",
		"CompoundNodeType",
		"MtableType",
		"TwoMiOperandItemType",
		"MoLineType",
		"LineType",
		"MoLineSegmentType",
		"LineSegmentType",
		"MoVectorType",
		"VectorSingleType",
		"VectorDoubleType",
		"MoRayType",
		"RayType",
		"MoDegreeType",
		"DegreeType",
		"MsubsupFromToType",
		"MunderoverFromToType",
		"MsubFromType",
		"MunderFromType",
		"MsupToType",
		"MoverToType",
		"SignPreviousMoType",
		"MinusType",
		"NegativeSignType",
		"FirstNegativeSignType",
		"PlusType",
		"PositiveSignType",
		"FirstPositiveSignType",
		"OpenMatrixType",
		"CloseMatrixType",
		"MatrixType",
		"VerticalBarType",
		"OpenSimultaneousEquationsType",
		"SimultaneousEquationsType",
		"DeterminantType",
		"FractionType",
		"MiOperandType",
		"MnOperandType",
		"OperandType",
		"OperatorType",
		"FromToOperatorType",
		"LogOperatorType",
		"MiType",
		"MnType",
		"MoType",
		"TwoMnType",
		"ThreeMnType",
		"ArrowOverSingleSymbolType",
		"MoFrownType",
		"FrownType",
		"SingleType",
		"SingleMsubsupType",
		"SingleMsubType",
		"SingleMsupType",
		"SingleMunderoverType",
		"SingleMunderType",
		"SingleMoverType",
		"SingleFractionType",
		"SingleSqrtType",
		"PowerType",
		"SquarePowerType",
		"CubePowerType",
		"MsubLogType",
		"AbsoluteType",
		"BinomialType",
		"SingleNumberFractionType",
		"AddIntegerFractionType",
	}:
		continue
	legacy_class = getattr(_core, _name)
	parent_name = _TYPE_PARENT_NAMES[_name]
	bases = (globals()[parent_name], legacy_class)
	attrs = {}
	for attr_name in _NODETYPE_CLASS_ATTRS:
		if attr_name in legacy_class.__dict__:
			attrs[attr_name] = copy.deepcopy(legacy_class.__dict__[attr_name])
	globals()[_name] = type(_name, bases, attrs)


class MsubsupFromToType(SingleMsubsupType):
	tag = _nodes.Msubsup
	child = ["FromToOperatorType", NodeType, NodeType]
	name = "from_to"


class MunderoverFromToType(SingleMunderoverType):
	tag = _nodes.Munderover
	child = ["FromToOperatorType", NodeType, NodeType]
	name = "from_to"


class MsubFromType(SingleMsubType):
	tag = _nodes.Msub
	child = ["FromToOperatorType", NodeType]
	name = "from"


class MunderFromType(SingleMunderType):
	tag = _nodes.Munder
	child = ["FromToOperatorType", NodeType]
	name = "from"


class MsupToType(SingleMsupType):
	tag = _nodes.Msup
	child = ["FromToOperatorType", NodeType]
	name = "to"


class MoverToType(SingleMoverType):
	tag = _nodes.Mover
	child = ["FromToOperatorType", NodeType]
	name = "to"


class SignPreviousMoType(TerminalNodeType):
	tag = _nodes.Mo
	data = re.compile(r"^[(*+-\./:<=>±·×÷−∔]$")


class MinusType(TerminalNodeType):
	tag = _nodes.Mo
	data = re.compile(r"^[-−]$")


class NegativeSignType(SiblingNodeType):
	previous_siblings = [SignPreviousMoType]
	self_ = MinusType
	name = "NegativeSignType"


class FirstNegativeSignType(SiblingNodeType):
	previous_siblings = [None]
	self_ = MinusType
	name = "NegativeSignType"


class PlusType(TerminalNodeType):
	tag = _nodes.Mo
	data = re.compile(r"^[+∔]$")


class PositiveSignType(SiblingNodeType):
	previous_siblings = [SignPreviousMoType]
	self_ = PlusType
	name = "PositiveSignType"


class FirstPositiveSignType(SiblingNodeType):
	previous_siblings = [None]
	self_ = PlusType
	name = "PositiveSignType"


def ComplementMethod(method):
	def decorator(cls, obj):
		return not method(obj)

	return decorator


def _resolve_reference(value):
	if value in {None, object, "*"}:
		return value
	name = getattr(value, "__name__", None)
	if not name:
		return value
	if hasattr(_nodes, name):
		return getattr(_nodes, name)
	if name in globals():
		return globals()[name]
	return value


def _remap_sequence(values):
	return [_resolve_reference(value) for value in values]


def _nodetype_check(cls, obj):
	if not issubclass(obj.__class__, cls.tag):
		return False
	return True


def _terminal_nodetype_check(cls, obj):
	if not issubclass(obj.__class__, cls.tag):
		return False
	for key, value in cls.attrib.items():
		if key not in obj.attrib:
			return False
		elif value.search(obj.attrib[key]) is None:
			return False
	if obj.data != "":
		try:
			if cls.data.search(obj.data) is None:
				return False
		except BaseException:
			return False
	return True


def _nonterminal_nodetype_check(cls, obj):
	if not issubclass(obj.__class__, cls.tag):
		return False
	for key, value in cls.attrib.items():
		if key not in obj.attrib:
			return False
		elif value.search(obj.attrib[key]) is None:
			return False
	if cls.child[-1] == "*" and len(cls.child) > 1:
		d = len(obj.child) - (len(cls.child) - 1)
		type_list = cls.child[:-1] + [cls.child[-2]] * d
	else:
		type_list = cls.child
	if len(type_list) != len(obj.child):
		return False
	type_list_names = [item if isinstance(item, str) else item.__name__ for item in type_list]
	type_list = [all_nodetypes_dict[name] for name in type_list_names]
	for nodetype, child in zip(type_list, obj.child):
		if nodetype is not object and not nodetype.check(child):
			return False
	return True


def _sibling_nodetype_check(cls, obj):
	self_index = obj.index_in_parent()
	if self_index is None:
		return False
	previous_siblings = cls.previous_siblings
	next_siblings = cls.next_siblings
	previous_count = len(previous_siblings)
	next_count = len(next_siblings)
	start_index = self_index - previous_count
	end_index = self_index + next_count
	if previous_count > 0 and previous_siblings[0] is None:
		previous_siblings = previous_siblings[1:]
		previous_count = len(previous_siblings)
		start_index = self_index - previous_count
		if start_index != 0:
			return False
	elif start_index < 0:
		return False
	if next_count > 0 and next_siblings[-1] is None:
		next_siblings = next_siblings[:-1]
		next_count = len(next_siblings)
		end_index = self_index + next_count
		if end_index != len(obj.parent.child) - 1:
			return False
	elif end_index >= len(obj.parent.child):
		return False
	type_list = previous_siblings + [cls.self_] + next_siblings
	type_list_names = [item if isinstance(item, str) else item.__name__ for item in type_list]
	type_list = [all_nodetypes_dict[name] for name in type_list_names]
	for nodetype, sibling in zip(type_list, obj.parent.child[start_index:end_index + 1]):
		if nodetype is not object and not nodetype.check(sibling):
			return False
	return True


def _compound_nodetype_check(cls, obj):
	for nodetype in cls.compound:
		if nodetype.check(obj):
			return True
	return False


nodetypes = [globals()[name] for name in _REGISTERED_NODETYPE_NAMES]
nodetypes = sorted(nodetypes, key=lambda cls: -cls.priority)
nodetypes_dict = {name: globals()[name] for name in _REGISTERED_NODETYPE_NAMES}

NodeType.check = classmethod(_nodetype_check)
TerminalNodeType.check = classmethod(_terminal_nodetype_check)
NonTerminalNodeType.check = classmethod(_nonterminal_nodetype_check)
SiblingNodeType.check = classmethod(_sibling_nodetype_check)
CompoundNodeType.check = classmethod(_compound_nodetype_check)

for nodetype in nodetypes:
	for attr_name in ("tag", "self_"):
		if hasattr(nodetype, attr_name):
			setattr(nodetype, attr_name, _resolve_reference(getattr(nodetype, attr_name)))
	for attr_name in ("child", "previous_siblings", "next_siblings", "compound"):
		if hasattr(nodetype, attr_name):
			setattr(nodetype, attr_name, _remap_sequence(getattr(nodetype, attr_name)))

notnodetypes = []
notnodetypes_dict = {}
for nodetype in nodetypes:
	dic = dict(nodetype.__dict__)
	dic.update({
		"check": classmethod(ComplementMethod(nodetype.check)),
		"name": "",
	})
	notnodetype = type(f"Not{nodetype.__name__}", nodetype.__bases__, dic)
	globals()[notnodetype.__name__] = notnodetype
	notnodetypes.append(notnodetype)
	notnodetypes_dict[notnodetype.__name__] = notnodetype

all_nodetypes = [*nodetypes, *notnodetypes]
all_nodetypes_dict = {cls.__name__: cls for cls in all_nodetypes}
all_nodetypes_dict["object"] = object

nodetypes_check = []


def initialize(Access8MathConfig):
	nodetypes_check.clear()
	if Access8MathConfig and Access8MathConfig["settings"]["analyze_math_meaning"]:
		for nodetype in nodetypes:
			if nodetype.__name__ in Access8MathConfig["rules"]:
				if Access8MathConfig["rules"][nodetype.__name__]:
					nodetypes_check.append(nodetype)
			else:
				nodetypes_check.append(nodetype)


def mathrule_validate(mathrule, validator):
	result = True
	if not len(mathrule.serialized_order) == validator[0]:
		result = False
	if not len(mathrule.role) == validator[1]:
		result = False
	if validator[2] == ".":
		for index in range(len(mathrule.serialized_order)):
			if index % 2 == 0:
				if not isinstance(mathrule.serialized_order[index], str):
					result = False
			else:
				if not isinstance(mathrule.serialized_order[index], int):
					result = False
	elif validator[2] == "*":
		if not isinstance(mathrule.serialized_order[0], str):
			result = False
		elif not isinstance(mathrule.serialized_order[1], tuple):
			result = False
		elif not isinstance(mathrule.serialized_order[2], str):
			result = False
	return result


__all__ = [
	"MathRule",
	"ComplementMethod",
	"initialize",
	"mathrule_validate",
	"nodetypes",
	"nodetypes_dict",
	"notnodetypes",
	"notnodetypes_dict",
	"all_nodetypes",
	"all_nodetypes_dict",
	"nodetypes_check",
	"mathrule_info",
	*_TYPE_CREATION_ORDER,
]
