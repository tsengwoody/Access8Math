import os
import re

PATH = os.path.dirname(__file__)

import addonHandler
import api
import config
import globalVars
from keyboardHandler import KeyboardInputGesture
from NVDAObjects import NVDAObject
import nvwave
from scriptHandler import script
import speech
import textInfos
import tones
import ui

from command.latex import A8MLaTeXCommandView
from command.mark import A8MMarkCommandView
from command.review import A8MHTMLCommandView
from command.translate import A8MTranslateCommandView
from command.batch import A8MBatchCommandView
from delimiter import LaTeX as LaTeX_delimiter, AsciiMath as AsciiMath_delimiter
from lib.mathProcess import textmath2laObjFactory, latex2mathml, asciimath2mathml, latex2asciimath, asciimath2latex
from regularExpression import delimiterRegularExpression, latex_bracket_dollar


addonHandler.initTranslation()
ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

from jinja2 import Environment, FileSystemLoader
TEMPLATES_PATH = os.path.join(PATH, 'web', 'templates')
env = Environment(loader=FileSystemLoader(TEMPLATES_PATH), variable_start_string='{|{', variable_end_string='}|}')

command_mode = config.conf["Access8Math"]["settings"]["command_mode"]
navigate_mode = config.conf["Access8Math"]["settings"]["navigate_mode"]
shortcut_mode = config.conf["Access8Math"]["settings"]["shortcut_mode"]
greekAlphabet_mode = False
writeNav_mode = False


