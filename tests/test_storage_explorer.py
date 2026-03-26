import importlib
import os
import sys
import types
import unittest
from unittest import mock


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLUGIN_ROOT = os.path.join(PROJECT_ROOT, "addon", "globalPlugins", "Access8Math")


class FakeConfigObject:
	def __init__(self, name=None, app_name=None, window_handle=1):
		self.name = name
		self.windowHandle = window_handle
		self.appModule = types.SimpleNamespace(appName=app_name)


class ExplorerImportHarness:
	def __init__(self, *, foreground=None, desktop_name="focused item", com_windows=None, com_error=False, ps_stdout=None):
		self.foreground = foreground or FakeConfigObject(app_name="explorer")
		self.desktop_name = desktop_name
		self.com_windows = list(com_windows or [])
		self.com_error = com_error
		self.ps_stdout = ps_stdout
		self.calls = []
		self.explorer = None
		self._patcher = None
		self._subprocess_patcher = None
		self._old_userprofile = None

	def __enter__(self):
		access8math_pkg = types.ModuleType("Access8Math")
		access8math_pkg.__path__ = [PLUGIN_ROOT]

		api_module = types.ModuleType("api")
		api_module.getForegroundObject = lambda: self.foreground
		api_module.getDesktopObject = lambda: types.SimpleNamespace(
			objectWithFocus=lambda: types.SimpleNamespace(name=self.desktop_name)
		)

		ui_module = types.ModuleType("ui")
		ui_module.message = lambda *args, **kwargs: None

		comtypes_module = types.ModuleType("comtypes")
		comtypes_client_module = types.ModuleType("comtypes.client")

		def create_object(name):
			self.calls.append(("com", name))
			if self.com_error:
				raise RuntimeError("COM unavailable")
			return types.SimpleNamespace(Windows=lambda: list(self.com_windows))

		comtypes_client_module.CreateObject = create_object
		comtypes_module.client = comtypes_client_module

		subprocess_module = types.ModuleType("subprocess")
		subprocess_module.DEVNULL = object()
		subprocess_module.PIPE = object()
		subprocess_module.STARTF_USESHOWWINDOW = 1

		class FakeStartupInfo:
			def __init__(self):
				self.dwFlags = 0

		class FakeProcess:
			def __init__(self, stdout):
				self.returncode = 0
				self._stdout = stdout

			def communicate(self):
				return self._stdout, ""

		subprocess_module.STARTUPINFO = FakeStartupInfo
		subprocess_module.Popen = lambda *args, **kwargs: FakeProcess(self.ps_stdout or "")

		modules = {
			"Access8Math": access8math_pkg,
			"api": api_module,
			"ui": ui_module,
			"comtypes": comtypes_module,
			"comtypes.client": comtypes_client_module,
			"subprocess": subprocess_module,
		}

		self._patcher = mock.patch.dict(sys.modules, modules)
		self._patcher.start()

		self._translation_patcher = mock.patch.object(importlib.import_module("builtins"), "_", lambda text: text, create=True)
		self._translation_patcher.start()

		if PLUGIN_ROOT not in sys.path:
			sys.path.insert(0, PLUGIN_ROOT)
		for name in list(sys.modules):
			if name == "Access8Math.lib.explorer" or name.startswith("Access8Math.lib.explorer."):
				sys.modules.pop(name, None)

		self.explorer = importlib.import_module("Access8Math.lib.explorer")
		self.explorer._shell = None
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		for name in list(sys.modules):
			if name == "Access8Math.lib.explorer" or name.startswith("Access8Math.lib.explorer."):
				sys.modules.pop(name, None)
		if self._patcher:
			self._patcher.stop()
		if getattr(self, "_translation_patcher", None):
			self._translation_patcher.stop()


class TestExplorerStorage(unittest.TestCase):
	def test_is_explorer_matches_foreground_objects_with_explorer_app_name(self):
		with ExplorerImportHarness(foreground=FakeConfigObject(app_name="explorer")) as harness:
			self.assertTrue(harness.explorer.is_explorer())

	def test_get_selected_file_explorer_returns_focused_item_path_from_com_shell(self):
		window = types.SimpleNamespace(
			hwnd=101,
			Document=types.SimpleNamespace(
				FocusedItem=types.SimpleNamespace(path=r"C:\Users\alice\Desktop\report.txt")
			),
		)
		with ExplorerImportHarness(
			foreground=FakeConfigObject(app_name="explorer", window_handle=101),
			com_windows=[window],
		) as harness:
			self.assertEqual(
				harness.explorer.get_selected_file_explorer(),
				r"C:\Users\alice\Desktop\report.txt",
			)

	def test_get_selected_file_explorer_uses_powershell_fallback_when_com_fails(self):
		with ExplorerImportHarness(
			foreground=FakeConfigObject(app_name="explorer", window_handle=303),
			com_error=True,
			ps_stdout="303:C:\\Users\\alice\\Downloads\\report.txt\n",
		) as harness:
			self.assertEqual(
				harness.explorer.get_selected_file_explorer(),
				r"C:\Users\alice\Downloads\report.txt",
			)

	def test_get_selected_file_explorer_uses_desktop_fallback_when_window_is_missing(self):
		window = types.SimpleNamespace(
			hwnd=404,
			Document=types.SimpleNamespace(
				FocusedItem=types.SimpleNamespace(path=r"C:\Users\alice\Desktop\not-used.txt")
			),
		)
		with mock.patch.dict(os.environ, {"USERPROFILE": r"C:\Users\alice"}, clear=False):
			with ExplorerImportHarness(
				foreground=FakeConfigObject(app_name="explorer", window_handle=505),
				com_error=True,
				ps_stdout="404:C:\\Users\\alice\\Desktop\\not-used.txt\n",
				desktop_name="notes.txt",
			) as harness:
				self.assertTrue(
					harness.explorer.get_selected_file_explorer().endswith(r"Desktop\notes.txt")
				)

	def test_get_selected_file_delegates_to_explorer_only_logic(self):
		with ExplorerImportHarness() as harness:
			explorer_module = harness.explorer
			explorer_module.get_selected_file_explorer = mock.Mock(return_value=False)

			self.assertFalse(explorer_module.get_selected_file(harness.foreground))
			explorer_module.get_selected_file_explorer.assert_called_once_with(harness.foreground)
