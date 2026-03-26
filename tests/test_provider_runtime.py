import importlib
import os
import sys
import types
import unittest
from unittest import mock


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLUGIN_PARENT = os.path.join(PROJECT_ROOT, "addon", "globalPlugins")
PLUGIN_ROOT = os.path.join(PROJECT_ROOT, "addon", "globalPlugins", "Access8Math")


class ConfigStub(dict):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.spec = {}


class ProviderImportHarness:
	def __init__(self, *, mathcat_factory=None, mathplayer_factory=None):
		self.mathcat_factory = mathcat_factory
		self.mathplayer_factory = mathplayer_factory
		self._patcher = None
		self._translation_patcher = None
		self.provider = None

	def __enter__(self):
		access8math_pkg = types.ModuleType("Access8Math")
		access8math_pkg.__path__ = [PLUGIN_ROOT]

		addon_handler = types.ModuleType("addonHandler")
		addon_handler.initTranslation = lambda: None

		api_module = types.ModuleType("api")
		api_module.getFocusObject = lambda: types.SimpleNamespace()

		interaction_stub = types.ModuleType("Access8Math.interaction")
		interaction_stub.A8MInteraction = type(
			"A8MInteraction",
			(),
			{
				"__init__": lambda self, parent=None: None,
				"set": lambda self, data=None, name=None, **kwargs: None,
				"setFocus": lambda self: None,
			},
		)

		config_module = types.ModuleType("config")
		config_module.conf = ConfigStub(
			{
				"Access8Math": {
					"settings": {
						"language": "en",
						"speech_source": "Access8Math",
						"braille_source": "Access8Math",
						"interact_source": "Access8Math",
					}
				}
			}
		)

		log_handler = types.ModuleType("logHandler")
		log_handler.log = types.SimpleNamespace(
			warning=lambda *args, **kwargs: None,
			error=lambda *args, **kwargs: None,
		)

		math_pres = types.ModuleType("mathPres")
		math_pres.MathPresentationProvider = type("MathPresentationProvider", (), {})

		math_player_module = types.ModuleType("mathPres.mathPlayer")

		if self.mathplayer_factory is None:
			class MissingMathPlayer:
				def __init__(self, *args, **kwargs):
					raise RuntimeError("MathPlayer unavailable")

			math_player_module.MathPlayer = MissingMathPlayer
		else:
			math_player_module.MathPlayer = self.mathplayer_factory

		global_plugins_pkg = types.ModuleType("globalPlugins")
		global_plugins_pkg.__path__ = []

		speech_module = types.ModuleType("speech")
		speech_module.speak = lambda *args, **kwargs: None

		reader_module = types.ModuleType("reader")
		reader_module.MathContent = type("MathContent", (), {})
		access8math_reader_module = types.ModuleType("Access8Math.reader")
		access8math_reader_module.MathContent = reader_module.MathContent

		output_module = types.ModuleType("output")
		output_module.translate_Braille = lambda value: value
		output_module.translate_SpeechCommand_CapNotification = lambda value: value
		access8math_output_module = types.ModuleType("Access8Math.output")
		access8math_output_module.translate_Braille = output_module.translate_Braille
		access8math_output_module.translate_SpeechCommand_CapNotification = output_module.translate_SpeechCommand_CapNotification

		modules = {
			"addonHandler": addon_handler,
			"Access8Math": access8math_pkg,
			"Access8Math.output": access8math_output_module,
			"Access8Math.reader": access8math_reader_module,
			"api": api_module,
			"config": config_module,
			"logHandler": log_handler,
			"mathPres": math_pres,
			"mathPres.mathPlayer": math_player_module,
			"globalPlugins": global_plugins_pkg,
			"speech": speech_module,
			"reader": reader_module,
			"output": output_module,
			"Access8Math.interaction": interaction_stub,
		}

		if self.mathcat_factory is not None:
			mathcat_module = types.ModuleType("globalPlugins.MathCAT")
			mathcat_module.MathCAT = self.mathcat_factory
			modules["globalPlugins.MathCAT"] = mathcat_module

		self._patcher = mock.patch.dict(sys.modules, modules)
		self._patcher.start()
		self._translation_patcher = mock.patch.object(importlib.import_module("builtins"), "_", lambda text: text, create=True)
		self._translation_patcher.start()

		for path in (PLUGIN_PARENT, PLUGIN_ROOT):
			if path not in sys.path:
				sys.path.insert(0, path)

		for name in list(sys.modules):
			if name == "Access8Math.provider" or name.startswith("Access8Math.provider."):
				sys.modules.pop(name, None)

		self.provider = importlib.import_module("Access8Math.provider")
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		for name in list(sys.modules):
			if name == "Access8Math.provider" or name.startswith("Access8Math.provider."):
				sys.modules.pop(name, None)
		if self._translation_patcher:
			self._translation_patcher.stop()
		if self._patcher:
			self._patcher.stop()