class TextMathEditField(NVDAObject):
	initial = True
	shortcut_mode = False
	greekAlphabet_mode = False
	writeNav_mode = False
	_originGestureMap = {}

	def event_gainFocus(self):
		if self.initial:
			self._originGestureMap = self._gestureMap.copy()
			self.initial = False

		global command_mode, navigate_mode, shortcut_mode
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

	def bindCommandGestures(self):
		self.bindGesture("kb:alt+b", "batch")
		self.bindGesture("kb:alt+h", "view_math")
		self.bindGesture("kb:alt+i", "interact")
		self.bindGesture("kb:alt+l", "latex_command")
		self.bindGesture("kb:alt+m", "mark")
		self.bindGesture("kb:alt+t", "translate")

	def unbindCommandGestures(self):
		import inputCore
		for key in ["alt+b", "alt+h", "alt+i", "alt+l", "alt+m", "alt+t"]:
			key = "kb:{}".format(key)
			try:
				self.removeGestureBinding(key)
			except:
				pass

			key = inputCore.normalizeGestureIdentifier(key)
			if key in self._originGestureMap:
				self._gestureMap[key] = self._originGestureMap[key]

	def bindNavigateGestures(self):
		gestures = [
			"kb:alt+downArrow",
			"kb:alt+leftArrow",
			"kb:alt+rightArrow",
			"kb:alt+shift+downArrow",
			"kb:alt+shift+leftArrow",
			"kb:alt+shift+rightArrow",
			"kb:alt+home",
			"kb:alt+end",
		]
		for key in gestures:
			self.bindGesture(key, "navigate")

	def unbindNavigateGestures(self):
		import inputCore
		gestures = [
			"kb:alt+downArrow",
			"kb:alt+leftArrow",
			"kb:alt+rightArrow",
			"kb:alt+shift+downArrow",
			"kb:alt+shift+leftArrow",
			"kb:alt+shift+rightArrow",
			"kb:alt+home",
			"kb:alt+end",
		]
		for key in gestures:
			try:
				self.removeGestureBinding(key)
			except:
				pass

			key = inputCore.normalizeGestureIdentifier(key)
			if key in self._originGestureMap:
				self._gestureMap[key] = self._originGestureMap[key]

	def bindShortcutGestures(self):
		for i in range(1, 13):
			key = "kb:f{}".format(i)
			self.bindGesture(key, "shortcut")
			key = "kb:shift+f{}".format(i)
			self.bindGesture(key, "shortcut_help")

		for i in [c for c in "abcdefghijklmnopqrstuvwxyz"]:
			key = "kb:{}".format(i)
			self.bindGesture(key, "shortcut")
			key = "kb:shift+{}".format(i)
			self.bindGesture(key, "shortcut_help")

	def unbindShortcutGestures(self):
		import inputCore
		for i in range(1, 13):
			key = "kb:f{}".format(i)
			try:
				self.removeGestureBinding(key)
			except KeyError:
				pass
			key = inputCore.normalizeGestureIdentifier(key)
			if key in self._originGestureMap:
				self._gestureMap[key] = self._originGestureMap[key]

			key = "kb:shift+f{}".format(i)
			try:
				self.removeGestureBinding(key)
			except KeyError:
				pass
			key = inputCore.normalizeGestureIdentifier(key)
			if key in self._originGestureMap:
				self._gestureMap[key] = self._originGestureMap[key]

		for i in [c for c in "abcdefghijklmnopqrstuvwxyz"]:
			key = "kb:{}".format(i)
			try:
				self.removeGestureBinding(key)
			except KeyError:
				pass
			key = inputCore.normalizeGestureIdentifier(key)
			if key in self._originGestureMap:
				self._gestureMap[key] = self._originGestureMap[key]

			key = "kb:shift+{}".format(i)
			try:
				self.removeGestureBinding(key)
			except KeyError:
				pass
			key = inputCore.normalizeGestureIdentifier(key)
			if key in self._originGestureMap:
				self._gestureMap[key] = self._originGestureMap[key]

	def bindGreekAlphabetGestures(self):
		for i in [c for c in "abcdefghijklmnopqrstuvwxyz"]:
			key = "kb:{}".format(i)
			self.bindGesture(key, "GreekAlphabet")

	def unbindGreekAlphabetGestures(self):
		import inputCore
		for i in range(1, 13):
			key = "kb:f{}".format(i)
			try:
				self.removeGestureBinding(key)
			except KeyError:
				pass
			key = inputCore.normalizeGestureIdentifier(key)
			if key in self._originGestureMap:
				self._gestureMap[key] = self._originGestureMap[key]

	def bindWriteNavGestures(self):
		for c in [
			c for c in "abcdefghijklmnopqrstuvwxyz1234567890`-=[];',./\\"
		] + [
			"upArrow", "downArrow", "leftarrow", "rightarrow", "home", "end", "pageUp", "pageDown", "space", "enter", "delete", "backspace", "tab"
		] + [
			"control+c", "control+v", "control+x", "control+t",
		] + [
			"numLockNumpad{number}".format(number=i) for i in range(10)
		] + [
			"numpadPlus", "numpadMinus", "numpadMultiply", "numpadDivide", "numpadEnter", "numpadDecimal"
		] + [
			"numLockNumpadPlus", "numLockNumpadMinus", "numLockNumpadMultiply", "numLockNumpadDivide", "numpadDelete"
		]:
			key = "kb:{}".format(c)
			self.bindGesture(key, "writeNav")
			key = "kb:shift+{}".format(c)
			self.bindGesture(key, "writeNav")

	def unbindWriteNavGestures(self):
		import inputCore
		for c in [
			c for c in "abcdefghijklmnopqrstuvwxyz1234567890`-=[];',./\\"
		] + [
			"upArrow", "downArrow", "leftarrow", "rightarrow", "home", "end", "pageUp", "pageDown", "space", "enter", "control+c", "control+v", "control+x", "delete", "backspace", "tab"
		] + [
			"control+c", "control+v", "control+x", "control+t",
		] + [
			"numLockNumpad{number}".format(number=i) for i in range(10)
		] + [
			"numpadPlus", "numpadMinus", "numpadMultiply", "numpadDivide", "numpadEnter", "numpadDecimal"
		] + [
			"numLockNumpadPlus", "numLockNumpadMinus", "numLockNumpadMultiply", "numLockNumpadDivide", "numpadDelete"
		]:
			key = "kb:{}".format(c)
			try:
				self.removeGestureBinding(key)
			except KeyError:
				pass
			key = inputCore.normalizeGestureIdentifier(key)
			if key in self._originGestureMap:
				self._gestureMap[key] = self._originGestureMap[key]

			key = "kb:shift+{}".format(c)
			try:
				self.removeGestureBinding(key)
			except KeyError:
				pass
			key = inputCore.normalizeGestureIdentifier(key)
			if key in self._originGestureMap:
				self._gestureMap[key] = self._originGestureMap[key]

	def gesture_not_concurrent(self):
		global shortcut_mode
		if shortcut_mode:
			shortcut_mode = not shortcut_mode
			self.unbindShortcutGestures()
		global greekAlphabet_mode
		if greekAlphabet_mode:
			greekAlphabet_mode = not greekAlphabet_mode
			self.unbindGreekAlphabetGestures()

	@script(
		gestures=["kb:nvda+alt+c"],
		description=_("command gesture toggle"),
		category=ADDON_SUMMARY,
	)
	def script_command_toggle(self, gesture):
		global command_mode
		command_mode = not command_mode
		if command_mode:
			self.bindCommandGestures()
			ui.message(_("activate command gesture"))
		else:
			self.unbindCommandGestures()
			ui.message(_("deactivate command gesture"))

	@script(
		gestures=["kb:nvda+alt+n"],
		description=_("block navigate gesture toggle"),
		category=ADDON_SUMMARY,
	)
	def script_navigate_toggle(self, gesture):
		global navigate_mode
		navigate_mode = not navigate_mode
		if navigate_mode:
			self.bindNavigateGestures()
			ui.message(_("activate block navigate gesture"))
		else:
			self.unbindNavigateGestures()
			ui.message(_("deactivate block navigate gesture"))

	@script(
		gestures=["kb:nvda+alt+s"],
		description=_("shortcut gesture toggle"),
		category=ADDON_SUMMARY,
	)
	def script_shortcut_toggle(self, gesture):
		if self.writeNav_mode:
			ui.message(_("cannot activate shortcut gesture in write navigate mode"))
			return
		global shortcut_mode
		if not shortcut_mode:
			self.gesture_not_concurrent()
			shortcut_mode = not shortcut_mode
			self.bindShortcutGestures()
			ui.message(_("activate shortcut gesture"))
		else:
			shortcut_mode = not shortcut_mode
			self.unbindShortcutGestures()
			ui.message(_("deactivate shortcut gesture"))

	@script(
		gestures=["kb:nvda+alt+g"],
		description=_("greek alphabet gesture toggle"),
		category=ADDON_SUMMARY,
	)
	def script_greekAlphabet_toggle(self, gesture):
		if self.writeNav_mode:
			ui.message(_("cannot activate greek alphabet gesture in write navigate mode"))
			return
		global greekAlphabet_mode
		if not greekAlphabet_mode:
			self.gesture_not_concurrent()
			greekAlphabet_mode = not greekAlphabet_mode
			self.bindGreekAlphabetGestures()
			ui.message(_("activate greek alphabet gesture"))
		else:
			greekAlphabet_mode = not greekAlphabet_mode
			self.unbindGreekAlphabetGestures()
			ui.message(_("deactivate greek alphabet gesture"))

	@script(
		gestures=["kb:NVDA+space"],
		description=_("write navigate mode toggle"),
		category=ADDON_SUMMARY,
	)
	def script_writeNav_toggle(self, gesture):
		self.writeNav_mode = not self.writeNav_mode
		if self.writeNav_mode:
			self.gesture_not_concurrent()
			self.bindWriteNavGestures()
			if config.conf["Access8Math"]["settings"]["writeNavAudioIndication"]:
				sound = "browseMode.wav"
				nvwave.playWaveFile(os.path.join(globalVars.appDir, "waves", sound))
			else:
				ui.message(_("write navigation mode on"))
		else:
			self.unbindWriteNavGestures()
			if config.conf["Access8Math"]["settings"]["writeNavAudioIndication"]:
				sound = "focusMode.wav"
				nvwave.playWaveFile(os.path.join(globalVars.appDir, "waves", sound))
			else:
				ui.message(_("write navigation mode off"))

	def script_writeNav_exit(self, gesture):
		if not self.writeNav_mode:
			self.writeNav_mode = not self.writeNav_mode
			self.bindWriteNavGestures()
			if config.conf["Access8Math"]["settings"]["writeNavAudioIndication"]:
				sound = "browseMode.wav"
				nvwave.playWaveFile(os.path.join(globalVars.appDir, "waves", sound))
			else:
				ui.message(_("write navigation mode on"))
		else:
			gesture.send()

	def script_shortcut(self, gesture):
		with SectionManager() as manager:
			if manager.inMath:
				view = A8MLaTeXCommandView(selection=manager.selection.text, inSection=manager.inMath)
				slot = gesture.mainKeyName[1:] if len(gesture.mainKeyName) > 1 else gesture.mainKeyName
				if slot in view.data.shortcut:
					view.command(view.data.shortcut[slot]["id"])
				else:
					if True:
						gesture.send()
					else:
						ui.message(_("shortcut {shortcut} is not set").format(
							shortcut=slot,
						))
			else:
				gesture.send()

	def script_shortcut_help(self, gesture):
		with SectionManager() as manager:
			if manager.inMath:
				view = A8MLaTeXCommandView(selection=manager.selection.text, inSection=manager.inMath)
				slot = gesture.mainKeyName[1:]
				if slot in view.data.shortcut:
					ui.message(view.data.shortcut[slot]["name"])
				else:
					if True:
						gesture.send()
					else:
						ui.message(_("shortcut {shortcut} is not set").format(
							shortcut=slot,
						))
			else:
				gesture.send()

	def script_GreekAlphabet(self, gesture):
		with SectionManager() as manager:
			if manager.inMath:
				view = A8MLaTeXCommandView(selection=manager.selection.text, inSection=manager.inMath)
				slot = gesture.mainKeyName
				if slot in view.data.greekAlphabet:
					view.greekAlphabetCommand(view.data.greekAlphabet[slot]["id"])
				else:
					ui.message(_("GreekAlphabet {GreekAlphabet} is not set").format(
						GreekAlphabet=slot,
					))
			else:
				gesture.send()

	def script_writeNav(self, gesture):
		if gesture.mainKeyName in ["space", "enter", "numpadEnter"]:
			self.script_interact(gesture)
		elif gesture.mainKeyName in ["downArrow", "upArrow", "home", "end", "pageUp", "pageDown"]:
			self.script_navigateLine(gesture)
		elif gesture.mainKeyName == "c" and "control" in gesture.modifierNames:
			self.script_navigateCopy(gesture)
		elif gesture.mainKeyName == "v" and "control" in gesture.modifierNames:
			self.script_navigatePaste(gesture)
		elif gesture.mainKeyName == "x" and "control" in gesture.modifierNames:
			self.script_navigateCut(gesture)
		elif gesture.mainKeyName == "t" and "control" in gesture.modifierNames:
			self.script_translate(gesture)
		elif gesture.mainKeyName in ["delete", "backspace"]:
			self.script_navigateDelete(gesture)
		else:
			self.script_navigate(gesture)

	def script_view_math(self, gesture):
		document = self.makeTextInfo(textInfos.POSITION_ALL)
		html_file = text2template(document.text, os.path.join(PATH, 'web', 'review', 'index.html'))
		raw_file = os.path.join(PATH, 'web', 'review', 'raw.txt')
		with open(raw_file, "w", encoding="utf8", newline="") as f:
			f.write(document.text)
		A8MHTMLCommandView(file=html_file).setFocus()

	def script_mark(self, gesture):
		with SectionManager() as manager:
			if manager.pointer and manager.pointer['type'] == 'text':
				A8MMarkCommandView(section=manager).setFocus()
			else:
				ui.message(_("In math section. Please leave math section first and try again."))

	def script_latex_command(self, gesture):
		with SectionManager() as manager:
			if manager.inLaTeX or manager.inText:
				A8MLaTeXCommandView(selection=manager.selection.text, inSection=manager.inLaTeX).setFocus()
			else:
				ui.message(_("Not in LaTeX block or text block. cannot use LaTeX command"))

	def script_interact(self, gesture):
		with SectionManager() as manager:
			if manager.inMath:
				from mathPres import interactionProvider
				if manager.pointer['type'] == 'latex':
					mathMl = latex2mathml(manager.pointer['data'])
				elif manager.pointer['type'] == 'asciimath':
					mathMl = asciimath2mathml(manager.pointer['data'])
				elif manager.pointer['type'] == 'mathml':
					mathMl = manager.pointer['data']
				mathMl = mathMl.replace("<<", "&lt;<").replace(">>", ">&gt;")
				interactionProvider.interactWithMathMl(mathMl)
			else:
				ui.message(_("This block cannot be interacted"))

	def script_translate(self, gesture):
		with SectionManager() as manager:
			if manager.inLaTeX or manager.inAsciiMath:
				A8MTranslateCommandView(section=manager).setFocus()
			else:
				ui.message(_("This block cannot be translated"))

	def script_batch(self, gesture):
		with SectionManager() as manager:
			A8MBatchCommandView(section=manager).setFocus()

	def script_navigate(self, gesture):
		with SectionManager() as manager:
			selected = False
			if gesture.mainKeyName == "downArrow":
				result = manager.move(type='any', step=0)
				if "shift" in gesture.modifierNames:
					selected = True
			elif gesture.mainKeyName == "leftArrow":
				result = manager.move(type='any', step=-1)
				if "shift" in gesture.modifierNames:
					selected = True
			elif gesture.mainKeyName == "rightArrow":
				result = manager.move(type='any', step=1)
				if "shift" in gesture.modifierNames:
					selected = True
			elif gesture.mainKeyName == "tab":
				if "shift" in gesture.modifierNames:
					result = manager.move(type='interactivable', step=-1)
				else:
					result = manager.move(type='interactivable', step=1)
			elif gesture.mainKeyName == "t":
				if "shift" in gesture.modifierNames:
					result = manager.move(type='text', step=-1)
				else:
					result = manager.move(type='text', step=1)
			elif gesture.mainKeyName == "l":
				if "shift" in gesture.modifierNames:
					result = manager.move(type='latex', step=-1)
				else:
					result = manager.move(type='latex', step=1)
			elif gesture.mainKeyName == "a":
				if "shift" in gesture.modifierNames:
					result = manager.move(type='asciimath', step=-1)
				else:
					result = manager.move(type='asciimath', step=1)
			elif gesture.mainKeyName == "m":
				if "shift" in gesture.modifierNames:
					result = manager.move(type='mathml', step=-1)
				else:
					result = manager.move(type='mathml', step=1)
			elif gesture.mainKeyName == "home":
				result = manager.start()
			elif gesture.mainKeyName == "end":
				result = manager.end()
			else:
				result = None

			if not result:
				tones.beep(100, 50)
				result = manager.move(type='any', step=0)
				if "shift" in gesture.modifierNames:
					selected = True

			if result:
				if selected:
					manager.caret.updateSelection()

				from mathPres import speechProvider
				if "alt" not in gesture.modifierNames and result['type'] == "latex":
					mathMl = latex2mathml(result['data'])
					mathMl = mathMl.replace("<<", "&lt;<").replace(">>", ">&gt;")
					speech.speak(speechProvider.getSpeechForMathMl(mathMl))
				elif "alt" not in gesture.modifierNames and result['type'] == "asciimath":
					mathMl = asciimath2mathml(result['data'])
					mathMl = mathMl.replace("<<", "&lt;<").replace(">>", ">&gt;")
					speech.speak(speechProvider.getSpeechForMathMl(mathMl))
				elif "alt" not in gesture.modifierNames and result['type'] == "mathml":
					mathMl = result['data']
					speech.speak(speechProvider.getSpeechForMathMl(mathMl))
				elif not selected:
					ui.message(result['data'])

				if "alt" in gesture.modifierNames:
					tones.beep(500, 50)

	def script_navigateLine(self, gesture):
		with SectionManager() as manager:
			selected = False
			if gesture.mainKeyName == "upArrow":
				results = manager.moveLine(step=-1)
				if "shift" in gesture.modifierNames:
					selected = True
			elif gesture.mainKeyName == "downArrow":
				results = manager.moveLine(step=1)
				if "shift" in gesture.modifierNames:
					selected = True
			elif gesture.mainKeyName == "home":
				results = manager.moveLine(step=0, type=gesture.mainKeyName)
				if "shift" in gesture.modifierNames:
					selected = True
			elif gesture.mainKeyName == "end":
				results = manager.moveLine(step=0, type=gesture.mainKeyName)
				if "shift" in gesture.modifierNames:
					selected = True
			elif gesture.mainKeyName == "pageUp":
				results = manager.moveLine(step=-10)
				if "shift" in gesture.modifierNames:
					selected = True
			elif gesture.mainKeyName == "pageDown":
				results = manager.moveLine(step=10)
				if "shift" in gesture.modifierNames:
					selected = True
			else:
				results = []

			if len(results) == 0:
				tones.beep(100, 50)
				results = manager.moveLine(step=0)
				if "shift" in gesture.modifierNames:
					selected = True

			if len(results) > 0:
				if selected:
					manager.caret.updateSelection()

				from mathPres import speechProvider
				for result in results:
					if result['data'] == "":
						continue
					if result['type'] == "latex":
						mathMl = latex2mathml(result['data'])
						mathMl = mathMl.replace("<<", "&lt;<").replace(">>", ">&gt;")
						speech.speak(speechProvider.getSpeechForMathMl(mathMl))
					elif result['type'] == "asciimath":
						mathMl = asciimath2mathml(result['data'])
						mathMl = mathMl.replace("<<", "&lt;<").replace(">>", ">&gt;")
						speech.speak(speechProvider.getSpeechForMathMl(mathMl))
					elif result['type'] == "mathml":
						mathMl = result['data']
						mathMl = mathMl.replace("<<", "&lt;<").replace(">>", ">&gt;")
						speech.speak(speechProvider.getSpeechForMathMl(mathMl))
					else:
						ui.message(result['data'])

	def script_navigateCopy(self, gesture):
		with SectionManager() as manager:
			result = manager.move(type='any', step=0)
			api.copyToClip(result["raw"])
			ui.message(_("{data} copy to clipboard").format(data=result["raw"]))

	def script_navigatePaste(self, gesture):
		with SectionManager() as manager:
			manager.endMargin()
			KeyboardInputGesture.fromName("control+v").send()
			ui.message(_("{data} insert to document").format(data=api.getClipData()))

	def script_navigateCut(self, gesture):
		with SectionManager() as manager:
			result = manager.move(type='any', step=0)
			manager.caret.updateSelection()
			KeyboardInputGesture.fromName("control+x").send()
			ui.message(_("{data} cut from document").format(data=result["raw"]))

	def script_navigateDelete(self, gesture):
		with SectionManager() as manager:
			result = manager.move(type='any', step=0)
			manager.caret.updateSelection()
			KeyboardInputGesture.fromName("delete").send()
			ui.message(_("{data} delete from document").format(data=result["raw"]))


