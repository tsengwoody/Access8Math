import builtins
import importlib
import os
import sys
import types
import unittest
from unittest import mock


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLUGIN_PARENT = os.path.join(PROJECT_ROOT, "addon", "globalPlugins")
PLUGIN_ROOT = os.path.join(PLUGIN_PARENT, "Access8Math")


class ConfigStub(dict):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.spec = {}


class EntryPointImportHarness:
	def __init__(self, *, focus_object=None):
		self.focus_object = focus_object or types.SimpleNamespace(
			name="focused object",
			appModule=types.SimpleNamespace(appName="explorer"),
		)
		self.selected_path = r"C:\Users\alice\Desktop\report.txt"
		self.context_menu_paths = []
		self.context_menu_views = []
		self.editor_paths = []
		self.editor_frames = []
		self.explorer_calls = []
		self.math_pres_register = mock.Mock()
		self._patcher = None
		self._translation_patcher = None
		self.module = None

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
		api_module.getFocusObject = lambda: self.focus_object

		app_modules = types.ModuleType("appModules")
		app_modules.explorer = types.SimpleNamespace(
			AppModule=type("ExplorerAppModule", (), {})
		)

		config_module = types.ModuleType("config")
		config_module.conf = ConfigStub(
			{
				"Access8Math": {
					"settings": {
						"language": "en",
						"command_mode": False,
						"navigate_mode": False,
						"shortcut_mode": False,
						"writeNavAudioIndication": False,
						"writeNavAcrossLine": False,
						"LaTeX_delimiter": "bracket",
						"Nemeth_delimiter": "at",
						"speech_source": "Access8Math",
						"braille_source": "Access8Math",
						"interact_source": "Access8Math",
					}
				}
			}
		)

		control_types = types.ModuleType("controlTypes")
		control_types.Role = types.SimpleNamespace(WINDOW=1, EDITABLETEXT=2)

		global_plugin_handler = types.ModuleType("globalPluginHandler")
		global_plugin_handler.GlobalPlugin = type("GlobalPlugin", (), {})

		global_vars = types.ModuleType("globalVars")
		global_vars.appArgs = types.SimpleNamespace(secure=False)
		global_vars.mathcontent = ""

		gui_module = types.ModuleType("gui")
		gui_module.mainFrame = types.SimpleNamespace(
			sysTrayIcon=types.SimpleNamespace(
				toolsMenu=types.SimpleNamespace(),
				Bind=lambda *args, **kwargs: None,
			)
		)
		gui_module.settingsDialogs = types.SimpleNamespace(
			NVDASettingsDialog=types.SimpleNamespace(categoryClasses=[])
		)

		language_handler = types.ModuleType("languageHandler")
		language_handler.getWindowsLanguage = lambda: "en"

		log_handler = types.ModuleType("logHandler")
		log_handler.log = types.SimpleNamespace(
			warning=lambda *args, **kwargs: None,
			error=lambda *args, **kwargs: None,
		)

		event_handler = types.ModuleType("eventHandler")
		event_handler.executeEvent = lambda *args, **kwargs: None

		math_pres = types.ModuleType("mathPres")
		math_pres.registerProvider = self.math_pres_register
		math_pres.interactionProvider = types.SimpleNamespace()
		math_pres.speechProvider = types.SimpleNamespace()

		math_player_module = types.ModuleType("mathPres.mathPlayer")
		math_player_module.MathPlayer = type("MathPlayer", (), {})

		nvda_objects = types.ModuleType("NVDAObjects")
		nvda_objects.__path__ = []
		nvda_objects.NVDAObject = type("NVDAObject", (), {"__init__": lambda self, *args, **kwargs: None})

		iaccessible_module = types.ModuleType("NVDAObjects.IAccessible")
		iaccessible_module.IAccessible = type("IAccessible", (nvda_objects.NVDAObject,), {})

		script_handler = types.ModuleType("scriptHandler")
		script_handler.script = lambda *args, **kwargs: (lambda func: func)

		keyboard_handler = types.ModuleType("keyboardHandler")
		keyboard_handler.KeyboardInputGesture = type("KeyboardInputGesture", (), {})

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

		wx_module = types.ModuleType("wx")
		wx_module.ID_ANY = -1
		wx_module.EVT_MENU = object()
		wx_module.Menu = type("Menu", (), {"Append": lambda self, *args, **kwargs: types.SimpleNamespace()})
		wx_module.CallAfter = lambda func, *args, **kwargs: func(*args, **kwargs)

		nvda_window_module = types.ModuleType("NVDAObjects.window")
		nvda_window_module.Window = type("Window", (), {})

		lxml_module = types.ModuleType("lxml")
		lxml_etree_module = types.ModuleType("lxml.etree")
		lxml_etree_module.ElementTree = type("ElementTree", (), {})
		lxml_etree_module.SubElement = lambda *args, **kwargs: None
		lxml_etree_module.Comment = lambda *args, **kwargs: None
		lxml_etree_module.ProcessingInstruction = lambda *args, **kwargs: None
		lxml_etree_module.XPath = type("XPath", (), {})
		lxml_etree_module.ElementBase = type("ElementBase", (), {})
		lxml_etree_module.PythonElementClassLookup = type("PythonElementClassLookup", (), {})
		lxml_etree_module.fromstring = lambda *args, **kwargs: None
		lxml_etree_module.parse = lambda *args, **kwargs: None
		lxml_etree_module.XML = lambda *args, **kwargs: None
		lxml_etree_module.HTML = lambda *args, **kwargs: None
		lxml_etree_module.tostring = lambda *args, **kwargs: b""
		lxml_etree_module.Element = lambda *args, **kwargs: types.SimpleNamespace()
		lxml_module.etree = lxml_etree_module

		reader_module = types.ModuleType("reader")
		reader_module.exist_language = lambda language: True
		reader_module.initialize = lambda settings: None
		access8math_reader_module = types.ModuleType("Access8Math.reader")
		access8math_reader_module.exist_language = reader_module.exist_language
		access8math_reader_module.initialize = reader_module.initialize

		command_pkg = package("Access8Math.command")
		command_context = types.ModuleType("Access8Math.command.context")

		class FakeContextMenuView:
			def __init__(self, path=None):
				self.path = path
				self.focused = False
				self.set_focus_called = False
				self.context_menu_views.append(self)
				self.context_menu_paths.append(path)

			def setFocus(self):
				self.focused = True
				self.set_focus_called = True

		FakeContextMenuView.context_menu_paths = self.context_menu_paths
		FakeContextMenuView.context_menu_views = self.context_menu_views
		command_context.A8MFEVContextMenuView = FakeContextMenuView

		dialogs_module = types.ModuleType("Access8Math.dialogs")
		dialogs_module.NewLanguageAddingDialog = type("NewLanguageAddingDialog", (), {})
		dialogs_module.UnicodeDicDialog = type("UnicodeDicDialog", (), {})
		dialogs_module.MathRuleDialog = type("MathRuleDialog", (), {})
		dialogs_module.MathReaderSettingsPanel = type("MathReaderSettingsPanel", (), {})
		dialogs_module.Access8MathSettingsDialog = type("Access8MathSettingsDialog", (), {})

		editor_module = types.ModuleType("Access8Math.editor")

		class FakeEditorFrame:
			def __init__(self, path=None):
				self.path = path
				self.shown = False
				self.show_args = []
				self.editor_frames.append(self)
				self.editor_paths.append(path)

			def Show(self, value):
				self.shown = value
				self.show_args.append(value)

			def control(self):
				return types.SimpleNamespace(SetValue=lambda value: None)

		FakeEditorFrame.editor_paths = self.editor_paths
		FakeEditorFrame.editor_frames = self.editor_frames
		editor_module.EditorFrame = FakeEditorFrame

		interaction_module = types.ModuleType("Access8Math.interaction")
		interaction_module.A8MInteraction = type("A8MInteraction", (), {})

		provider_module = types.ModuleType("Access8Math.provider")
		provider_module.access8math_instance = object()
		provider_module.runtime = types.SimpleNamespace(
			access8math=provider_module.access8math_instance,
			available_providers=["Access8Math", "MathCAT"],
			mathcat=object(),
			mathplayer=None,
			extend_reader_options=lambda options: dict(options),
		)
		provider_module.build_provider_runtime = mock.Mock(return_value=provider_module.runtime)
		provider_module.get_provider_runtime = mock.Mock(return_value=provider_module.runtime)
		self.provider_module = provider_module

		writer_module = types.ModuleType("Access8Math.writer")
		writer_module.TextMathEditField = type("TextMathEditField", (), {})

		lib_pkg = package("Access8Math.lib")
		explorer_module = types.ModuleType("Access8Math.lib.explorer")
		explorer_module.get_selected_file = mock.Mock(side_effect=lambda *args, **kwargs: self.selected_path)

		modules = {
			"addonHandler": addon_handler,
			"api": api_module,
			"appModules": app_modules,
			"config": config_module,
			"controlTypes": control_types,
			"globalPluginHandler": global_plugin_handler,
			"globalVars": global_vars,
			"gui": gui_module,
			"eventHandler": event_handler,
			"languageHandler": language_handler,
			"logHandler": log_handler,
			"mathPres": math_pres,
			"mathPres.mathPlayer": math_player_module,
			"NVDAObjects": nvda_objects,
			"NVDAObjects.IAccessible": iaccessible_module,
			"NVDAObjects.window": nvda_window_module,
			"lxml": lxml_module,
			"lxml.etree": lxml_etree_module,
			"keyboardHandler": keyboard_handler,
			"scriptHandler": script_handler,
			"textInfos": text_infos,
			"textInfos.offsets": text_infos_offsets,
			"tones": tones_module,
			"ui": ui_module,
			"wx": wx_module,
			"reader": reader_module,
			"Access8Math.reader": access8math_reader_module,
			"Access8Math.command": command_pkg,
			"Access8Math.command.context": command_context,
			"Access8Math.dialogs": dialogs_module,
			"Access8Math.editor": editor_module,
			"Access8Math.interaction": interaction_module,
			"Access8Math.provider": provider_module,
			"Access8Math.writer": writer_module,
			"Access8Math.lib": lib_pkg,
			"Access8Math.lib.explorer": explorer_module,
		}
		self._modules = modules

		self._patcher = mock.patch.dict(sys.modules, modules)
		self._patcher.start()
		self._translation_patcher = mock.patch.object(builtins, "_", lambda text: text, create=True)
		self._translation_patcher.start()

		for path in (PLUGIN_PARENT, PLUGIN_ROOT):
			if path not in sys.path:
				sys.path.insert(0, path)

		# Access8Math.__init__ eagerly imports sibling modules, so the harness
		# has to re-register the stubs after clearing cached package modules.
		for name in list(sys.modules):
			if name == "Access8Math" or name.startswith("Access8Math."):
				sys.modules.pop(name, None)

		sys.modules.update(self._modules)

		self.module = importlib.import_module("Access8Math")
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		for name in list(sys.modules):
			if name == "Access8Math" or name.startswith("Access8Math."):
				sys.modules.pop(name, None)
		if self._translation_patcher:
			self._translation_patcher.stop()
		if self._patcher:
			self._patcher.stop()


