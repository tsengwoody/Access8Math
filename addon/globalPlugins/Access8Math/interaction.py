from collections import Iterable
import re
import wx

import addonHandler
import api
import config
import eventHandler
import globalVars
from keyboardHandler import KeyboardInputGesture
from NVDAObjects.window import Window
import mathPres
from scriptHandler import script
import speech
import textInfos
import tones
import ui

try:
	from speech import BreakCommand
except:
	from speech.commands import BreakCommand

import A8M_PM
from A8M_PM import MathContent

addonHandler.initTranslation()

def flatten(lines):
	"""
	convert tree to linear using generator
	@param lines:
	@type list
	@rtype
	"""
	for line in lines:
		if isinstance(line, Iterable) and not isinstance(line, str):
			for sub in flatten(line):
				yield sub
		else:
			yield line

def translate_SpeechCommand(serializes):
	"""
	convert Access8Math serialize object to SpeechCommand
	@param lines: source serializes
	@type list
	@rtype SpeechCommand
	"""
	pattern = re.compile(r'[@](?P<time>[\d]*)[@]')
	speechSequence = []
	for r in flatten(serializes):
		time_search = pattern.search(r)
		try:
			time = time_search.group('time')
			command = BreakCommand(time=int(time) +int(config.conf["Access8Math"]["settings"]["item_interval_time"]))
			speechSequence.append(command)
		except:
			speechSequence.append(r)

	return speechSequence

def translate_Unicode(serializes):
	"""
	convert Access8Math serialize object to unicode
	@param lines: source serializes
	@type list
	@rtype unicode
	"""
	pattern = re.compile(r'[@](?P<time>[\d]*)[@]')
	sequence = ''

	for c in serializes:
		sequence = sequence +u'\n'
		for r in flatten(c):
			time_search = pattern.search(r)
			try:
				time = time_search.group('time')
			except:
				sequence = sequence +str(r)
			sequence = sequence +' '

	# replace mutiple blank to single blank
	pattern = re.compile(r'[ ]+')
	sequence = pattern.sub(lambda m: u' ', sequence)

	# replace blank line to none
	pattern = re.compile(r'\n\s*\n')
	sequence = pattern.sub(lambda m: u'\n', sequence)

	# strip blank at start and end line
	temp = ''
	for i in sequence.split('\n'):
		temp = temp +i.strip() +'\n'
	sequence = temp

	return sequence.strip()

class GenericFrame(wx.Frame):
	def __init__(self, *args, **kwargs):
		super(GenericFrame, self).__init__(*args, **kwargs)
		self.buttons = []

		self.CreateStatusBar() # A StatusBar in the bottom of the window
		self.createMenuBar()

		self.panel = wx.Panel(self, -1)
		self.createButtonBar(self.panel)

		mainSizer=wx.BoxSizer(wx.HORIZONTAL)
		for button in self.buttons:
			mainSizer.Add(button)

		self.panel.SetSizer(mainSizer)
		mainSizer.Fit(self)

	def menuData(self):
		return [
		]

	def createMenuBar(self):
		self.menuBar = wx.MenuBar()
		for eachMenuData in self.menuData():
			menuLabel = eachMenuData[0]
			menuItems = eachMenuData[1]
			self.menuBar.Append(self.createMenu(menuItems), menuLabel)

		self.SetMenuBar(self.menuBar)

	def createMenu(self, menuData):
		menu = wx.Menu()
		for eachItem in menuData:
			if len(eachItem) == 2:
				label = eachItem[0]
				subMenu = self.createMenu(eachItem[1])
				menu.AppendMenu(wx.NewId(), label, subMenu)

			else:
				self.createMenuItem(menu, *eachItem)
		return menu

	def createMenuItem(self, menu, label, status, handler, kind=wx.ITEM_NORMAL):
		if not label:
			menu.AppendSeparator()
			return
		menuItem = menu.Append(-1, label, status, kind)
		self.Bind(wx.EVT_MENU, handler, menuItem)

	def buttonData(self):
		return [
		]

	def createButtonBar(self, panel, yPos = 0):
		xPos = 0
		for eachLabel, eachHandler in self.buttonData():
			pos = (xPos, yPos)
			button = self.buildOneButton(panel, eachLabel,eachHandler, pos)
			self.buttons.append(button)
			xPos += button.GetSize().width

	def buildOneButton(self, parent, label, handler, pos=(0,0)):
		button = wx.Button(parent, -1, label, pos)
		self.Bind(wx.EVT_BUTTON, handler, button)
		return button


