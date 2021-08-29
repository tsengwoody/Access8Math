from io import StringIO
import os.path
import configobj
from configobj.validate import Validator
import globalVars
from logHandler import log

CONFIG_FILENAME = "Access8Math.ini"

Access8MathConfig = None

_configSpec = u"""[settings]
provider = string(default=Access8Math)
language = string(default=en)
item_interval_time = integer(default=50,min=0,max=100)
interaction_frame_show = boolean(default=false)
analyze_math_meaning = boolean(default=true)
auto_generate = boolean(default=false)
dictionary_generate = boolean(default=true)
no_move_beep = boolean(default=true)
edit_NVDA_gesture = boolean(default=true)
HTML_display = string(default=block)

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

def load():
	global Access8MathConfig
	if not Access8MathConfig:
		path = os.path.join(globalVars.appArgs.configPath, CONFIG_FILENAME)
		Access8MathConfig = configobj.ConfigObj(path, configspec=StringIO(_configSpec), encoding="utf-8")
		Access8MathConfig.newlines = "\r\n"
		Access8MathConfig.stringify = True
		val = Validator()
		ret = Access8MathConfig.validate(val, preserve_errors=True, copy=True)
		if ret != True:
			log.warning("Access8Math configuration is invalid: %s", ret)

def save():
	global Access8MathConfig
	if not Access8MathConfig:
		raise RuntimeError("Access8Math config is not loaded.")
	val = Validator()
	Access8MathConfig.validate(val, copy=True)
	Access8MathConfig.write()