class TestAccess8MathEntrypoints(unittest.TestCase):
	def test_init_registers_provider_from_provider_module(self):
		with EntryPointImportHarness() as harness:
			harness.provider_module.build_provider_runtime.assert_called_once_with()
			harness.math_pres_register.assert_called_once_with(
				harness.provider_module.runtime,
				speech=True,
				braille=True,
				interaction=True,
			)

	def test_virtual_context_menu_passes_selected_file_path_to_context_menu_view(self):
		with EntryPointImportHarness() as harness:
			context_menu = harness.module.VirtualContextMenu()

			context_menu.script_open_virtual_context_menu(None)

			harness.module.explorer.get_selected_file.assert_called_once()
			self.assertEqual(harness.context_menu_paths, [harness.selected_path])
			self.assertEqual(len(harness.context_menu_views), 1)
			self.assertTrue(harness.context_menu_views[0].set_focus_called)

	def test_editor_popup_passes_selected_file_path_to_editor_frame(self):
		with EntryPointImportHarness() as harness:
			context_menu = harness.module.VirtualContextMenu()

			context_menu.script_editor_popup(None)

			harness.module.explorer.get_selected_file.assert_called_once()
			self.assertEqual(harness.editor_paths, [harness.selected_path])
			self.assertEqual(len(harness.editor_frames), 1)
			self.assertEqual(harness.editor_frames[0].show_args, [True])
