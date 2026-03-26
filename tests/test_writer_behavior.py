import importlib
import os
import sys
import tempfile
import types
import unittest
import builtins
from unittest import mock


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLUGIN_PARENT = os.path.join(PROJECT_ROOT, "addon", "globalPlugins")
PLUGIN_ROOT = os.path.join(PROJECT_ROOT, "addon", "globalPlugins", "Access8Math")


class FakeTextInfo:
	def __init__(self, text="", start=0, end=None):
		self.text = text
		self._startOffset = start
		self._endOffset = start if end is None else end
		self.update_caret_calls = 0
		self.update_selection_calls = 0

	def updateCaret(self):
		self.update_caret_calls += 1

	def updateSelection(self):
		self.update_selection_calls += 1


class FakeFocusObject:
	def __init__(self, text, caret_start=0, caret_end=None):
		self._all_text = FakeTextInfo(text=text, start=0, end=len(text))
		self._caret = FakeTextInfo(text=text, start=caret_start, end=caret_end)
		self.gain_focus_calls = 0

	def makeTextInfo(self, position):
		if position == "caret":
			return self._caret
		if position == "all":
			return self._all_text
		raise AssertionError(f"unexpected position: {position!r}")

	def event_gainFocus(self):
		self.gain_focus_calls += 1


class FakeGesture:
	def __init__(self, main_key, modifiers=None):
		self.mainKeyName = main_key
		self.modifierNames = tuple(modifiers or [])
		self.sent = False

	def send(self):
		self.sent = True