class A8MInteractionFrame(GenericFrame):
	def __init__(self):
		title = _("Access8Math interaction window")
		super().__init__(wx.GetApp().TopWindow, title=title)
		self.Bind(wx.EVT_CHAR_HOOK, self.OnChar)

	def menuData(self):
		return [
			(_("&Menu"), (
				(_("&Exit"),_("Terminate the program"), self.OnExit),
			))
		]

	def buttonData(self):
		return (
			(_("interaction"), self.OnInteraction),
			(_("copy"), self.OnRawdataToClip),
		)

	def OnExit(self, event):
		self.Destroy()
		global main_frame
		main_frame = None

	def OnChar(self, event):
		keyCode = event.GetKeyCode()
		if keyCode == wx.WXK_ESCAPE:
			self.Destroy()
			global main_frame
			main_frame = None
			# self.Close()
		event.Skip() 

	def set_mathcontent(self, mathcontent):
		self.mathcontent = mathcontent
		globalVars.mathcontent = mathcontent

	def OnInteraction(self, event):
		parent = api.getFocusObject()
		vw = A8MInteraction(parent=parent)
		vw.set(data=self.mathcontent, name="")
		vw.setFocus()

	def OnRawdataToClip(self, event):
		api.copyToClip(self.mathcontent.root.get_mathml())
		ui.message(_("copy"))


class A8MProvider(mathPres.MathPresentationProvider):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.mathcontent = None

	def getSpeechForMathMl(self, mathMl):
		self.mathcontent = MathContent(config.conf["Access8Math"]["settings"]["language"], mathMl)
		return translate_SpeechCommand(self.mathcontent.pointer.serialized())

	def getBrailleForMathMl(self, mathMl):
		"""Get braille output for specified MathML markup.
		@param mathMl: The MathML markup.
		@type mathMl: str
		@return: A string of Unicode braille.
		@rtype: unicode
		"""
		raise SystemError
		# raise NotImplementedError

	def interactWithMathMl(self, mathMl):
		mathcontent = MathContent(config.conf["Access8Math"]["settings"]["language"], mathMl)
		if config.conf["Access8Math"]["settings"]["interaction_frame_show"]:
			show_main_frame(mathcontent)
		else:
			parent = api.getFocusObject()
			vw = A8MInteraction(parent=parent)
			vw.set(data=mathcontent, name="")
			vw.setFocus()


