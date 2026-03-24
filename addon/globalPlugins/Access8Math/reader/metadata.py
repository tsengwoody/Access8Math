AUTO_GENERATE = 0
DIC_GENERATE = 1


mathrule_info = {
	"generics": {
		"node": [3, 1, "*"],
		"math": [3, 1, "*"],
	},
	"fraction": {
		"mfrac": [5, 2, "."],
		"single_fraction": [5, 2, "."],
		"AddIntegerFractionType": [5, 2, "."],
		"BinomialType": [5, 2, "."],
	},
	"root": {
		"msqrt": [3, 1, "*"],
		"mroot": [5, 2, "."],
		"single_square_root": [3, 1, "."],
	},
	"position": {
		"msubsup": [7, 3, "."],
		"msup": [5, 2, "."],
		"msub": [5, 2, "."],
		"munderover": [7, 3, "."],
		"munder": [5, 2, "."],
		"mover": [5, 2, "."],
		"SingleMsubsup": [7, 3, "."],
		"SingleMsub": [5, 2, "."],
		"SingleMsup": [5, 2, "."],
		"SingleMunderover": [7, 3, "."],
		"SingleMunder": [5, 2, "."],
		"SingleMover": [5, 2, "."],
	},
	"power": {
		"power": [5, 2, "."],
		"SquarePowerType": [3, 2, "."],
		"CubePowerType": [3, 2, "."],
	},
	"from to": {
		"from_to": [7, 3, "."],
		"from": [5, 2, "."],
		"to": [5, 2, "."],
		"LogType": [3, 2, "."],
	},
	"table": {
		"mtable": [3, 1, "*"],
		"mtr": [3, 1, "*"],
		"mtd": [3, 1, "*"],
		"determinant": [3, 1, "*"],
		"matrix": [3, 1, "*"],
		"SimultaneousEquations": [3, 1, "*"],
	},
	"line": {
		"LineType": [3, 2, "."],
		"RayType": [3, 2, "."],
		"LineSegmentType": [3, 2, "."],
		"VectorSingleType": [3, 2, "."],
		"VectorDoubleType": [3, 2, "."],
		"ArrowOverSingleSymbolType": [3, 2, "."],
		"FrownType": [3, 2, "."],
		"DegreeType": [3, 2, "."],
	},
	"other": {
		"NegativeSignType": [1, 1, "."],
		"PositiveSignType": [1, 1, "."],
		"mmultiscripts": [0, 0, "."],
		"menclose": [3, 1, "*"],
		"mfenced": [3, 1, "*"],
	},
}