class WriterImportHarness:
	def __init__(self, *, focus_object=None, points=None, settings_override=None, view_data=None):
		self.focus_object = focus_object or FakeFocusObject("plain text")
		self.points = list(points or [])
		self.settings_override = dict(settings_override or {})
		self.view_data = dict(view_data or {})
		self.messages = []
		self.spoken = []
		self.braille_output = []
		self.interactions = []
		self.clipboard = ""
		self.played_waves = []
		self.keyboard_sends = []
		self.latex_calls = []
		self.asciimath_calls = []
		self.nemeth_calls = []
		self.beeps = []
		self.parser_delimiters = []
		self.parser_inputs = []
		self.command_view_events = []
		self.document_calls = []
		self.writer = None
		self._patcher = None
		self._tempdir = None

	def __enter__(self):
		access8math_pkg = types.ModuleType("Access8Math")
		access8math_pkg.__path__ = [PLUGIN_ROOT]

		addon_handler = types.ModuleType("addonHandler")
		addon_handler.initTranslation = lambda: None
		addon_handler.getCodeAddon = lambda: types.SimpleNamespace(manifest={"summary": "Access8Math"})

		api_module = types.ModuleType("api")
		api_module.getFocusObject = lambda: self.focus_object
		api_module.getForegroundObject = lambda: types.SimpleNamespace(
			name="Writer Document",
			appModule=types.SimpleNamespace(appName="writer-app"),
		)
		api_module.copyToClip = lambda value: setattr(self, "clipboard", value)
		api_module.getClipData = lambda: self.clipboard

		braille_module = types.ModuleType("braille")
		braille_module.TextRegion = lambda text: {"text": text}

		config_module = types.ModuleType("config")
		settings = {
			"command_mode": False,
			"navigate_mode": False,
			"shortcut_mode": False,
			"LaTeX_delimiter": "bracket",
			"Nemeth_delimiter": "at",
			"writeNavAcrossLine": False,
			"writeNavAudioIndication": False,
		}
		settings.update(self.settings_override)
		config_module.conf = {
			"Access8Math": {
				"settings": settings,
			},
		}

		keyboard_handler = types.ModuleType("keyboardHandler")

		class FakeKeyboardInputGesture:
			@classmethod
			def fromName(cls, name):
				return types.SimpleNamespace(send=lambda: self.keyboard_sends.append(name))

		keyboard_handler.KeyboardInputGesture = FakeKeyboardInputGesture

		nvda_objects = types.ModuleType("NVDAObjects")

		class FakeNVDAObject:
			def __init__(self, *args, **kwargs):
				self._gestureMap = {}

			def initOverlayClass(self):
				pass

			def event_gainFocus(self):
				pass

			def event_loseFocus(self):
				pass

			def event_caret(self):
				pass

			def bindGesture(self, key, script_name):
				self._gestureMap[key] = script_name

			def removeGestureBinding(self, key):
				self._gestureMap.pop(key)

			def makeTextInfo(self, position):
				return self_harness.focus_object.makeTextInfo(position)

		self_harness = self
		nvda_objects.NVDAObject = FakeNVDAObject

		math_pres = types.ModuleType("mathPres")
		math_pres.interactionProvider = types.SimpleNamespace(
			interactWithMathMl=lambda mathml: self.interactions.append(mathml)
		)
		math_pres.speechProvider = types.SimpleNamespace(
			getSpeechForMathMl=lambda mathml: [f"speech:{mathml}"],
			getBrailleForMathMl=lambda mathml: [f"braille:{mathml}"],
		)

		nvwave_module = types.ModuleType("nvwave")
		nvwave_module.playWaveFile = lambda path: self.played_waves.append(path)

		script_handler = types.ModuleType("scriptHandler")
		script_handler.script = lambda *args, **kwargs: (lambda func: func)

		speech_module = types.ModuleType("speech")
		speech_module.speak = lambda text: self.spoken.append(text)

		text_infos = types.ModuleType("textInfos")
		text_infos.POSITION_CARET = "caret"
		text_infos.POSITION_ALL = "all"

		tones_module = types.ModuleType("tones")
		tones_module.beep = lambda freq, duration: self.beeps.append((freq, duration))

		ui_module = types.ModuleType("ui")
		ui_module.message = lambda message: self.messages.append(message)

		input_core = types.ModuleType("inputCore")
		input_core.normalizeGestureIdentifier = lambda key: key

		command_modules = {}
		for module_name, class_name in {
			"Access8Math.command.latex": "A8MLaTeXCommandView",
			"Access8Math.command.mark": "A8MMarkCommandView",
			"Access8Math.command.review": "A8MHTMLCommandView",
			"Access8Math.command.translate": "A8MTranslateCommandView",
			"Access8Math.command.batch": "A8MBatchCommandView",
			"Access8Math.command.autocomplete": "A8MAutocompleteCommandView",
		}.items():
			module = types.ModuleType(module_name)
			module.__dict__[class_name] = self._build_command_view(class_name)
			command_modules[module_name] = module

		delimiter_module = types.ModuleType("Access8Math.delimiter")
		delimiter_module.LaTeX = {
			"bracket": {"start": r"\(", "end": r"\)", "type": "latex"},
		}
		delimiter_module.AsciiMath = {
			"graveaccent": {"start": "`", "end": "`", "type": "asciimath"},
		}
		delimiter_module.Nemeth = {
			"at": {"start": "@", "end": "@", "type": "nemeth"},
		}

		lib_braille = types.ModuleType("Access8Math.lib.braille")
		lib_braille.display_braille = lambda region: self.braille_output.append(region)

		lib_math_process = types.ModuleType("Access8Math.lib.mathProcess")
		lib_math_process.textmath2laObjFactory = self._textmath2la_obj_factory
		lib_math_process.latex2mathml = self._latex_to_mathml
		lib_math_process.asciimath2mathml = self._asciimath_to_mathml
		lib_math_process.nemeth2latex = self._nemeth_to_latex

		lib_viewhtml = types.ModuleType("Access8Math.lib.viewHTML")
		lib_viewhtml.Access8MathDocument = self._access8math_document

		modules = {
			"Access8Math": access8math_pkg,
			"addonHandler": addon_handler,
			"api": api_module,
			"braille": braille_module,
			"config": config_module,
			"keyboardHandler": keyboard_handler,
			"NVDAObjects": nvda_objects,
			"mathPres": math_pres,
			"nvwave": nvwave_module,
			"scriptHandler": script_handler,
			"speech": speech_module,
			"textInfos": text_infos,
			"tones": tones_module,
			"ui": ui_module,
			"inputCore": input_core,
			"Access8Math.delimiter": delimiter_module,
			"Access8Math.lib.braille": lib_braille,
			"Access8Math.lib.mathProcess": lib_math_process,
			"Access8Math.lib.viewHTML": lib_viewhtml,
		}
		modules.update(command_modules)

		self._patcher = mock.patch.dict(sys.modules, modules)
		self._patcher.start()
		self._translation_patcher = mock.patch.object(builtins, "_", lambda text: text, create=True)
		self._translation_patcher.start()

		if PLUGIN_PARENT not in sys.path:
			sys.path.insert(0, PLUGIN_PARENT)
		for name in list(sys.modules):
			if name == "Access8Math.writer" or name.startswith("Access8Math.writer."):
				sys.modules.pop(name, None)

		self.writer = importlib.import_module("Access8Math.writer")
		self.writer._ = lambda text: text
		self.writer.WindowsError = OSError
		self._tempdir = tempfile.TemporaryDirectory()
		if "Access8Math.writer.actions" in sys.modules:
			sys.modules["Access8Math.writer.actions"].PATH = self._tempdir.name
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		for name in list(sys.modules):
			if name == "Access8Math.writer" or name.startswith("Access8Math.writer."):
				sys.modules.pop(name, None)
		if self._patcher:
			self._patcher.stop()
		if getattr(self, "_translation_patcher", None):
			self._translation_patcher.stop()
		if self._tempdir:
			self._tempdir.cleanup()

	def _build_command_view(self, class_name):
		harness = self

		class FakeCommandView:
			def __init__(self, *args, **kwargs):
				self.args = args
				self.kwargs = kwargs
				self.focused = False
				self.data = types.SimpleNamespace(
					shortcut={},
					greekAlphabet={},
					data=[],
				)
				harness.command_view_events.append({
					"class_name": class_name,
					"args": args,
					"kwargs": kwargs,
					"focused": False,
				})

			def setFocus(self):
				self.focused = True
				harness.command_view_events[-1]["focused"] = True
				return None

			def command(self, command_id):
				return command_id

			def greekAlphabetCommand(self, command_id):
				return command_id

		FakeCommandView.__name__ = class_name
		return FakeCommandView

	def _latex_to_mathml(self, data):
		self.latex_calls.append(data)
		return f"<latex>{data}</latex>"

	def _asciimath_to_mathml(self, data):
		self.asciimath_calls.append(data)
		return f"<ascii>{data}</ascii>"

	def _nemeth_to_latex(self, data):
		self.nemeth_calls.append(data)
		return f"nemeth:{data}"

	def _textmath2la_obj_factory(self, delimiter):
		self.parser_delimiters.append(dict(delimiter))

		def parse(text):
			self.parser_inputs.append(text)
			return [dict(point) for point in self.points]

		return parse

	def _access8math_document(self, path):
		record = {
			"path": path,
			"raw2review": 0,
		}
		self.document_calls.append(record)
		return types.SimpleNamespace(
			path=path,
			raw2review=lambda: record.__setitem__("raw2review", record["raw2review"] + 1),
		)