class A8MInteraction(Window):
	# role = controlTypes.Role.MATH
	# Override the window name.
	# name = None
	# Any tree interceptor should not apply here.
	treeInterceptor = None

	def __init__(self, parent, root=None):
		self.parent = parent
		self.mathcontent = self.data = None
		super().__init__(windowHandle=self.parent.windowHandle)

	def set(self, name, data, *args, **kwargs):
		# self.name = name + " - math window"
		self.mathcontent = self.data = data
		# BrailleHandler.message()

	def setFocus(self):
		eventHandler.executeEvent("gainFocus", self)

	@script(
		gestures=["kb:escape"]
	)
	def script_escape(self, gesture):
		eventHandler.executeEvent("gainFocus", self.parent)

	def _get_mathMl(self):
		return self.mathcontent.root.get_mathml()
		#return self.raw_data

	def makeTextInfo(self, position=textInfos.POSITION_FIRST):
		return A8MInteractionTextInfo(self, position)

	"""def event_gainFocus(self):
		ui.message(_("enter interaction mode"))
		super().event_gainFocus()
		api.setReviewPosition(self.makeTextInfo(), False)"""

	def reportFocus(self):
		speech.speak(translate_SpeechCommand(self.mathcontent.root.serialized()))

	def getScript(self, gesture):
		if isinstance(gesture, KeyboardInputGesture) and "NVDA" not in gesture.modifierNames and (
						gesture.mainKeyName in {
							"leftArrow", "rightArrow", "upArrow", "downArrow",
							"home", "end",
							"space", "backspace", "enter",
						}
						#or len(gesture.mainKeyName)  ==  1
		):
			return self.script_navigate
		return super().getScript(gesture)

	def script_navigate(self, gesture):
		r = False
		if gesture.mainKeyName in ["downArrow", "upArrow", "leftArrow", "rightArrow", "home"]:
			r = self.mathcontent.navigate(gesture.mainKeyName)

		if not r:
			if config.conf["Access8Math"]["settings"]["no_move_beep"]:
				tones.beep(100, 100)
			else:
				speech.speak([_("no move")])

		api.setReviewPosition(self.makeTextInfo(), False)
		if self.mathcontent.pointer.parent:
			if config.conf["Access8Math"]["settings"]["auto_generate"] and self.mathcontent.pointer.parent.role_level == A8M_PM.AUTO_GENERATE:
				speech.speak([self.mathcontent.pointer.des])
			elif config.conf["Access8Math"]["settings"]["dictionary_generate"] and self.mathcontent.pointer.parent.role_level == A8M_PM.DIC_GENERATE:
				speech.speak([self.mathcontent.pointer.des])
		else:
			speech.speak([self.mathcontent.pointer.des])
		speech.speak(translate_SpeechCommand(self.mathcontent.pointer.serialized()))

	@script(
		gesture="kb:control+c",
	)
	def script_rawdataToClip(self, gesture):
		#api.copyToClip(self.raw_data)
		api.copyToClip(self.mathcontent.root.get_mathml())
		ui.message(_("copy"))

	@script(
		gesture="kb:control+s",
	)
	def script_snapshot(self, gesture):
		ui.message(_("snapshot"))
		globalVars.mathcontent = self.mathcontent

	@script(
		gesture="kb:control+a",
	)
	def script_asciimath_insert(self, gesture):
		def show(event):
			# asciimath to mathml
			from xml.etree.ElementTree import tostring
			import asciimathml
			global main_frame
			parent = main_frame if main_frame else gui.mainFrame
			with wx.TextEntryDialog(parent=parent, message=_("Write AsciiMath Content")) as dialog:
				if dialog.ShowModal() == wx.ID_OK:
					data = dialog.GetValue()
					data = asciimathml.parse(data)
					mathml = tostring(data)
					mathml = mathml.decode("utf-8")
					mathml = mathml.replace('math>', 'mrow>')
					self.mathcontent.insert(mathml)

		wx.CallAfter(show, None)

	@script(
		gesture="kb:control+l",
	)
	def script_latex_insert(self, gesture):
		def show(event):
			# latex to mathml
			from xml.etree.ElementTree import tostring
			import latex2mathml.converter
			global main_frame
			parent = main_frame if main_frame else gui.mainFrame
			with wx.TextEntryDialog(parent=parent, message=_("Write LaTeX Content")) as dialog:
				if dialog.ShowModal() == wx.ID_OK:
					data = dialog.GetValue()
					data = latex2mathml.converter.convert(data)
					mathml = data
					# mathml = mathml.replace('math>', 'mrow>')
					self.mathcontent.insert(mathml)

		wx.CallAfter(show, None)

	@script(
		gesture="kb:control+delete",
	)
	def script_delete(self, gesture):
		self.mathcontent.delete()


class A8MInteractionTextInfo(textInfos.offsets.OffsetsTextInfo):
	def __init__(self, obj, position):
		super().__init__(obj, position)
		self.obj = obj

	def _getStoryLength(self):
		serializes = self.obj.mathcontent.pointer.serialized()
		return len(translate_Unicode(serializes))

	def _getStoryText(self):
		serializes = self.obj.mathcontent.pointer.serialized()
		return translate_Unicode(serializes)

	def _getTextRange(self, start, end):
		text = self._getStoryText()
		return text[start:end] if text else u""

def show_main_frame(mathcontent):
	global main_frame
	if not main_frame:
		main_frame = A8MInteractionFrame()
	main_frame.set_mathcontent(mathcontent=mathcontent)
	main_frame.Show()
	main_frame.Raise()

main_frame = None