class SectionManager:
	def __init__(self):
		self.reset()

	@property
	def pointer(self):
		try:
			pointer = self.points[self.all_index]
		except:
			pointer = None

		return pointer

	@property
	def delimiter(self):
		if self.pointer['type'] == 'latex':
			result = LaTeX_delimiter[config.conf["Access8Math"]["settings"]["LaTeX_delimiter"]]
		elif self.pointer['type'] == 'asciimath':
			result = AsciiMath_delimiter["graveaccent"]
		else:
			result = {
				"start": "",
				"end": "",
				"type": self.pointer['type'],
			}
		return result

	@property
	def inSection(self):
		delimiter_start_length = len(self.delimiter["start"])
		delimiter_end_length = len(self.delimiter["end"])

		focus = api.getFocusObject()
		self.caret = focus.makeTextInfo(textInfos.POSITION_CARET)

		if self.caret._startOffset >= self.pointer['start'] + delimiter_start_length and self.caret._endOffset <= self.pointer['end'] - delimiter_end_length:
			return True
		else:
			return False

	@property
	def inMath(self):
		focus = api.getFocusObject()
		self.caret = focus.makeTextInfo(textInfos.POSITION_CARET)

		if self.inSection and (self.pointer['type'] == 'latex' or self.pointer['type'] == 'asciimath' or self.pointer['type'] == 'mathml'):
			return True
		else:
			return False

	@property
	def inText(self):
		focus = api.getFocusObject()
		self.caret = focus.makeTextInfo(textInfos.POSITION_CARET)

		if self.inSection and self.pointer['type'] == 'text':
			return True
		else:
			return False

	@property
	def inLaTeX(self):
		focus = api.getFocusObject()
		self.caret = focus.makeTextInfo(textInfos.POSITION_CARET)

		if self.inSection and self.pointer['type'] == 'latex':
			return True
		else:
			return False

	@property
	def inAsciiMath(self):
		focus = api.getFocusObject()
		self.caret = focus.makeTextInfo(textInfos.POSITION_CARET)

		if self.inSection and self.pointer['type'] == 'asciimath':
			return True
		else:
			return False

	@property
	def inMathML(self):
		focus = api.getFocusObject()
		self.caret = focus.makeTextInfo(textInfos.POSITION_CARET)

		if self.inSection and self.pointer['type'] == 'mathml':
			return True
		else:
			return False

	def reset(self):
		self.all_index = -1
		self.points = None

	def __enter__(self):
		focus = api.getFocusObject()
		self.caret = focus.makeTextInfo(textInfos.POSITION_CARET)
		self.selection = focus.makeTextInfo(textInfos.POSITION_SELECTION)
		self.reset()
		self.document = focus.makeTextInfo(textInfos.POSITION_ALL)
		self.points = textmath2laObjFactory(
			delimiter={
				"latex": config.conf["Access8Math"]["settings"]["LaTeX_delimiter"],
				"asciimath": "graveaccent",
			}
		)(self.document.text)
		for index, point in enumerate(self.points):
			if self.caret._startOffset >= point['start'] and self.caret._startOffset < point['end']:
				self.all_index = index
				break

		if self.caret._startOffset >= point['start'] and self.caret._startOffset <= point['end']:
			self.all_index = index

		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		pass

	def move(self, step=0, type="any", all_index=None):
		if all_index:
			type = self.points[all_index]['type']
			index = self.points[all_index]['index']
		else:
			index = -1
			if type == 'any':
				if self.all_index != -1 and self.all_index + step >= 0 and self.all_index + step < len(self.points):
					type = self.points[self.all_index + step]['type']
					index = self.points[self.all_index + step]['index']
			elif type == 'interactivable':
				if step > 0:
					for point in self.points[self.all_index + 1:]:
						if point['type'] == "latex" or point['type'] == "asciimath" or point['type'] == "mathml":
							index = point['index']
							break
				elif step < 0:
					for point in self.points[0:self.all_index]:
						if point['type'] == "latex" or point['type'] == "asciimath" or point['type'] == "mathml":
							index = point['index']
			else:
				if step > 0:
					for point in self.points[self.all_index + 1:]:
						if point['type'] == type:
							index = point['index']
							break
				elif step < 0:
					for point in self.points[0:self.all_index]:
						if point['type'] == type:
							index = point['index']

		pointer = None
		for all_index, point in enumerate(self.points):
			type_match = point['type'] == type
			if type == "interactivable":
				type_match |= point['type'] == "latex"
				type_match |= point['type'] == "asciimath"
				type_match |= point['type'] == "mathml"
			if type_match and point['index'] == index:
				self.all_index = all_index
				pointer = point
				break

		if not pointer:
			return None

		delimiter_start_length = len(self.delimiter["start"])
		self.caret._startOffset = self.caret._endOffset = pointer['start'] + delimiter_start_length
		self.caret.updateCaret()
		self.caret._startOffset = pointer['start']
		self.caret._endOffset = pointer['end']

		return pointer

	def moveLine(self, step, type=None):
		line = -1
		if self.pointer and self.pointer["line"] + step >= 0 and self.pointer["line"] + step <= self.points[-1]["line"]:
			line = self.pointer["line"] + step
		pointers = []
		for all_index, point in enumerate(self.points):
			if point['line'] == line:
				self.all_index = all_index
				pointers.append(point)

		if len(pointers) > 0:
			if type:
				if type == "home":
					pointers = [pointers[0]]
				elif type == "end":
					pointers = [pointers[-1]]
				self.caret._startOffset = self.caret._endOffset = pointers[0]['start']
				self.caret.updateCaret()
				self.caret._startOffset = pointers[0]['start']
				self.caret._endOffset = pointers[0]['end']
			else:
				self.caret._startOffset = self.caret._endOffset = pointers[0]['start']
				self.caret.updateCaret()
				self.caret._startOffset = pointers[0]['start']
				self.caret._endOffset = pointers[-1]['end']

		return pointers

	def start(self):
		delimiter_start_length = len(self.delimiter["start"])
		if self.pointer:
			self.caret._startOffset = self.caret._endOffset = self.pointer['start'] + delimiter_start_length
			self.caret.updateCaret()
			return self.pointer
		return None

	def end(self):
		delimiter_end_length = len(self.delimiter["end"])
		if self.pointer:
			self.caret._startOffset = self.caret._endOffset = self.pointer['end'] - delimiter_end_length - 1
			self.caret.updateCaret()
			return self.pointer
		return None

	def startMargin(self):
		if self.pointer:
			self.caret._startOffset = self.caret._endOffset = self.pointer['start']
			self.caret.updateCaret()
			return self.pointer
		return None

	def endMargin(self):
		if self.pointer:
			self.caret._startOffset = self.caret._endOffset = self.pointer['end']
			self.caret.updateCaret()
			return self.pointer
		return None

	def batch(self, mode='reverse'):
		def l2a(m):
			delimiter = AsciiMath_delimiter["graveaccent"]
			data = m.group('latex') or m.group('latex_start')
			try:
				data = delimiter["start"] + latex2asciimath(data) + delimiter["end"]
			except:
				data = m.group(0)
				print(data)
			return data

		def a2l(m):
			delimiter = LaTeX_delimiter[config.conf["Access8Math"]["settings"]["LaTeX_delimiter"]]
			data = m.group('asciimath') or m.group('asciimath_start')
			try:
				data = delimiter["start"] + asciimath2latex(data)[1:-1] + delimiter["end"]
			except:
				data = m.group(0)
				print(data)
			return data

		def reverse(m):
			data = m.group("latex") or m.group("latex_start") or m.group("asciimath") or m.group("asciimath_start")
			if not data:
				data = ''
			if m.group("ld_start") or m.group("lsd_start"):
				type_ = "latex"
			elif m.group("ad_start") or m.group("asd_start"):
				type_ = "asciimath"
			else:
				raise TypeError(m.group(0))
			if type_ == "latex":
				result = l2a(m)
			elif type_ == "asciimath":
				result = a2l(m)
			else:
				result = m.group(0)
			return result

		def b2d(m):
			data = m.group('latex') or m.group('latex_start')
			return r"${data}$".format(data=data)

		def d2b(m):
			data = m.group('latex') or m.group('latex_start')
			return r"\({data}\)".format(data=data)

		delimiter_regular_expression = delimiterRegularExpression(
			delimiter={
				"latex": config.conf["Access8Math"]["settings"]["LaTeX_delimiter"],
				"asciimath": "graveaccent",
			}
		)

		if mode == 'latex2asciimath':
			restring = "|".join([delimiter_regular_expression["latex"], delimiter_regular_expression["latex_start"]])
			pattern = re.compile(restring)
			text = pattern.sub(l2a, self.document.text)
		elif mode == 'asciimath2latex':
			restring = "|".join([delimiter_regular_expression["asciimath"], delimiter_regular_expression["asciimath_start"]])
			pattern = re.compile(restring)
			text = pattern.sub(a2l, self.document.text)
		elif mode == 'reverse':
			restring = "|".join([delimiter_regular_expression["latex"], delimiter_regular_expression["latex_start"], delimiter_regular_expression["asciimath"], delimiter_regular_expression["asciimath_start"]])
			pattern = re.compile(restring)
			text = pattern.sub(reverse, self.document.text)
		elif mode == 'bracket2dollar':
			restring = "|".join([latex_bracket_dollar["latex_bracket"], latex_bracket_dollar["latex_start_bracket"]])
			pattern = re.compile(restring)
			text = pattern.sub(b2d, self.document.text)
		elif mode == 'dollar2bracket':
			restring = "|".join([latex_bracket_dollar["latex_dollar"], latex_bracket_dollar["latex_start_dollar"]])
			pattern = re.compile(restring)
			text = pattern.sub(d2b, self.document.text)
		else:
			text = ''
		return text


def text2template(value, output):
	backslash_pattern = re.compile(r"\\")
	data = backslash_pattern.sub(lambda m: m.group(0).replace('\\', '\\\\'), value)
	data = data.replace(r'`', r'\`')
	raw = data
	template = env.get_template("index.template")
	content = template.render({
		'title': 'Access8Math',
		'data': data,
		'raw': raw,
		'LaTeX_delimiter': config.conf["Access8Math"]["settings"]["LaTeX_delimiter"],
		'display': config.conf["Access8Math"]["settings"]["HTML_display"],
	})
	with open(output, "w", encoding="utf8", newline="") as f:
		f.write(content)
	return output