class TestWriterSectionManager(unittest.TestCase):
	def test_writer_is_package_backed_and_re_exports_section_manager(self):
		with WriterImportHarness() as harness:
			writer_session = importlib.import_module("Access8Math.writer.session")
			self.assertTrue(harness.writer.__file__.endswith(os.path.join("writer", "__init__.py")))
			self.assertIs(harness.writer.SectionManager, writer_session.SectionManager)
			self.assertEqual(writer_session.SectionManager.__module__, "Access8Math.writer.session")

	def test_writer_navigation_module_owns_section_manager_navigation_methods(self):
		with WriterImportHarness() as harness:
			importlib.import_module("Access8Math.writer.navigation")
			for method_name in ["move", "moveLine", "start", "end", "startMargin", "endMargin"]:
				with self.subTest(method=method_name):
					self.assertEqual(
						getattr(harness.writer.SectionManager, method_name).__module__,
						"Access8Math.writer.navigation",
					)

	def test_section_manager_supports_command_selection_predicates_and_margin_moves(self):
		points = [
			{"start": 0, "end": 13, "type": "latex", "raw": r"\(\frac{x}\)", "data": r"\frac{x}", "index": 0, "line": 0},
		]
		with WriterImportHarness(
			focus_object=FakeFocusObject(r"\(\frac{x}\)", caret_start=4, caret_end=4),
			points=points,
		) as harness:
			manager = harness.writer.SectionManager()
			with manager:
				self.assertFalse(manager.inText)
				self.assertFalse(manager.inAsciiMath)
				self.assertFalse(manager.inNemeth)
				self.assertFalse(manager.inMathML)

				manager.commandSelection()
				self.assertEqual(manager.caret._startOffset, 2)
				self.assertEqual(manager.caret._endOffset, 7)
				self.assertEqual(manager.caret.update_selection_calls, 1)

				manager.startMargin()
				self.assertEqual(manager.caret._startOffset, 0)
				manager.endMargin()
				self.assertEqual(manager.caret._startOffset, 13)

	def test_section_manager_passes_delimiter_config_to_parser_and_drops_parser_indexes(self):
		points = [
			{"start": 0, "end": 0, "type": "text", "raw": "", "data": "", "index": 0, "line": 0},
			{"start": 0, "end": 3, "type": "text", "raw": "A ", "data": "A ", "index": 1, "line": 0},
			{"start": 3, "end": 6, "type": "nemeth", "raw": "@x@", "data": "x", "index": 2, "line": 0},
		]
		with WriterImportHarness(
			focus_object=FakeFocusObject("A @x@", caret_start=4, caret_end=4),
			points=points,
		) as harness:
			manager = harness.writer.SectionManager()
			with manager:
				self.assertEqual(
					harness.parser_delimiters[-1],
					{
						"latex": "bracket",
						"asciimath": "graveaccent",
						"nemeth": "at",
					},
				)
				self.assertEqual(harness.parser_inputs[-1], "A @x@")
				self.assertEqual(len(manager.points), 2)
				self.assertTrue(all("index" not in point for point in manager.points))
				self.assertEqual(manager.pointer["type"], "nemeth")

	def test_section_manager_detects_sections_and_current_command_token(self):
		text = "start \\(\\frac{x}{y}\\) tail"
		points = [
			{"start": 0, "end": 6, "type": "text", "raw": "start ", "data": "start ", "index": 0, "line": 0},
			{"start": 6, "end": 21, "type": "latex", "raw": r"\(\frac{x}{y}\)", "data": r"\frac{x}{y}", "index": 1, "line": 0},
			{"start": 21, "end": 26, "type": "text", "raw": " tail", "data": " tail", "index": 2, "line": 0},
		]
		caret_start = 10
		with WriterImportHarness(
			focus_object=FakeFocusObject(text, caret_start=caret_start, caret_end=caret_start),
			points=points,
		) as harness:
			manager = harness.writer.SectionManager()
			with manager:
				self.assertEqual(manager.section_index, 1)
				self.assertEqual(manager.pointer["type"], "latex")
				self.assertTrue(manager.inSection)
				self.assertTrue(manager.inMath)
				self.assertTrue(manager.inLaTeX)
				self.assertEqual(manager.delimiter["start"], r"\(")
				self.assertEqual(
					manager.command,
					{"all": r"\frac", "front": r"\f", "back": "rac"},
				)

	def test_section_manager_move_and_line_navigation_preserve_current_ranges(self):
		text = "A `x`\nB `y`\nC"
		points = [
			{"start": 0, "end": 2, "type": "text", "raw": "A ", "data": "A ", "index": 0, "line": 0},
			{"start": 2, "end": 5, "type": "asciimath", "raw": "`x`", "data": "x", "index": 1, "line": 0},
			{"start": 5, "end": 8, "type": "text", "raw": "\nB ", "data": "\nB ", "index": 2, "line": 1},
			{"start": 8, "end": 11, "type": "asciimath", "raw": "`y`", "data": "y", "index": 3, "line": 1},
			{"start": 11, "end": 13, "type": "text", "raw": "\nC", "data": "\nC", "index": 4, "line": 2},
		]
		with WriterImportHarness(
			focus_object=FakeFocusObject(text, caret_start=3, caret_end=3),
			points=points,
		) as harness:
			manager = harness.writer.SectionManager()
			with manager:
				next_text = manager.move(step=1, type_="text")
				self.assertEqual(next_text["data"], "\nB ")
				self.assertEqual(manager.caret._startOffset, 5)
				self.assertEqual(manager.caret._endOffset, 8)

				line_group = manager.moveLine(step=0)
				self.assertEqual([item["data"] for item in line_group], ["\nB ", "y"])
				self.assertEqual(manager.caret._startOffset, 5)
				self.assertEqual(manager.caret._endOffset, 11)

				line_end = manager.moveLine(step=0, type="end")
				self.assertEqual([item["data"] for item in line_end], ["y"])
				self.assertEqual(manager.caret._startOffset, 8)
				self.assertEqual(manager.caret._endOffset, 11)


