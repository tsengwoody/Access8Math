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
		self._added_plugin_parent = False
		self.provider = None

	def __enter__(self):
		def package(name):
			module = types.ModuleType(name)
			module.__path__ = []
			return module

		addon_handler = types.ModuleType("addonHandler")
		addon_handler.initTranslation = lambda: None
		addon_handler.getCodeAddon = lambda: types.SimpleNamespace(
			manifest={"summary": "Access8Math", "version": "0.0"}
		)

		api_module = types.ModuleType("api")
		api_module.getFocusObject = lambda: types.SimpleNamespace()
		api_module.getForegroundObject = lambda: types.SimpleNamespace(
			appModule=types.SimpleNamespace(appName="explorer"),
			windowHandle=0,
		)

		app_modules = types.ModuleType("appModules")
		app_modules.explorer = types.SimpleNamespace(
			AppModule=type("ExplorerAppModule", (), {})
		)

		control_types = types.ModuleType("controlTypes")
		control_types.Role = types.SimpleNamespace(WINDOW=1, EDITABLETEXT=2, MATH=3)

		global_plugin_handler = types.ModuleType("globalPluginHandler")
		global_plugin_handler.GlobalPlugin = type("GlobalPlugin", (), {})

		global_vars = types.ModuleType("globalVars")
		global_vars.appArgs = types.SimpleNamespace(secure=False)
		global_vars.mathcontent = ""

		gui_module = types.ModuleType("gui")
		gui_module.__path__ = []
		gui_module.mainFrame = types.SimpleNamespace(
			sysTrayIcon=types.SimpleNamespace(
				toolsMenu=types.SimpleNamespace(),
				Bind=lambda *args, **kwargs: None,
			)
		)
		gui_module.settingsDialogs = types.SimpleNamespace(
			NVDASettingsDialog=types.SimpleNamespace(categoryClasses=[])
		)

		gui_helper_module = types.ModuleType("gui.guiHelper")
		gui_helper_module.BoxSizerHelper = type(
			"BoxSizerHelper",
			(),
			{
				"__init__": lambda self, *args, **kwargs: None,
				"addLabeledControl": lambda self, *args, **kwargs: types.SimpleNamespace(Selection=0, GetSelection=lambda: 0),
				"addItem": lambda self, *args, **kwargs: types.SimpleNamespace(SetValue=lambda value: None, IsChecked=lambda: True),
			},
		)

		gui_context_help = types.ModuleType("gui.contextHelp")
		gui_context_help.ContextHelpMixin = type("ContextHelpMixin", (), {})

		gui_nvdacontrols = types.ModuleType("gui.nvdaControls")

		gui_settings_dialogs = types.ModuleType("gui.settingsDialogs")
		gui_settings_dialogs.MultiCategorySettingsDialog = type("MultiCategorySettingsDialog", (), {})
		gui_settings_dialogs.SettingsDialog = type("SettingsDialog", (), {})
		gui_settings_dialogs.SettingsPanel = type("SettingsPanel", (), {})

		language_handler = types.ModuleType("languageHandler")
		language_handler.getWindowsLanguage = lambda: "en"

		event_handler = types.ModuleType("eventHandler")
		event_handler.executeEvent = lambda *args, **kwargs: None

		novel_window_module = types.ModuleType("NVDAObjects.window")
		novel_window_module.Window = type("Window", (), {})

		nvda_objects = types.ModuleType("NVDAObjects")
		nvda_objects.__path__ = []
		nvda_objects.NVDAObject = type("NVDAObject", (), {"__init__": lambda self, *args, **kwargs: None})

		iaccessible_module = types.ModuleType("NVDAObjects.IAccessible")
		iaccessible_module.IAccessible = type("IAccessible", (nvda_objects.NVDAObject,), {})

		script_handler = types.ModuleType("scriptHandler")
		script_handler.script = lambda *args, **kwargs: (lambda func: func)

		keyboard_handler = types.ModuleType("keyboardHandler")
		keyboard_handler.KeyboardInputGesture = type(
			"KeyboardInputGesture",
			(),
			{"fromName": classmethod(lambda cls, name: types.SimpleNamespace(send=lambda: None))},
		)

		text_infos = types.ModuleType("textInfos")
		text_infos.POSITION_CARET = "caret"
		text_infos.POSITION_ALL = "all"
		text_infos.POSITION_FIRST = "first"
		text_infos.UNIT_CHARACTER = "character"
		text_infos_offsets = types.ModuleType("textInfos.offsets")
		text_infos_offsets.OffsetsTextInfo = type("OffsetsTextInfo", (), {})
		text_infos.offsets = text_infos_offsets

		tones_module = types.ModuleType("tones")
		tones_module.beep = lambda *args, **kwargs: None

		ui_module = types.ModuleType("ui")
		ui_module.message = lambda *args, **kwargs: None

		class WxObject:
			def __init__(self, *args, **kwargs):
				pass

		wx_module = types.ModuleType("wx")
		wx_module.ID_ANY = -1
		wx_module.ID_NEW = 1
		wx_module.ID_OPEN = 2
		wx_module.ID_SAVE = 3
		wx_module.ID_SAVEAS = 4
		wx_module.ID_EXIT = 5
		wx_module.ITEM_NORMAL = 0
		wx_module.DEFAULT_FRAME_STYLE = 0
		wx_module.TE_MULTILINE = 0
		wx_module.HORIZONTAL = 0
		wx_module.WXK_ESCAPE = 27
		wx_module.EVT_MENU = object()
		wx_module.EVT_BUTTON = object()
		wx_module.EVT_FIND = object()
		wx_module.EVT_FIND_NEXT = object()
		wx_module.EVT_FIND_REPLACE = object()
		wx_module.EVT_FIND_REPLACE_ALL = object()
		wx_module.EVT_CLOSE = object()
		wx_module.EVT_TEXT = object()
		wx_module.EVT_CHAR_HOOK = object()
		wx_module.Frame = WxObject
		wx_module.Panel = WxObject
		wx_module.MenuBar = WxObject
		wx_module.Menu = type("Menu", (), {"Append": lambda self, *args, **kwargs: types.SimpleNamespace(), "AppendMenu": lambda self, *args, **kwargs: None, "AppendSeparator": lambda self: None})
		wx_module.TextCtrl = WxObject
		wx_module.FindReplaceData = WxObject
		wx_module.Button = WxObject
		wx_module.CheckBox = WxObject
		wx_module.Choice = WxObject
		wx_module.Dialog = WxObject
		wx_module.BoxSizer = WxObject
		wx_module.NewId = lambda: 1
		wx_module.GetApp = lambda: types.SimpleNamespace(TopWindow=None)
		wx_module.CallAfter = lambda func, *args, **kwargs: func(*args, **kwargs)
		wx_module.CallLater = lambda delay, func, *args, **kwargs: func(*args, **kwargs)
		wx_module.Size = lambda *args, **kwargs: types.SimpleNamespace()

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
			debugWarning=lambda *args, **kwargs: None,
		)

		math_pres = types.ModuleType("mathPres")
		math_pres.interactionProvider = types.SimpleNamespace()
		math_pres.speechProvider = types.SimpleNamespace()
		math_pres.MathPresentationProvider = type("MathPresentationProvider", (), {})
		math_pres.registerProvider = mock.Mock()

		braille_module = types.ModuleType("braille")
		braille_module.NVDAObjectRegion = type("NVDAObjectRegion", (), {})

		braille_tables = types.ModuleType("brailleTables")
		braille_tables.TABLES_DIR = ""
		braille_tables.TableType = types.SimpleNamespace(OUTPUT=0)
		braille_tables.getDefaultTableForCurLang = lambda table_type: "en-ueb-g1.ctb"

		louis_helper = types.ModuleType("louisHelper")
		louis_helper.translate = lambda args, string, mode=4: ([], [], [], [])

		speech_xml = types.ModuleType("speechXml")
		speech_xml.SsmlParser = type("SsmlParser", (), {"convertFromXml": lambda self, xml: []})

		speech_module = types.ModuleType("speech")
		speech_module.__path__ = []
		speech_module.speak = lambda *args, **kwargs: None

		speech_commands_module = types.ModuleType("speech.commands")
		speech_commands_module.BreakCommand = type("BreakCommand", (), {})
		speech_commands_module.PitchCommand = type("PitchCommand", (), {})

		speech_speech_module = types.ModuleType("speech.speech")
		speech_speech_module._getSpellingCharAddCapNotification = lambda *args, **kwargs: []

		synth_driver_handler = types.ModuleType("synthDriverHandler")
		synth_driver_handler.getSynth = lambda: types.SimpleNamespace(name="dummy", supportedCommands=[])

		character_processing = types.ModuleType("characterProcessing")
		character_processing._getSpeechSymbolsForLocale = lambda language: (
			types.SimpleNamespace(symbols={}),
			types.SimpleNamespace(symbols={}),
		)

		comtypes_module = types.ModuleType("comtypes")
		comtypes_client = types.ModuleType("comtypes.client")
		comtypes_client.CreateObject = lambda *args, **kwargs: types.SimpleNamespace(Windows=lambda: [])
		comtypes_module.client = comtypes_client

		nvwave_module = types.ModuleType("nvwave")
		nvwave_module.playWaveFile = lambda *args, **kwargs: None

		core_module = types.ModuleType("core")
		queue_handler = types.ModuleType("queueHandler")

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

		output_module = types.ModuleType("output")
		output_module.translate_Braille = lambda value: value
		output_module.translate_SpeechCommand_CapNotification = lambda value: value
		access8math_output_module = types.ModuleType("Access8Math.output")
		access8math_output_module.translate_Braille = output_module.translate_Braille
		access8math_output_module.translate_SpeechCommand_CapNotification = output_module.translate_SpeechCommand_CapNotification
		access8math_output_module.translate_Unicode = lambda value: value

		reader_module = types.ModuleType("reader")
		reader_module.MathContent = type("MathContent", (), {})
		access8math_reader_module = types.ModuleType("Access8Math.reader")
		access8math_reader_module.MathContent = reader_module.MathContent
		access8math_reader_module.exist_language = lambda language: True
		access8math_reader_module.initialize = lambda settings: None

		writer_actions_module = types.ModuleType("Access8Math.writer.actions")
		writer_actions_module.WriterActionsMixin = type("WriterActionsMixin", (), {})
		writer_gestures_module = types.ModuleType("Access8Math.writer.gestures")
		writer_gestures_module.WriterGestureMixin = type("WriterGestureMixin", (), {})
		writer_routing_module = types.ModuleType("Access8Math.writer.routing")
		writer_routing_module.WriterRoutingMixin = type("WriterRoutingMixin", (), {})
		writer_session_module = types.ModuleType("Access8Math.writer.session")
		writer_session_module.SectionManager = type("SectionManager", (), {})
		writer_module = types.ModuleType("Access8Math.writer")
		writer_module.TextMathEditField = type("TextMathEditField", (), {})

		command_pkg = package("Access8Math.command")
		command_context = types.ModuleType("Access8Math.command.context")
		command_context.A8MFEVContextMenuView = type("A8MFEVContextMenuView", (), {})
		command_context.A8MFEVContextMenuViewTextInfo = type("A8MFEVContextMenuViewTextInfo", (), {})
		command_models = types.ModuleType("Access8Math.command.models")
		command_models.MenuModel = type("MenuModel", (), {})
		command_views = types.ModuleType("Access8Math.command.views")
		command_views.MenuView = type("MenuView", (), {"__init__": lambda self, *args, **kwargs: None, "getScript": lambda self, gesture: None})
		command_views.MenuViewTextInfo = type("MenuViewTextInfo", (), {})
		command_clipboard = types.ModuleType("Access8Math.command.clipboard")
		command_clipboard.clearClipboard = lambda: None
		command_batch = types.ModuleType("Access8Math.command.batch")
		command_batch.A8MBatchCommandView = type("A8MBatchCommandView", (), {})
		command_autocomplete = types.ModuleType("Access8Math.command.autocomplete")
		command_autocomplete.A8MAutocompleteCommandView = type("A8MAutocompleteCommandView", (), {})
		command_mark = types.ModuleType("Access8Math.command.mark")
		command_mark.A8MMarkCommandView = type("A8MMarkCommandView", (), {})
		command_latex = types.ModuleType("Access8Math.command.latex")
		command_latex.A8MLaTeXCommandView = type("A8MLaTeXCommandView", (), {})
		command_translate = types.ModuleType("Access8Math.command.translate")
		command_translate.A8MTranslateCommandView = type("A8MTranslateCommandView", (), {})

		dialogs_module = types.ModuleType("Access8Math.dialogs")
		dialogs_module.NewLanguageAddingDialog = type("NewLanguageAddingDialog", (), {})
		dialogs_module.UnicodeDicDialog = type("UnicodeDicDialog", (), {})
		dialogs_module.MathRuleDialog = type("MathRuleDialog", (), {})
		dialogs_module.MathReaderSettingsPanel = type("MathReaderSettingsPanel", (), {})
		dialogs_module.Access8MathSettingsDialog = type("Access8MathSettingsDialog", (), {})

		editor_module = types.ModuleType("Access8Math.editor")
		editor_module.EditorFrame = type("EditorFrame", (), {"__init__": lambda self, path=None: None, "Show": lambda self, value: None})

		interaction_module = types.ModuleType("Access8Math.interaction")
		interaction_module.A8MInteraction = type(
			"A8MInteraction",
			(),
			{
				"__init__": lambda self, parent=None, root=None: None,
				"set": lambda self, data=None, name=None, **kwargs: None,
				"setFocus": lambda self: None,
			},
		)
		interaction_stub = interaction_module

		modules = {
			"addonHandler": addon_handler,
			"appModules": app_modules,
			"api": api_module,
			"braille": braille_module,
			"brailleTables": braille_tables,
			"characterProcessing": character_processing,
			"comtypes": comtypes_module,
			"comtypes.client": comtypes_client,
			"config": config_module,
			"controlTypes": control_types,
			"core": core_module,
			"eventHandler": event_handler,
			"globalPluginHandler": global_plugin_handler,
			"globalVars": global_vars,
			"gui": gui_module,
			"gui.contextHelp": gui_context_help,
			"gui.guiHelper": gui_helper_module,
			"gui.nvdaControls": gui_nvdacontrols,
			"gui.settingsDialogs": gui_settings_dialogs,
			"Access8Math.output": access8math_output_module,
			"Access8Math.reader": access8math_reader_module,
			"keyboardHandler": keyboard_handler,
			"languageHandler": language_handler,
			"logHandler": log_handler,
			"mathPres": math_pres,
			"mathPres.mathPlayer": math_player_module,
			"nvwave": nvwave_module,
			"NVDAObjects": nvda_objects,
			"NVDAObjects.IAccessible": iaccessible_module,
			"NVDAObjects.window": novel_window_module,
			"queueHandler": queue_handler,
			"globalPlugins": global_plugins_pkg,
			"speech": speech_module,
			"speech.commands": speech_commands_module,
			"speech.speech": speech_speech_module,
			"scriptHandler": script_handler,
			"synthDriverHandler": synth_driver_handler,
			"textInfos": text_infos,
			"textInfos.offsets": text_infos_offsets,
			"tones": tones_module,
			"ui": ui_module,
			"wx": wx_module,
			"reader": reader_module,
			"Access8Math.interaction": interaction_stub,
			"Access8Math.command": command_pkg,
			"Access8Math.command.batch": command_batch,
			"Access8Math.command.autocomplete": command_autocomplete,
			"Access8Math.command.clipboard": command_clipboard,
			"Access8Math.command.context": command_context,
			"Access8Math.command.latex": command_latex,
			"Access8Math.command.mark": command_mark,
			"Access8Math.command.models": command_models,
			"Access8Math.command.translate": command_translate,
			"Access8Math.command.views": command_views,
			"Access8Math.dialogs": dialogs_module,
			"Access8Math.editor": editor_module,
			"Access8Math.writer": writer_module,
			"Access8Math.writer.actions": writer_actions_module,
			"Access8Math.writer.gestures": writer_gestures_module,
			"Access8Math.writer.routing": writer_routing_module,
			"Access8Math.writer.session": writer_session_module,
		}

		if self.mathcat_factory is not None:
			mathcat_module = types.ModuleType("globalPlugins.MathCAT")
			mathcat_module.MathCAT = self.mathcat_factory
			modules["globalPlugins.MathCAT"] = mathcat_module

		self._patcher = mock.patch.dict(sys.modules, modules)
		self._patcher.start()
		self._translation_patcher = mock.patch.object(importlib.import_module("builtins"), "_", lambda text: text, create=True)
		self._translation_patcher.start()

		if PLUGIN_PARENT not in sys.path:
			sys.path.insert(0, PLUGIN_PARENT)
			self._added_plugin_parent = True

		for name in list(sys.modules):
			if name == "Access8Math.provider" or name.startswith("Access8Math.provider."):
				sys.modules.pop(name, None)

		try:
			self.provider = importlib.import_module("Access8Math.provider")
			return self
		except BaseException:
			if self._added_plugin_parent:
				try:
					sys.path.remove(PLUGIN_PARENT)
				except ValueError:
					pass
				self._added_plugin_parent = False
			if self._translation_patcher:
				self._translation_patcher.stop()
				self._translation_patcher = None
			if self._patcher:
				self._patcher.stop()
				self._patcher = None
			raise

	def __exit__(self, exc_type, exc_val, exc_tb):
		for name in list(sys.modules):
			if name == "Access8Math.provider" or name.startswith("Access8Math.provider."):
				sys.modules.pop(name, None)
		if self._added_plugin_parent:
			try:
				sys.path.remove(PLUGIN_PARENT)
			except ValueError:
				pass
			self._added_plugin_parent = False
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

	def test_reader_package_imports_from_filesystem_without_package_root_in_sys_path(self):
		with ProviderImportHarness() as harness:
			sys.modules.pop("Access8Math.reader", None)
			try:
				reader_module = importlib.import_module("Access8Math.reader")
				self.assertTrue(reader_module.__file__.startswith(PLUGIN_ROOT))
				self.assertNotIn(PLUGIN_ROOT, sys.path)
			finally:
				sys.modules.pop("Access8Math.reader", None)

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
