import config

LaTeX = {
	"latex": {
		"start": r"\l",
		"end": r"\l",
		"type": "latex",
	},
	"bracket": {
		"start": r"\(",
		"end": r"\)",
		"type": "latex",
	},
	"dollar": {
		"start": "$",
		"end": "$",
		"type": "latex",
	},
}

AsciiMath = {
	"asciimath": {
		"start": r"\a",
		"end": r"\a",
		"type": "asciimath",
	},
	"graveaccent": {
		"start": "`",
		"end": "`",
		"type": "asciimath",
	},
}

delimiter = {"latex": config.conf["Access8Math"]["settings"]["LaTeX_delimiter"], "asciimath": "graveaccent"}