class TestWriterActions(unittest.TestCase):
	def test_writer_actions_module_owns_writer_action_methods(self):
		with WriterImportHarness() as harness:
			importlib.import_module("Access8Math.writer.actions")
			for method_name in ["script_view_math", "script_interact", "displayBlocks"]:
				with self.subTest(method=method_name):
					self.assertEqual(
						getattr(harness.writer.TextMathEditField, method_name).__module__,
						"Access8Math.writer.actions",
					)

	def test_writer_routing_module_owns_routing_methods(self):
		with WriterImportHarness() as harness:
			importlib.import_module("Access8Math.writer.routing")
			for method_name in [
				"script_writeNav",
				"script_navigate",
				"script_navigateLine",
				"script_navigateCopy",
				"script_navigatePaste",
				"script_navigateCut",
				"script_navigateDelete",
			]:
				with self.subTest(method=method_name):
					self.assertEqual(
						getattr(harness.writer.TextMathEditField, method_name).__module__,
						"Access8Math.writer.routing",
					)

	def test_writer_gestures_module_owns_gesture_binding_helpers(self):
		with WriterImportHarness() as harness:
			importlib.import_module("Access8Math.writer.gestures")
			for method_name in [
				"bindCommandGestures",
				"unbindCommandGestures",
				"bindNavigateGestures",
				"unbindNavigateGestures",
				"bindShortcutGestures",
				"unbindShortcutGestures",
				"bindGreekAlphabetGestures",
				"unbindGreekAlphabetGestures",
				"bindWriteNavGestures",
				"unbindWriteNavGestures",
				"gesture_not_concurrent",
			]:
				with self.subTest(method=method_name):
					self.assertEqual(
						getattr(harness.writer.TextMathEditField, method_name).__module__,
						"Access8Math.writer.gestures",
					)

	def test_script_mark_latex_command_translate_autocomplete_and_batch_entrypoints(self):
		points = [
			{"start": 0, "end": 10, "type": "latex", "raw": r"\(\alpha\)", "data": r"\alpha", "index": 0, "line": 0},
		]
		with WriterImportHarness(
			focus_object=FakeFocusObject(r"\(\alpha\)", caret_start=4, caret_end=4),
			points=points,
			view_data={
				"A8MAutocompleteCommandView": {"data": ["alpha"]},
			},
		) as harness:
			field = harness.writer.TextMathEditField()
			field.section_manager = harness.writer.SectionManager()

			field.script_latex_command(FakeGesture("l", modifiers=["alt"]))
			field.script_translate(FakeGesture("t", modifiers=["alt"]))
			field.script_autocomplete(FakeGesture("upArrow", modifiers=["alt"]))
			field.script_batch(FakeGesture("b", modifiers=["alt"]))
			field.script_mark(FakeGesture("m", modifiers=["alt"]))

			self.assertEqual(
				[event["class_name"] for event in harness.command_view_events],
				[
					"A8MLaTeXCommandView",
					"A8MTranslateCommandView",
					"A8MAutocompleteCommandView",
					"A8MBatchCommandView",
				],
			)
			self.assertEqual(harness.messages[-1], "In math section. Please leave math section first and try again.")

	def test_script_mark_latex_command_translate_and_autocomplete_reject_invalid_contexts(self):
		points = [
			{"start": 0, "end": 14, "type": "mathml", "raw": "<math>x</math>", "data": "<math>x</math>", "index": 0, "line": 0},
		]
		with WriterImportHarness(
			focus_object=FakeFocusObject("<math>x</math>", caret_start=1, caret_end=1),
			points=points,
		) as harness:
			field = harness.writer.TextMathEditField()
			field.section_manager = harness.writer.SectionManager()

			field.script_mark(FakeGesture("m", modifiers=["alt"]))
			field.script_latex_command(FakeGesture("l", modifiers=["alt"]))
			field.script_translate(FakeGesture("t", modifiers=["alt"]))
			field.script_autocomplete(FakeGesture("upArrow", modifiers=["alt"]))

			self.assertEqual(
				harness.messages,
				[
					"In math section. Please leave math section first and try again.",
					"Not in LaTeX block or text block. cannot use LaTeX command",
					"This block cannot be translated",
					"No autocomplete found",
				],
			)
			self.assertEqual(harness.command_view_events, [])

	def test_script_view_math_exports_document_and_focuses_review_view(self):
		with WriterImportHarness(focus_object=FakeFocusObject("alpha\nbeta")) as harness:
			field = harness.writer.TextMathEditField()
			field.script_view_math(FakeGesture("h", modifiers=["alt"]))

			self.assertEqual(harness.document_calls[-1]["raw2review"], 1)
			self.assertTrue(harness.document_calls[-1]["path"].endswith(os.path.join("Writer Document.txt")))
			self.assertEqual(harness.command_view_events[-1]["class_name"], "A8MHTMLCommandView")
			self.assertTrue(harness.command_view_events[-1]["focused"])

	def test_script_interact_converts_latex_before_invoking_math_interaction(self):
		points = [
			{"start": 0, "end": 5, "type": "latex", "raw": r"\(x\)", "data": "x", "index": 0, "line": 0},
		]
		with WriterImportHarness(
			focus_object=FakeFocusObject(r"\(x\)", caret_start=2, caret_end=2),
			points=points,
		) as harness:
			field = harness.writer.TextMathEditField()
			field.section_manager = harness.writer.SectionManager()

			field.script_interact(FakeGesture("enter"))

			self.assertEqual(harness.latex_calls, ["x"])
			self.assertEqual(harness.interactions, ["<latex>x</latex>"])
			self.assertEqual(harness.messages, [])

	def test_script_interact_handles_other_math_types_and_non_math_blocks(self):
		cases = [
			(
				"asciimath",
				{"start": 0, "end": 3, "type": "asciimath", "raw": "`x`", "data": "x", "index": 0, "line": 0},
				"<ascii>x</ascii>",
				[],
				["x"],
				[],
			),
			(
				"nemeth",
				{"start": 0, "end": 3, "type": "nemeth", "raw": "@x@", "data": "x", "index": 0, "line": 0},
				"<latex>nemeth:x</latex>",
				["nemeth:x"],
				[],
				["x"],
			),
			(
				"mathml",
				{"start": 0, "end": 14, "type": "mathml", "raw": "<math>x</math>", "data": "<math>x</math>", "index": 0, "line": 0},
				"<math>x</math>",
				[],
				[],
				[],
			),
		]
		for type_name, point, expected_mathml, expected_latex_calls, expected_asciimath_calls, expected_nemeth_calls in cases:
			with self.subTest(type_name=type_name):
				with WriterImportHarness(
					focus_object=FakeFocusObject(point["raw"], caret_start=1, caret_end=1),
					points=[point],
				) as harness:
					field = harness.writer.TextMathEditField()
					field.section_manager = harness.writer.SectionManager()

					field.script_interact(FakeGesture("enter"))

					self.assertEqual(harness.interactions, [expected_mathml])
					self.assertEqual(harness.latex_calls, expected_latex_calls)
					self.assertEqual(harness.asciimath_calls, expected_asciimath_calls)
					self.assertEqual(harness.nemeth_calls, expected_nemeth_calls)

		with WriterImportHarness(
			focus_object=FakeFocusObject("plain", caret_start=1, caret_end=1),
			points=[{"start": 0, "end": 5, "type": "text", "raw": "plain", "data": "plain", "index": 0, "line": 0}],
		) as harness:
			field = harness.writer.TextMathEditField()
			field.section_manager = harness.writer.SectionManager()

			field.script_interact(FakeGesture("enter"))

			self.assertEqual(harness.interactions, [])
			self.assertEqual(harness.messages, ["This block cannot be interacted"])

	def test_display_blocks_speaks_math_in_view_mode_and_raw_text_in_raw_mode(self):
		with WriterImportHarness() as harness:
			field = harness.writer.TextMathEditField()

			field.displayBlocks([{"type": "latex", "data": "x+1", "raw": r"\(x+1\)"}], "view")
			field.displayBlocks([{"type": "latex", "data": "x+1", "raw": r"\(x+1\)"}], "raw")

			self.assertEqual(harness.latex_calls, ["x+1"])
			self.assertEqual(harness.spoken[0], ["speech:<latex>x+1</latex>"])
			self.assertEqual(harness.spoken[1], ["x+1"])
			self.assertEqual(harness.braille_output[0], [{"text": "⠀braille:<latex>x+1</latex>⠀"}])
			self.assertEqual(harness.braille_output[1], [{"text": "x+1"}])

	def test_display_blocks_supports_asciimath_nemeth_and_mathml_view_mode(self):
		with WriterImportHarness() as harness:
			field = harness.writer.TextMathEditField()

			field.displayBlocks(
				[
					{"type": "asciimath", "data": "x", "raw": "`x`"},
					{"type": "nemeth", "data": "y", "raw": "@y@"},
					{"type": "mathml", "data": "<math>z</math>", "raw": "<math>z</math>"},
				],
				"view",
			)

			self.assertEqual(harness.asciimath_calls, ["x"])
			self.assertEqual(harness.nemeth_calls, ["y"])
			self.assertEqual(harness.latex_calls, ["nemeth:y"])
			self.assertEqual(
				harness.spoken[-1],
				[
					"speech:<ascii>x</ascii>",
					"speech:<latex>nemeth:y</latex>",
					"speech:<math>z</math>",
				],
			)

	def test_script_navigate_selects_previous_block_without_crossing_lines(self):
		points = [
			{"start": 0, "end": 1, "type": "text", "raw": "A", "data": "A", "index": 0, "line": 0},
			{"start": 1, "end": 4, "type": "asciimath", "raw": "`x`", "data": "x", "index": 1, "line": 0},
			{"start": 4, "end": 6, "type": "text", "raw": "\nB", "data": "\nB", "index": 2, "line": 1},
		]
		with WriterImportHarness(
			focus_object=FakeFocusObject("A`x`\nB", caret_start=2, caret_end=2),
			points=points,
		) as harness:
			field = harness.writer.TextMathEditField()
			field.section_manager = harness.writer.SectionManager()

			field.script_navigate(FakeGesture("leftArrow"))

			self.assertEqual(harness.spoken[-1], ["A"])
			self.assertEqual(harness.braille_output[-1], [{"text": "A"}])

	def test_script_navigate_line_selection_and_boundary_fallback(self):
		points = [
			{"start": 0, "end": 2, "type": "text", "raw": "A ", "data": "A ", "index": 0, "line": 0},
			{"start": 2, "end": 5, "type": "asciimath", "raw": "`x`", "data": "x", "index": 1, "line": 0},
			{"start": 5, "end": 8, "type": "text", "raw": "\nB ", "data": "\nB ", "index": 2, "line": 1},
			{"start": 8, "end": 11, "type": "latex", "raw": r"\(y\)", "data": "y", "index": 3, "line": 1},
		]
		with WriterImportHarness(
			focus_object=FakeFocusObject("A `x`\nB \\(y\\)", caret_start=3, caret_end=3),
			points=points,
		) as harness:
			field = harness.writer.TextMathEditField()
			field.section_manager = harness.writer.SectionManager()

			field.script_navigateLine(FakeGesture("end", modifiers=["shift"]))

			self.assertEqual(harness.focus_object._caret.update_selection_calls, 1)
			self.assertEqual(harness.spoken, [])

			field.script_navigateLine(FakeGesture("pageUp"))

			self.assertEqual(harness.beeps[-1], (100, 50))
			self.assertEqual(harness.spoken[-1], ["A ", "speech:<ascii>x</ascii>"])

	def test_script_write_nav_dispatches_navigation_and_edit_actions(self):
		with WriterImportHarness() as harness:
			field = harness.writer.TextMathEditField()
			calls = []
			field.script_interact = lambda gesture: calls.append(("interact", gesture.mainKeyName))
			field.script_navigateLine = lambda gesture: calls.append(("navigateLine", gesture.mainKeyName))
			field.script_navigateCopy = lambda gesture: calls.append(("copy", gesture.mainKeyName))
			field.script_navigatePaste = lambda gesture: calls.append(("paste", gesture.mainKeyName))
			field.script_navigateCut = lambda gesture: calls.append(("cut", gesture.mainKeyName))
			field.script_translate = lambda gesture: calls.append(("translate", gesture.mainKeyName))
			field.script_navigateDelete = lambda gesture: calls.append(("delete", gesture.mainKeyName))
			field.script_navigate = lambda gesture: calls.append(("navigate", gesture.mainKeyName))

			field.script_writeNav(FakeGesture("enter"))
			field.script_writeNav(FakeGesture("downArrow"))
			field.script_writeNav(FakeGesture("c", modifiers=["control"]))
			field.script_writeNav(FakeGesture("v", modifiers=["control"]))
			field.script_writeNav(FakeGesture("x", modifiers=["control"]))
			field.script_writeNav(FakeGesture("t", modifiers=["control"]))
			field.script_writeNav(FakeGesture("delete"))
			field.script_writeNav(FakeGesture("a"))

			self.assertEqual(
				calls,
				[
					("interact", "enter"),
					("navigateLine", "downArrow"),
					("copy", "c"),
					("paste", "v"),
					("cut", "x"),
					("translate", "t"),
					("delete", "delete"),
					("navigate", "a"),
				],
			)

	def test_script_navigate_clipboard_and_delete_actions_operate_on_current_block(self):
		points = [
			{"start": 0, "end": 5, "type": "text", "raw": "plain", "data": "plain", "index": 0, "line": 0},
		]
		with WriterImportHarness(
			focus_object=FakeFocusObject("plain", caret_start=1, caret_end=1),
			points=points,
		) as harness:
			field = harness.writer.TextMathEditField()
			field.section_manager = harness.writer.SectionManager()
			harness.clipboard = "clip"

			field.script_navigateCopy(FakeGesture("c", modifiers=["control"]))
			field.script_navigatePaste(FakeGesture("v", modifiers=["control"]))
			field.script_navigateCut(FakeGesture("x", modifiers=["control"]))
			field.script_navigateDelete(FakeGesture("delete"))

			self.assertEqual(harness.clipboard, "plain")
			self.assertEqual(harness.keyboard_sends, ["control+v", "control+x", "delete"])
			self.assertEqual(harness.focus_object._caret.update_selection_calls, 2)
			self.assertEqual(
				harness.messages,
				[
					"plain copied to clipboard",
					"plain inserted to document",
					"plain cut from document",
					"plain deleted from document",
				],
			)

	def test_event_gain_focus_and_mode_toggles_bind_expected_gestures(self):
		with WriterImportHarness(
			settings_override={
				"command_mode": True,
				"navigate_mode": True,
				"shortcut_mode": True,
			},
		) as harness:
			field = harness.writer.TextMathEditField()

			field.event_gainFocus()
			self.assertIn("kb:alt+b", field._gestureMap)
			self.assertIn("kb:alt+leftArrow", field._gestureMap)
			self.assertIn("kb:f1", field._gestureMap)

			field.script_command_toggle(FakeGesture("c"))
			field.script_navigate_toggle(FakeGesture("n"))
			field.script_shortcut_toggle(FakeGesture("s"))
			field.script_greekAlphabet_toggle(FakeGesture("g"))

			self.assertEqual(
				harness.messages[-4:],
				[
					"Command gestures deactivated",
					"Block navigation gestures deactivated",
					"Shortcut gestures deactivated",
					"Greek alphabet gestures activated",
				],
			)

	def test_script_write_nav_toggle_and_exit_manage_focus_and_messages(self):
		points = [
			{"start": 0, "end": 5, "type": "text", "raw": "plain", "data": "plain", "index": 0, "line": 0},
		]
		with WriterImportHarness(
			focus_object=FakeFocusObject("plain", caret_start=1, caret_end=1),
			points=points,
		) as harness:
			field = harness.writer.TextMathEditField()
			field.section_manager = harness.writer.SectionManager()

			field.script_writeNav_toggle(FakeGesture("space"))
			self.assertTrue(field.writeNav_mode)
			self.assertEqual(harness.messages[-1], "Browse navigation mode on")
			self.assertEqual(harness.spoken[-1], ["plain"])

			field.script_writeNav_toggle(FakeGesture("space"))
			self.assertFalse(field.writeNav_mode)
			self.assertEqual(harness.messages[-1], "Browse navigation mode off")
			self.assertEqual(harness.focus_object.gain_focus_calls, 1)

			exit_gesture = FakeGesture("escape")
			field.script_writeNav_exit(exit_gesture)
			self.assertTrue(field.writeNav_mode)
			self.assertFalse(exit_gesture.sent)

			field.script_writeNav_exit(exit_gesture)
			self.assertTrue(exit_gesture.sent)

	def test_script_write_nav_toggle_uses_wave_files_when_audio_indication_enabled(self):
		points = [
			{"start": 0, "end": 5, "type": "text", "raw": "plain", "data": "plain", "index": 0, "line": 0},
		]
		with WriterImportHarness(
			focus_object=FakeFocusObject("plain", caret_start=1, caret_end=1),
			points=points,
			settings_override={"writeNavAudioIndication": True},
		) as harness:
			field = harness.writer.TextMathEditField()
			field.section_manager = harness.writer.SectionManager()

			field.script_writeNav_toggle(FakeGesture("space"))
			field.script_writeNav_toggle(FakeGesture("space"))

			self.assertEqual(
				harness.played_waves,
				[
					os.path.join("waves", "browseMode.wav"),
					os.path.join("waves", "focusMode.wav"),
				],
			)


if __name__ == "__main__":
	unittest.main()
