import config
import os
import sys
import tones

if sys.version_info.major == 2:
	unicode = unicode
elif sys.version_info.major >= 3:
	unicode = str

settings = [
	"IFS",
	"AMM",
	"DG",
	"AG",
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
	"SetType",
	"AbsoluteType",
	"MatrixType",
	"DeterminantType",
	"AddIntegerFractionType",
]

def initialize_config():
	config.conf["Access8Math"] = {}
	config.conf["Access8Math"]["language"] = "pt"
	config.conf["Access8Math"]["item_interval_time"] = "50"
	for k in settings:
		config.conf["Access8Math"][k] = u"True"
	tones.beep(100,100)

def environ_from_config():
	try:
		os.environ['LANGUAGE'] = 'pt' #config.conf["Access8Math"]["language"]
		for k in settings:
			os.environ[k] = unicode(True if config.conf["Access8Math"][k] in [u'True', u'true', True] else False)
		os.environ['item_interval_time'] = config.conf["Access8Math"]["item_interval_time"]
	except:
		initialize_config()
		os.environ['LANGUAGE'] = 'pt' #config.conf["Access8Math"]["language"]
		for k in settings:
			os.environ[k] = unicode(True if config.conf["Access8Math"][k] in [u'True', u'true', True] else False)
		os.environ['item_interval_time'] = config.conf["Access8Math"]["item_interval_time"]
	# finally:
		# from logHandler import log
		# log.error('============================')
		# log.error(os.environ['LANGUAGE'])
		# log.error('============================')
