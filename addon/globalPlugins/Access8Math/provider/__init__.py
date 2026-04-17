import addonHandler
import config
from logHandler import log
import mathPres

from .access8math import Access8MathProvider

addonHandler.initTranslation()

SOURCE_KEYS = ("speech_source", "braille_source", "interact_source")

_runtime = None


def probe_access8math():
	provider_name = "Access8Math"
	try:
		return Access8MathProvider()
	except BaseException:
		rollback_configured_sources(provider_name)
		log.warning(f"{provider_name} not available")
		return None


def probe_mathcat():
	provider_name = "MathCAT"
	try:
		from globalPlugins.MathCAT import MathCAT
		return MathCAT()
	except ModuleNotFoundError:
		try:
			from mathPres.MathCAT.MathCAT import MathCAT
			return MathCAT()
		except BaseException:
			rollback_configured_sources(provider_name)
			log.warning(f"{provider_name} not available")
	except BaseException:
		rollback_configured_sources(provider_name)
		log.warning(f"{provider_name} not available")
		return None


def probe_mathplayer():
	provider_name = "MathPlayer"
	try:
		from mathPres.mathPlayer import MathPlayer
		return MathPlayer()

	except BaseException:
		rollback_configured_sources(provider_name)
		log.warning(f"{provider_name} not available")
		return None


def rollback_configured_sources(provider_name):
	settings = config.conf["Access8Math"]["settings"]
	for key in SOURCE_KEYS:
		if settings[key] == provider_name:
			settings[key] = "Access8Math"


def build_provider_runtime():
	global _runtime

	access8math = probe_access8math()
	mathcat = probe_mathcat()
	mathplayer = probe_mathplayer()

	_runtime = RoutingProvider()
	if access8math:
		_runtime.register_provider("Access8Math", access8math)
	if mathcat:
		_runtime.register_provider("MathCAT", mathcat)
	if mathplayer:
		_runtime.register_provider("MathPlayer", mathplayer)

	return _runtime


def get_provider_runtime():
	global _runtime
	if _runtime is None:
		_runtime = build_provider_runtime()
	return _runtime


class RoutingProvider(mathPres.MathPresentationProvider):
	PROVIDER_LABEL = {
		"Access8Math": _("Access8Math"),
		"MathCAT": _("MathCAT"),
		"MathPlayer": _("MathPlayer"),
	}

	def __init__(self):
		self.providers = {}

	def getSpeechForMathMl(self, mathMl):
		speechSequence = []

		provider = self.providers.get(config.conf["Access8Math"]["settings"]["speech_source"], None)
		if provider:
			speechSequence = provider.getSpeechForMathMl(mathMl)

		return speechSequence

	def getBrailleForMathMl(self, mathMl):
		cells = ""

		provider = self.providers.get(config.conf["Access8Math"]["settings"]["braille_source"], None)
		if provider:
			cells = provider.getBrailleForMathMl(mathMl)

		def inrange(cell):
			return 0x2800 <= ord(cell) < 0x2800 + 256

		cells = [cell if inrange(cell) else chr(0x2800) for cell in cells]
		return "".join(cells)

	def interactWithMathMl(self, mathMl):
		provider = self.providers.get(config.conf["Access8Math"]["settings"]["interact_source"], None)
		if provider:
			provider.interactWithMathMl(mathMl)

	def register_provider(self, name, provider):
		self.providers[name] = provider

	def unregister_provider(self, name):
		self.providers.pop(name, None)

	@property
	def available_providers(self):
		result = {}
		for key in self.providers:
			if key in self.PROVIDER_LABEL:
				result[key] = self.PROVIDER_LABEL[key]
			else:
				result[key] = key
		return result

	@property
	def available_provider_ids(self):
		return list(self.available_providers.keys())
