import config

_configSpec = u"""[settings]
language = string(default=en)
braille_language = string(default=en)
item_interval_time = integer(default=50,min=0,max=100)
interaction_frame_show = boolean(default=false)
analyze_math_meaning = boolean(default=true)
auto_generate = boolean(default=false)
dictionary_generate = boolean(default=true)
no_move_beep = boolean(default=true)
command_mode = boolean(default=false)
navigate_mode = boolean(default=false)
shortcut_mode = boolean(default=false)
writeNavAudioIndication = boolean(default=true)
HTML_display = string(default=block)
LaTeX_delimiter = string(default=bracket)
speech_source = string(default=Access8Math)
braille_source = string(default=Access8Math)
interact_source = string(default=Access8Math)

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
		"language": "string(default=en)",
		"braille_language": "string(default=en)",
		"item_interval_time": "integer(default=50,min=0,max=100)",
		"interaction_frame_show": "boolean(default=false)",
		"analyze_math_meaning": "boolean(default=true)",
		"auto_generate": "boolean(default=false)",
		"dictionary_generate": "boolean(default=true)",
		"no_move_beep": "boolean(default=true)",
		"command_mode": "boolean(default=false)",
		"navigate_mode": "boolean(default=false)",
		"shortcut_mode": "boolean(default=false)",
		"writeNavAudioIndication": "boolean(default=true)",
		"HTML_display": "string(default=block)",
		"LaTeX_delimiter": "string(default=bracket)",
		"speech_source": "string(default=Access8Math)",
		"braille_source": "string(default=Access8Math)",
		"interact_source": "string(default=Access8Math)",
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