class TestProviderRuntime(unittest.TestCase):
	def test_available_providers_includes_access8math_and_detected_backends(self):
		MathCAT = type("MathCAT", (), {})
		MathPlayer = type("MathPlayer", (), {})
		with ProviderImportHarness(mathcat_factory=MathCAT, mathplayer_factory=MathPlayer) as harness:
			runtime = harness.provider.build_provider_runtime()

			self.assertEqual(
				runtime.available_providers,
				{
					"Access8Math": "Access8Math",
					"MathCAT": "MathCAT",
					"MathPlayer": "MathPlayer",
				},
			)
			self.assertEqual(runtime.available_provider_ids, ["Access8Math", "MathCAT", "MathPlayer"])

	def test_rollback_configured_sources_falls_back_to_access8math_for_missing_provider(self):
		with ProviderImportHarness() as harness:
			harness.provider.config.conf["Access8Math"]["settings"].update({
				"speech_source": "MathPlayer",
				"braille_source": "MathPlayer",
				"interact_source": "MathCAT",
			})

			harness.provider.rollback_configured_sources("MathPlayer")

			self.assertEqual(
				{
					key: harness.provider.config.conf["Access8Math"]["settings"][key]
					for key in ("speech_source", "braille_source", "interact_source")
				},
				{
					"speech_source": "Access8Math",
					"braille_source": "Access8Math",
					"interact_source": "MathCAT",
				},
			)

	def test_available_providers_labels_registered_backends(self):
		with ProviderImportHarness() as harness:
			runtime = harness.provider.RoutingProvider()
			runtime.register_provider("Access8Math", object())
			runtime.register_provider("MathCAT", object())

			self.assertEqual(
				runtime.available_providers,
				{
					"Access8Math": "Access8Math",
					"MathCAT": "MathCAT",
				},
			)

	def test_unregister_provider_removes_registered_backend(self):
		with ProviderImportHarness() as harness:
			runtime = harness.provider.RoutingProvider()
			runtime.register_provider("MathCAT", object())

			runtime.unregister_provider("MathCAT")

			self.assertNotIn("MathCAT", runtime.providers)

	def test_access8math_provider_is_defined_in_access8math_module(self):
		with ProviderImportHarness() as harness:
			self.assertEqual(harness.provider.Access8MathProvider.__module__, "Access8Math.provider.access8math")

	def test_access8math_provider_interaction_uses_package_relative_import(self):
		with ProviderImportHarness() as harness:
			access8math_module = importlib.import_module("Access8Math.provider.access8math")
			mathcontent = types.SimpleNamespace()
			access8math_module.MathContent = mock.Mock(return_value=mathcontent)
			interaction_calls = []

			class FakeInteraction:
				def __init__(self, parent=None):
					interaction_calls.append(("init", parent))

				def set(self, data=None, name=None, **kwargs):
					interaction_calls.append(("set", data, name))

				def setFocus(self):
					interaction_calls.append(("focus",))

			access8math_module.api.getFocusObject = lambda: "focus-object"
			with mock.patch.dict(
				sys.modules,
				{"Access8Math.interaction": types.SimpleNamespace(A8MInteraction=FakeInteraction)},
				clear=False,
			):
				provider = access8math_module.Access8MathProvider()
				provider.interactWithMathMl("<math />")

			self.assertEqual(interaction_calls[0], ("init", "focus-object"))
			self.assertEqual(interaction_calls[1], ("set", mathcontent, ""))
			self.assertEqual(interaction_calls[2], ("focus",))
