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

shortcut_mode = False
sln_mode = False
active = config.conf["Access8Math"]["settings"]["edit_NVDA_gesture"]

class TextMathEditField(NVDAObject):
	def getScript(self, gesture):
		global sln_mode
		if isinstance(gesture, KeyboardInputGesture):
			if (
				(len(gesture.modifierNames) == 0 or (len(gesture.modifierNames) == 1 and "shift" in gesture.modifierNames)) \
				and (
					gesture.mainKeyName in set("abcdefghijklmnopqrstuvwxyz1234567890") 
				) \
				and sln_mode
			):
				return self.script_sln
		return super().getScript(gesture)

	@script(
		gestures=["kb:NVDA+alt+h" if active else "kb:alt+h"],
		description=_("view math"),
		category=ADDON_SUMMARY,
	)
	def script_view_math(self, gesture):
		document = self.makeTextInfo(textInfos.POSITION_ALL)
		html_file = text2template(document.text, os.path.join(PATH, 'web', 'review', 'index.html'))
		raw_file = os.path.join(PATH, 'web', 'review', 'raw.txt')
		with open(raw_file, "w", encoding="utf-8") as f:
			f.write(document.text)
		A8MHTMLCommandView(file=html_file).setFocus()

	@script(
		gestures=["kb:NVDA+alt+s" if active else "kb:alt+s"],
		description=_("shortcut switch"),
		category=ADDON_SUMMARY,
	)
	def script_shortcut_switch(self, gesture):
		global shortcut_mode
		shortcut_mode = not shortcut_mode
		if shortcut_mode:
			ui.message(_("shortcut mode on"))
		else:
			ui.message(_("shortcut mode off"))

	@script(gestures=["kb:NVDA+shift+space"])
	def script_sln_switch(self, gesture):
		global sln_mode
		sln_mode = not sln_mode
		if sln_mode:
			ui.message(_("single letter navigation mode on"))
		else:
			ui.message(_("single letter navigation mode off"))

	def script_sln(self, gesture):
		if not (gesture.mainKeyName == "t" or gesture.mainKeyName == "l"):
			tones.beep(100, 50)
			return
		self.script_navigate(gesture)

	@script(gestures=["kb:f{}".format(i) for i in range(1, 13)])
	def script_shortcut(self, gesture):
		global shortcut_mode
		if not shortcut_mode:
			gesture.send()
			return
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

	@script(gestures=["kb:shift+f{}".format(i) for i in range(1, 13)])
	def script_shortcut_help(self, gesture):
		global shortcut_mode
		if not shortcut_mode:
			gesture.send()
			return
		with SectionManager() as manager:
			view = A8MLaTeXCommandView(selection=manager.selection.text)
		slot = gesture.mainKeyName[1:]
		if slot in view.data.shortcut:
			ui.message(view.data.shortcut[slot]["name"])
		else:
			ui.message(_("shortcut {shortcut} is not set").format(
				shortcut=slot,
			))

	@script(
		gestures=["kb:NVDA+alt+m" if active else "kb:alt+m"],
		description=_("popup mark command menu window"),
		category=ADDON_SUMMARY,
	)
	def script_mark(self, gesture):
		with SectionManager() as manager:
			if manager.pointer and manager.pointer['type'] == 'text':
				A8MMarkCommandView(selection=manager.selection.text, delimiter=LaTeX_delimiter[config.conf["Access8Math"]["settings"]["LaTeX_delimiter"]]).setFocus()
			else:
				ui.message(_("In math section. Please leave math section first and try again."))

	@script(
		gestures=["kb:NVDA+alt+l" if active else "kb:alt+l"],
		description=_("popup LaTeX command menu window"),
		category=ADDON_SUMMARY,
	)
	def script_latex_command(self, gesture):
		with SectionManager() as manager:
			if manager.pointer and manager.pointer['type'] == 'math':
				A8MLaTeXCommandView(selection=manager.selection.text).setFocus()
			else:
				ui.message(_("Not in math section. Please insert LaTeX mark first and try again."))

	@script(
		gestures=[
			"kb:NVDA+alt+downArrow" if active else "kb:alt+downArrow",
			"kb:NVDA+alt+leftArrow" if active else "kb:alt+leftArrow",
			"kb:NVDA+alt+rightArrow" if active else "kb:alt+rightArrow",
			"kb:NVDA+alt+shift+downArrow" if active else "kb:alt+shift+downArrow",
			"kb:NVDA+alt+shift+leftArrow" if active else "kb:alt+shift+leftArrow",
			"kb:NVDA+alt+shift+rightArrow" if active else "kb:alt+shift+rightArrow"
		],
		description=_("move cursor by block unit"),
		category=ADDON_SUMMARY,
	)
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
			if gesture.mainKeyName == "t":
				if "shift" in gesture.modifierNames:
					result = manager.move(type='text', step=-1)
				else:
					result = manager.move(type='text', step=1)
			elif gesture.mainKeyName == "l":
				if "shift" in gesture.modifierNames:
					result = manager.move(type='math', step=-1)
				else:
					result = manager.move(type='math', step=1)
			if result:
				tones.beep(500, 50)
				if selected:
					manager.caret.updateSelection()
				else:
					ui.message(result['data'])
			else:
				tones.beep(100, 50)

	@script(
		gestures=[
			"kb:NVDA+alt+home" if active else "kb:alt+home",
			"kb:NVDA+alt+end" if active else "kb:alt+end",
		],
		description=_("move cursor to block start point or block end point"),
		category=ADDON_SUMMARY,
	)
	def script_startend(self, gesture):
		with SectionManager() as manager:
			if gesture.mainKeyName == "home":
				manager.start()
			elif gesture.mainKeyName == "end":
				manager.end()
		tones.beep(500, 20)

	@script(
		gestures=["kb:NVDA+alt+i" if active else "kb:alt+i"],
		description=_("interacte with LaTeX"),
		category=ADDON_SUMMARY,
	)
	def script_interacte(self, gesture):
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
			return True
		return False

	def end(self):
		if self.pointer:
			if self.pointer['type'] == 'math':
				self.caret._startOffset = self.pointer['end'] - 3
				self.caret._endOffset = self.pointer['end'] - 3
			else:
				self.caret._startOffset = self.pointer['end'] - 1
				self.caret._endOffset = self.pointer['end'] - 1

			self.caret.updateCaret()
			return True
		return False

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
