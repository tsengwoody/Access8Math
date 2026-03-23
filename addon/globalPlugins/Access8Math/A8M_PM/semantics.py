import copy

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


for _name in _TYPE_CREATION_ORDER:
	legacy_class = getattr(_core, _name)
	parent_name = _TYPE_PARENT_NAMES[_name]
	if parent_name is None:
		bases = (legacy_class,)
	else:
		bases = (globals()[parent_name], legacy_class)
	attrs = {}
	for attr_name in _NODETYPE_CLASS_ATTRS:
		if attr_name in legacy_class.__dict__:
			attrs[attr_name] = copy.deepcopy(legacy_class.__dict__[attr_name])
	globals()[_name] = type(_name, bases, attrs)


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
