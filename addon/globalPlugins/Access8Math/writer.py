import os
import re

PATH = os.path.dirname(__file__)

import addonHandler
import api
import config
from keyboardHandler import KeyboardInputGesture
from NVDAObjects import NVDAObject
from scriptHandler import script, getLastScriptRepeatCount
import textInfos
import tones
import ui

from A8M_PM import MathContent
from command.latex import A8MLaTeXCommandView, A8MLaTeXCommandModel
from command.mark import A8MMarkCommandView
from command.review import A8MHTMLCommandView
from delimiter import LaTeX as LaTeX_delimiter
from lib.mathProcess import textmath2laObj, laObj2mathObj, obj2html, textmath2laObjEdit, latex2mathml
from interaction import A8MInteraction, show_main_frame

addonHandler.initTranslation()
ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

from jinja2 import Environment, FileSystemLoader, select_autoescape
TEMPLATES_PATH = os.path.join(PATH, 'web', 'templates')
env = Environment(loader=FileSystemLoader(TEMPLATES_PATH), variable_start_string='{|{', variable_end_string='}|}')

write_mode = config.conf["Access8Math"]["settings"]["write_mode"]
navigate_mode = config.conf["Access8Math"]["settings"]["navigate_mode"]
shortcut_mode = config.conf["Access8Math"]["settings"]["shortcut_mode"]
singleLetterNav_mode = False

