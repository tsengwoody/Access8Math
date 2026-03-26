# coding=utf-8

import os

import addonHandler
import api
import config
from NVDAObjects import NVDAObject
import nvwave
from scriptHandler import script
import ui

from ..command.latex import A8MLaTeXCommandView
from ..command.mark import A8MMarkCommandView
from ..command.translate import A8MTranslateCommandView
from ..command.batch import A8MBatchCommandView
from ..command.autocomplete import A8MAutocompleteCommandView
from .actions import WriterActionsMixin
from .gestures import WriterGestureMixin
from .routing import WriterRoutingMixin
from .session import SectionManager

addonHandler.initTranslation()
ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

command_mode = config.conf["Access8Math"]["settings"]["command_mode"]
navigate_mode = config.conf["Access8Math"]["settings"]["navigate_mode"]
shortcut_mode = config.conf["Access8Math"]["settings"]["shortcut_mode"]
greekAlphabet_mode = False
writeNav_mode = False


class TextMathEditField(WriterActionsMixin, WriterRoutingMixin, WriterGestureMixin, NVDAObject):
	initial = True
	writeNav_mode = False
	_originGestureMap = {}

	def initOverlayClass(self):
		super().initOverlayClass()

	def event_gainFocus(self):
		self.section_manager = SectionManager()
		if self.initial:
			self._originGestureMap = self._gestureMap.copy()
			self.initial = False

		global command_mode, navigate_mode, shortcut_mode, greekAlphabet_mode
		try:
			if command_mode:
				self.bindCommandGestures()
			if navigate_mode:
				self.bindNavigateGestures()
			if shortcut_mode:
				self.bindShortcutGestures()
			if greekAlphabet_mode:
				self.bindGreekAlphabetGestures()
			if self.writeNav_mode:
				self.bindWriteNavGestures()
		except WindowsError:
			pass

		super().event_gainFocus()

	def event_loseFocus(self):
		super().event_loseFocus()

	def event_caret(self):
		super().event_caret()

	@script(
		gestures=["kb:nvda+alt+c"],
		description=_("Toggle command gestures"),
		category=ADDON_SUMMARY,
	)
	def script_command_toggle(self, gesture):
		global command_mode
		command_mode = not command_mode
		if command_mode:
			self.bindCommandGestures()
			ui.message(_("Command gestures activated"))
		else:
			self.unbindCommandGestures()
			ui.message(_("Command gestures deactivated"))

	@script(
		gestures=["kb:nvda+alt+n"],
		description=_("Toggle block navigation gestures"),
		category=ADDON_SUMMARY,
	)
	def script_navigate_toggle(self, gesture):
		global navigate_mode
		navigate_mode = not navigate_mode
		if navigate_mode:
			self.bindNavigateGestures()
			ui.message(_("Block navigation gestures activated"))
		else:
			self.unbindNavigateGestures()
			ui.message(_("Block navigation gestures deactivated"))

	@script(
		gestures=["kb:nvda+alt+s"],
		description=_("Toggle shortcut gestures"),
		category=ADDON_SUMMARY,
	)
	def script_shortcut_toggle(self, gesture):
		if self.writeNav_mode:
			ui.message(_("Cannot activate shortcut gesture in browse navigation mode"))
			return
		global shortcut_mode
		if not shortcut_mode:
			self.gesture_not_concurrent()
			shortcut_mode = not shortcut_mode
			self.bindShortcutGestures()
			ui.message(_("Shortcut gestures activated"))
		else:
			shortcut_mode = not shortcut_mode
			self.unbindShortcutGestures()
			ui.message(_("Shortcut gestures deactivated"))

	@script(
		gestures=["kb:nvda+alt+g"],
		description=_("Toggle Greek alphabet gesture"),
		category=ADDON_SUMMARY,
	)
	def script_greekAlphabet_toggle(self, gesture):
		if self.writeNav_mode:
			ui.message(_("Cannot activate Greek alphabet gestures in browse navigation mode"))
			return
		global greekAlphabet_mode
		if not greekAlphabet_mode:
			self.gesture_not_concurrent()
			greekAlphabet_mode = not greekAlphabet_mode
			self.bindGreekAlphabetGestures()
			ui.message(_("Greek alphabet gestures activated"))
		else:
			greekAlphabet_mode = not greekAlphabet_mode
			self.unbindGreekAlphabetGestures()
			ui.message(_("Greek alphabet gestures deactivated"))

	@script(
		gestures=["kb:NVDA+space"],
		description=_("Toggle browse navigation mode"),
		category=ADDON_SUMMARY,
	)
	def script_writeNav_toggle(self, gesture):
		self.writeNav_mode = not self.writeNav_mode
		if self.writeNav_mode:
			self.gesture_not_concurrent()
			self.bindWriteNavGestures()
			if config.conf["Access8Math"]["settings"]["writeNavAudioIndication"]:
				sound = "browseMode.wav"
				nvwave.playWaveFile(os.path.join("waves", sound))
			else:
				ui.message(_("Browse navigation mode on"))
			with self.section_manager as manager:
				result = manager.move(type_='any', step=0)
				self.displayBlocks([result], "view")
		else:
			self.unbindWriteNavGestures()
			if config.conf["Access8Math"]["settings"]["writeNavAudioIndication"]:
				sound = "focusMode.wav"
				nvwave.playWaveFile(os.path.join("waves", sound))
			else:
				ui.message(_("Browse navigation mode off"))
			api.getFocusObject().event_gainFocus()

	def script_writeNav_exit(self, gesture):
		if not self.writeNav_mode:
			self.writeNav_mode = not self.writeNav_mode
			self.bindWriteNavGestures()
			if config.conf["Access8Math"]["settings"]["writeNavAudioIndication"]:
				sound = "browseMode.wav"
				nvwave.playWaveFile(os.path.join("waves", sound))
			else:
				ui.message(_("Browse navigation mode on"))
		else:
			gesture.send()

	def script_shortcut(self, gesture):
		with self.section_manager as manager:
			if manager.inMath:
				view = A8MLaTeXCommandView(inSection=manager.inMath)
				slot = gesture.mainKeyName[1:] if len(gesture.mainKeyName) > 1 else gesture.mainKeyName
				if slot in view.data.shortcut:
					view.command(view.data.shortcut[slot]["id"])
				else:
					gesture.send()
			else:
				gesture.send()

	def script_shortcut_help(self, gesture):
		with self.section_manager as manager:
			if manager.inMath:
				view = A8MLaTeXCommandView(inSection=manager.inMath)
				slot = gesture.mainKeyName[1:] if len(gesture.mainKeyName) > 1 else gesture.mainKeyName
				if slot in view.data.shortcut:
					ui.message(view.data.shortcut[slot]["name"])
				else:
					gesture.send()
			else:
				gesture.send()

	def script_GreekAlphabet(self, gesture):
		with self.section_manager as manager:
			if manager.inMath:
				view = A8MLaTeXCommandView(inSection=manager.inMath)
				slot = gesture.mainKeyName
				if slot in view.data.greekAlphabet:
					view.greekAlphabetCommand(view.data.greekAlphabet[slot]["id"])
				else:
					ui.message(_("Greek alphabet {GreekAlphabet} is not set").format(
						GreekAlphabet=slot,
					))
			else:
				gesture.send()

	def script_mark(self, gesture):
		with self.section_manager as manager:
			if (manager.pointer and manager.pointer['type'] == 'text') or len(manager.points) == 0:
				view = A8MMarkCommandView(section=manager)
				view.setFocus()
			else:
				ui.message(_("In math section. Please leave math section first and try again."))

	def script_latex_command(self, gesture):
		with self.section_manager as manager:
			if manager.inLaTeX or manager.inText:
				A8MLaTeXCommandView(inSection=manager.inLaTeX).setFocus()
			else:
				ui.message(_("Not in LaTeX block or text block. cannot use LaTeX command"))

	def script_autocomplete(self, gesture):
		with self.section_manager as manager:
			command = manager.command["all"]
			if command:
				view = A8MAutocompleteCommandView(section=manager, command=command)
				if len(view.data.data) > 0:
					view.setFocus()
				else:
					ui.message(_("No autocomplete found"))
			else:
				ui.message(_("No autocomplete found"))

	def script_translate(self, gesture):
		with self.section_manager as manager:
			if manager.inLaTeX or manager.inAsciiMath or manager.inNemeth:
				A8MTranslateCommandView(section=manager).setFocus()
			else:
				ui.message(_("This block cannot be translated"))

	def script_batch(self, gesture):
		with self.section_manager as manager:
			A8MBatchCommandView(section=manager).setFocus()
