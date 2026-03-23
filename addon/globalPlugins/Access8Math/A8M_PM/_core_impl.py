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
	pass


class TerminalNodeType(NodeType):
	pass


class NonTerminalNodeType(NodeType):
	pass


class SiblingNodeType(NodeType):
	pass


class CompoundNodeType(NodeType):
	pass


class FractionType(NonTerminalNodeType):
	pass


class MiOperandType(TerminalNodeType):
	pass


class MnOperandType(TerminalNodeType):
	pass


class OperandType(CompoundNodeType):
	pass


class OperatorType(TerminalNodeType):
	pass


class FromToOperatorType(TerminalNodeType):
	pass


class LogOperatorType(TerminalNodeType):
	pass


class MiType(TerminalNodeType):
	pass


class MnType(TerminalNodeType):
	pass


class MoType(TerminalNodeType):
	pass


class MtableType(NonTerminalNodeType):
	pass


class TwoMnType(TerminalNodeType):
	pass


class ThreeMnType(TerminalNodeType):
	pass


class TwoMiOperandItemType(NonTerminalNodeType):
	pass


class MoLineType(TerminalNodeType):
	pass


class LineType(NonTerminalNodeType):
	pass


class MoLineSegmentType(TerminalNodeType):
	pass


class LineSegmentType(NonTerminalNodeType):
	pass


class MoVectorType(TerminalNodeType):
	pass


class VectorSingleType(NonTerminalNodeType):
	pass


class VectorDoubleType(NonTerminalNodeType):
	pass


class MoRayType(TerminalNodeType):
	pass


class RayType(NonTerminalNodeType):
	pass


class ArrowOverSingleSymbolType(NonTerminalNodeType):
	pass


class MoFrownType(TerminalNodeType):
	pass


class FrownType(NonTerminalNodeType):
	pass


class MoDegreeType(TerminalNodeType):
	pass


class DegreeType(NonTerminalNodeType):
	pass


class SingleType(CompoundNodeType):
	pass


class SingleMsubsupType(NonTerminalNodeType):
	pass


class SingleMsubType(NonTerminalNodeType):
	pass


class SingleMsupType(NonTerminalNodeType):
	pass


class SingleMunderoverType(NonTerminalNodeType):
	pass


class SingleMunderType(NonTerminalNodeType):
	pass


class SingleMoverType(NonTerminalNodeType):
	pass


class SingleFractionType(FractionType):
	pass


class SingleSqrtType(NonTerminalNodeType):
	pass


class PowerType(SingleMsupType):
	pass


class SquarePowerType(PowerType):
	pass


class CubePowerType(PowerType):
	pass


class MsubsupFromToType(SingleMsubsupType):
	pass


class MunderoverFromToType(SingleMunderoverType):
	pass


class MsubFromType(SingleMsubType):
	pass


class MunderFromType(SingleMunderType):
	pass


class MsupToType(SingleMsupType):
	pass


class MoverToType(SingleMoverType):
	pass


class MsubLogType(SingleMsubType):
	pass


class VerticalBarType(TerminalNodeType):
	pass


class AbsoluteType(SiblingNodeType):
	pass


class OpenMatrixType(TerminalNodeType):
	pass


class CloseMatrixType(TerminalNodeType):
	pass


class MatrixType(SiblingNodeType):
	pass


class OpenSimultaneousEquationsType(TerminalNodeType):
	pass


class SimultaneousEquationsType(SiblingNodeType):
	pass


class DeterminantType(SiblingNodeType):
	pass


class BinomialType(FractionType):
	pass


class SingleNumberFractionType(SingleFractionType):
	pass


class AddIntegerFractionType(SiblingNodeType):
	pass


class SignPreviousMoType(TerminalNodeType):
	pass


class MinusType(TerminalNodeType):
	pass


class NegativeSignType(SiblingNodeType):
	pass


class FirstNegativeSignType(SiblingNodeType):
	pass


class PlusType(TerminalNodeType):
	pass


class PositiveSignType(SiblingNodeType):
	pass


class FirstPositiveSignType(SiblingNodeType):
	pass