class TextMathEditField(NVDAObject):
	initial = True
	write_mode = False
	navigate_mode = False
	shortcut_mode = False
	singleLetterNav_mode = False
	_originGestureMap = {}

	def event_gainFocus(self):
		if self.initial:
			self._originGestureMap = self._gestureMap.copy()
			self.initial = False

		global write_mode, navigate_mode, shortcut_mode
		try:
			if write_mode:
				self.bindWriteGestures()
			if navigate_mode:
				self.bindNavigateGestures()
			if shortcut_mode:
				self.bindShortcutGestures()
			if self.singleLetterNav_mode:
				self.bindSingleLetterNavGestures()
		except WindowsError:
			pass

		super().event_gainFocus()

	def bindWriteGestures(self):
		self.bindGesture("kb:alt+h", "view_math")
		self.bindGesture("kb:alt+i", "interact")
		self.bindGesture("kb:alt+l", "latex_command")
		self.bindGesture("kb:alt+m", "mark")

	def unbindWriteGestures(self):
		import inputCore
		for key in ["alt+h", "alt+i", "alt+l", "alt+m"]:
			key = "kb:{}".format(key)
			try:
				self.removeGestureBinding(key)
			except KeyError as e:
				pass

			if key in self._originGestureMap:
				key = inputCore.normalizeGestureIdentifier(key)
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
			except KeyError as e:
				pass

			if key in self._originGestureMap:
				key = inputCore.normalizeGestureIdentifier(key)
				self._gestureMap[key] = self._originGestureMap[key]

	def bindShortcutGestures(self):
		for i in range(1, 13):
			key = "kb:f{}".format(i)
			self.bindGesture(key, "shortcut")
			key = "kb:shift+f{}".format(i)
			self.bindGesture(key, "shortcut_help")

	def unbindShortcutGestures(self):
		import inputCore
		for i in range(1, 13):
			key = "kb:f{}".format(i)
			try:
				self.removeGestureBinding(key)
			except KeyError:
				pass
			if key in self._originGestureMap:
				key = inputCore.normalizeGestureIdentifier(key)
				self._gestureMap[key] = self._originGestureMap[key]

			key = "kb:shift+f{}".format(i)
			try:
				self.removeGestureBinding(key)
			except KeyError:
				pass
			if key in self._originGestureMap:
				key = inputCore.normalizeGestureIdentifier(key)
				self._gestureMap[key] = self._originGestureMap[key]

	def bindSingleLetterNavGestures(self):
		for c in [c for c in "abcdefghijklmnopqrstuvwxyz1234567890"] + ["upArrow", "downArrow", "leftArrow", "rightArrow", "home", "end"]:
			key = "kb:{}".format(c)
			self.bindGesture("kb:{}".format(c), "singleLetterNav")
			key = "kb:shift+{}".format(c)
			self.bindGesture("kb:shift+{}".format(c), "singleLetterNav")

	def unbindSingleLetterNavGestures(self):
		import inputCore
		for c in [c for c in "abcdefghijklmnopqrstuvwxyz1234567890"] + ["upArrow", "downArrow", "leftArrow", "rightArrow", "home", "end"]:
			key = "kb:{}".format(c)
			try:
				self.removeGestureBinding(key)
			except KeyError:
				pass
			if key in self._originGestureMap:
				key = inputCore.normalizeGestureIdentifier(key)
				self._gestureMap[key] = self._originGestureMap[key]

			key = "kb:shift+{}".format(c)
			try:
				self.removeGestureBinding(key)
			except KeyError:
				pass
			if key in self._originGestureMap:
				key = inputCore.normalizeGestureIdentifier(key)
				self._gestureMap[key] = self._originGestureMap[key]

	@script(
		gestures=["kb:alt+w"],
		description=_("write gesture toggle"),
		category=ADDON_SUMMARY,
	)
	def script_command_toggle(self, gesture):
		global write_mode
		write_mode = not write_mode
		if write_mode:
			self.bindWriteGestures()
			ui.message(_("activate write gesture"))
		else:
			self.unbindWriteGestures()
			ui.message(_("deactivate write gesture"))

	@script(
		gestures=["kb:alt+n"],
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
		gestures=["kb:alt+s"],
		description=_("shortcut gesture toggle"),
		category=ADDON_SUMMARY,
	)
	def script_shortcut_toggle(self, gesture):
		global shortcut_mode
		shortcut_mode = not shortcut_mode
		if shortcut_mode:
			self.bindShortcutGestures()
			ui.message(_("activate shortcut gesture"))
		else:
			self.unbindShortcutGestures()
			ui.message(_("deactivate shortcut gesture"))

	@script(
		gestures=["kb:NVDA+shift+space"],
		description=_("single letter navigate mode toggle"),
		category=ADDON_SUMMARY,
	)
	def script_singleLetterNav_toggle(self, gesture):
		self.singleLetterNav_mode = not self.singleLetterNav_mode
		if self.singleLetterNav_mode:
			self.bindSingleLetterNavGestures()
			ui.message(_("single letter navigation mode on"))
		else:
			self.unbindSingleLetterNavGestures()
			ui.message(_("single letter navigation mode off"))

	def script_shortcut(self, gesture):
		with SectionManager() as manager:
			if manager.pointer and manager.pointer['type'] == 'math':
				view = A8MLaTeXCommandView(selection=manager.selection.text)
				slot = gesture.mainKeyName[1:]
				if slot in view.data.shortcut:
					view.command(view.data.shortcut[slot]["id"])
				else:
					ui.message(_("shortcut {shortcut} is not set").format(
						shortcut=slot,
					))
			else:
				ui.message(_("Not in math section. Please insert LaTeX mark first and try again."))

	def script_shortcut_help(self, gesture):
		with SectionManager() as manager:
			view = A8MLaTeXCommandView(selection=manager.selection.text)
		slot = gesture.mainKeyName[1:]
		if slot in view.data.shortcut:
			ui.message(view.data.shortcut[slot]["name"])
		else:
			ui.message(_("shortcut {shortcut} is not set").format(
				shortcut=slot,
			))

	def script_singleLetterNav(self, gesture):
		self.script_navigate(gesture)

	def script_view_math(self, gesture):
		document = self.makeTextInfo(textInfos.POSITION_ALL)
		html_file = text2template(document.text, os.path.join(PATH, 'web', 'review', 'index.html'))
		raw_file = os.path.join(PATH, 'web', 'review', 'raw.txt')
		with open(raw_file, "w", encoding="utf-8") as f:
			f.write(document.text)
		A8MHTMLCommandView(file=html_file).setFocus()

	def script_mark(self, gesture):
		with SectionManager() as manager:
			if manager.pointer and manager.pointer['type'] == 'text':
				A8MMarkCommandView(selection=manager.selection.text, delimiter=LaTeX_delimiter[config.conf["Access8Math"]["settings"]["LaTeX_delimiter"]]).setFocus()
			else:
				ui.message(_("In math section. Please leave math section first and try again."))

	def script_latex_command(self, gesture):
		with SectionManager() as manager:
			if manager.pointer and manager.pointer['type'] == 'math':
				A8MLaTeXCommandView(selection=manager.selection.text).setFocus()
			else:
				ui.message(_("Not in math section. Please insert LaTeX mark first and try again."))

	def script_interact(self, gesture):
		delimiter = LaTeX_delimiter[config.conf["Access8Math"]["settings"]["LaTeX_delimiter"]]
		delimiter_start_length = len(delimiter["start"])
		delimiter_end_length = len(delimiter["end"])
		with SectionManager() as manager:
			if manager.pointer and manager.pointer['type'] == 'math':
				data = manager.pointer['data'][delimiter_start_length:-delimiter_end_length]
				mathMl = latex2mathml(data)
				mathMl = mathMl.replace("<<", "&lt;<").replace(">>", ">&gt;")
				mathcontent = MathContent(config.conf["Access8Math"]["settings"]["language"], mathMl)
				if config.conf["Access8Math"]["settings"]["interaction_frame_show"]:
					show_main_frame(mathcontent)
				else:
					parent = api.getFocusObject()
					vw = A8MInteraction(parent=parent)
					vw.set(data=mathcontent, name="")
					vw.setFocus()
			else:
				ui.message(_("This block cannot be interacted"))

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
			elif gesture.mainKeyName == "t":
				if "shift" in gesture.modifierNames:
					result = manager.move(type='text', step=-1)
				else:
					result = manager.move(type='text', step=1)
			elif gesture.mainKeyName == "l":
				if "shift" in gesture.modifierNames:
					result = manager.move(type='math', step=-1)
				else:
					result = manager.move(type='math', step=1)
			elif gesture.mainKeyName == "home":
				result = manager.start()
			elif gesture.mainKeyName == "end":
				result = manager.end()
			if result:
				tones.beep(500, 50)
				if selected:
					manager.caret.updateSelection()
				else:
					ui.message(result['data'])
			else:
				tones.beep(100, 50)


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

	def reset(self):
		self.all_index = -1
		self.points = None

	def __enter__(self):
		focus = api.getFocusObject()
		self.caret = focus.makeTextInfo(textInfos.POSITION_CARET)
		self.selection = focus.makeTextInfo(textInfos.POSITION_SELECTION)
		self.reset()
		document = focus.makeTextInfo(textInfos.POSITION_ALL)
		self.points = textmath2laObjEdit(LaTeX_delimiter=LaTeX_delimiter[config.conf["Access8Math"]["settings"]["LaTeX_delimiter"]])(document.text)
		for index, point in enumerate(self.points):
			if self.caret._startOffset >= point['start'] and self.caret._startOffset < point['end']:
				self.all_index = index
				break

		if self.caret._startOffset >= point['start'] and self.caret._startOffset <= point['end']:
			self.all_index = index

		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		pass

	def move(self, step, type):
		if step == 0:
			self.caret._startOffset = self.pointer['start']
			self.caret._endOffset = self.pointer['end']
			return self.pointer

		index = -1
		if type == 'any':
			if self.all_index != -1 and self.all_index+step >= 0 and self.all_index+step < len(self.points):
				type = self.points[self.all_index+step]['type']
				index = self.points[self.all_index+step]['index']
		else:
			if step > 0:
				for point in self.points[self.all_index+1:]:
					if point['type'] == type:
						index = point['index']
						break
			elif step < 0:
				for point in self.points[0:self.all_index]:
					if point['type'] == type:
						index = point['index']

		pointer = None
		for all_index, point in enumerate(self.points):
			if point['type'] == type and point['index'] == index:
				self.all_index = all_index
				pointer = point
				break

		if not pointer:
			return None

		self.caret._startOffset = self.caret._endOffset = pointer['start']+2 if type == 'math' else pointer['start']
		self.caret.updateCaret()
		self.caret._startOffset = pointer['start']
		self.caret._endOffset = pointer['end']

		return pointer

	def start(self):
		if self.pointer:
			if self.pointer['type'] == 'math':
				self.caret._startOffset = self.pointer['start']+2
				self.caret._endOffset = self.pointer['start']+2
			else:
				self.caret._startOffset = self.pointer['start']
				self.caret._endOffset = self.pointer['start']
			self.caret.updateCaret()
			return self.pointer
		return None

	def end(self):
		if self.pointer:
			if self.pointer['type'] == 'math':
				self.caret._startOffset = self.pointer['end'] - 3
				self.caret._endOffset = self.pointer['end'] - 3
			else:
				self.caret._startOffset = self.pointer['end'] - 1
				self.caret._endOffset = self.pointer['end'] - 1

			self.caret.updateCaret()
			return self.pointer
		return None

def text2template(value, output):
	raw = []
	for line in value.split('\n'):
		line = line.replace('\r', '').replace(r'`', r'\`')
		if line != '':
			raw.extend(textmath2laObj(LaTeX_delimiter=LaTeX_delimiter[config.conf["Access8Math"]["settings"]["LaTeX_delimiter"]])(line))
		raw.append({'type': 'text-content', 'data': ''})

	data = raw
	template = env.get_template("index.template")
	content = template.render({
		'title': 'Access8Math',
		'data': data,
		'raw': raw,
		'display': config.conf["Access8Math"]["settings"]["HTML_display"],
	})
	with open(output, 'w', encoding='utf8') as f:
		f.write(content)
	return output
