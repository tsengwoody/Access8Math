import config

_configSpec = u"""[settings]
provider = string(default=Access8Math)
language = string(default=en)
item_interval_time = integer(default=50,min=0,max=100)
interaction_frame_show = boolean(default=false)
analyze_math_meaning = boolean(default=true)
auto_generate = boolean(default=false)
dictionary_generate = boolean(default=true)
no_move_beep = boolean(default=true)
edit_NVDA_gesture = boolean(default=false)
HTML_display = string(default=block)
LaTeX_delimiter = string(default=bracket)

[rules]
SingleMsubsupType = boolean(default=true)
SingleMsubType = boolean(default=true)
SingleMsupType = boolean(default=true)
SingleMunderoverType = boolean(default=true)
SingleMunderType = boolean(default=true)
SingleMoverType = boolean(default=true)
SingleFractionType = boolean(default=true)
SingleSqrtType = boolean(default=true)
PowerType = boolean(default=true)
SquarePowerType = boolean(default=true)
CubePowerType = boolean(default=true)
SetType = boolean(default=true)
AbsoluteType = boolean(default=true)
MatrixType = boolean(default=true)
DeterminantType = boolean(default=true)
AddIntegerFractionType = boolean(default=true)
"""

config.conf.spec["Access8Math"] = {
	"settings": {
		"provider": "string(default=Access8Math)",
		"language": "string(default=en)",
		"item_interval_time": "integer(default=50,min=0,max=100)",
		"interaction_frame_show": "boolean(default=false)",
		"analyze_math_meaning": "boolean(default=true)",
		"auto_generate": "boolean(default=false)",
		"dictionary_generate": "boolean(default=true)",
		"no_move_beep": "boolean(default=true)",
		"edit_NVDA_gesture": "boolean(default=false)",
		"HTML_display": "string(default=block)",
		"LaTeX_delimiter": "string(default=bracket)",
	},
	"rules": {
		"SingleMsubsupType": "boolean(default=true)",
		"SingleMsubType": "boolean(default=true)",
		"SingleMsupType": "boolean(default=true)",
		"SingleMunderoverType": "boolean(default=true)",
		"SingleMunderType": "boolean(default=true)",
		"SingleMoverType": "boolean(default=true)",
		"SingleFractionType": "boolean(default=true)",
		"SingleSqrtType": "boolean(default=true)",
		"PowerType": "boolean(default=true)",
		"SquarePowerType": "boolean(default=true)",
		"CubePowerType": "boolean(default=true)",
		"SetType": "boolean(default=true)",
		"AbsoluteType": "boolean(default=true)",
		"MatrixType": "boolean(default=true)",
		"DeterminantType": "boolean(default=true)",
		"AddIntegerFractionType": "boolean(default=true)",
	}
}
