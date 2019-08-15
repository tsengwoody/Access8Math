"""# Access8Math: Allows access math content written by MathML in NVDA
# Copyright (C) 2017-2019 Tseng Woody <tsengwoody.tw@gmail.com>
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details."""
# coding: utf-8

from collections import Iterable
import os
import re
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)

if sys.version_info.major == 2:
	PATH = os.path.dirname(os.path.abspath(__file__))
	PYTHON_PATH = os.path.join(PATH, 'python2')
	sys.path.insert(0, PYTHON_PATH)
	sys.path.insert(0, PATH)
	import cgi
	import xml
	from xml.etree import ElementTree as ET
elif sys.version_info.major >= 3:
	PATH = os.path.dirname(os.path.abspath(__file__))
	PYTHON_PATH = os.path.join(PATH, 'python3')
	sys.path.insert(0, PYTHON_PATH)
	sys.path.insert(0, PATH)
	import cgi
	import globalPlugins.MathMlReader.python3.xml as xml
	from globalPlugins.MathMlReader.python3.xml.etree import ElementTree as ET

if sys.version_info.major == 2:
	import A8M_PM_2 as A8M_PM
	from A8M_PM_2 import create_node, MathContent
elif sys.version_info.major >= 3:
	import A8M_PM_3 as A8M_PM
	from A8M_PM_3 import create_node, MathContent

from utils import convert_bool

import addonHandler
import api
import config
import controlTypes
import eventHandler
import globalPlugins
import globalPluginHandler
import globalVars
import gui
from keyboardHandler import KeyboardInputGesture
from logHandler import log
import mathPres
from mathPres.mathPlayer import MathPlayer
import speech
import textInfos
import textInfos.offsets
import ui
import wx
import wxgui

if sys.version_info.major == 2:
	string_types = basestring
	unicode = unicode
elif sys.version_info.major >= 3:
	string_types = str
	unicode = str


try:
	from scriptHandler import script
except:
	def script(**kwargs):
		def script_decorator(decoratedScript):
			return decoratedScript
		return script_decorator
try:
	addonHandler.initTranslation()
except:
	_ = lambda x : x
try:
	ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]
	ADDON_PANEL_TITLE = str(ADDON_SUMMARY) if sys.version_info.major >= 3 else unicode(ADDON_SUMMARY)
except:
	ADDON_PANEL_TITLE = ADDON_SUMMARY = 'focusHighlight'

def mathml2etree(mathml):
	"""
	Convert mathml to XML etree object
	@param mathml: source mathml
	@type mathml: str
	@rtype: XML etree
	"""
	gtlt_pattern = re.compile(r"([\>])(.*?)([\<])")
	if sys.version_info.major == 2:
		import HTMLParser
		mathml = gtlt_pattern.sub(
						lambda m: m.group(1) +cgi.escape(HTMLParser.HTMLParser().unescape(m.group(2))) +m.group(3),
						mathml
		)
	elif sys.version_info.major >= 3:
		import html
		mathml = gtlt_pattern.sub(
						lambda m: m.group(1) +cgi.escape(html.unescape(m.group(2))) +m.group(3),
						mathml
		)

	quote_pattern = re.compile(r"=([\"\'])(.*?)\1")
	mathml = quote_pattern.sub(lambda m: '=' +m.group(1) +cgi.escape(m.group(2)) +m.group(1), mathml)
	parser = ET.XMLParser()
	try:
		tree = ET.fromstring(mathml.encode('utf-8'), parser=parser)
	except BaseException as error:
		raise SystemError(error)
	return tree

def flatten(lines):
	"""
	convert tree to linear using generator
	@param lines:
	@type list
	@rtype
	"""
	for line in lines:
		if isinstance(line, Iterable) and not isinstance(line, string_types):
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
			command = speech.BreakCommand(time=int(time) +int(os.environ['item_interval_time']))
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
				sequence = sequence +unicode(r)
			sequence = sequence +u' '

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

class InteractionFrame(wxgui.GenericFrame):
	def __init__(self, obj):
		self.obj = obj
		title = _("Access8Math interaction window")
		super(InteractionFrame, self).__init__(wx.GetApp().TopWindow, title=title)

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
		self.Close(True)  # Close the frame.

	def OnInteraction(self, event):
		self.obj.parent = api.getFocusObject()

		# 用ctrl+m 出現的互動視窗會朗讀原始程式的視窗資訊
		def event_focusEntered(self):
			if self.role in (controlTypes.ROLE_MENUBAR, controlTypes.ROLE_POPUPMENU, controlTypes.ROLE_MENUITEM):
				speech.cancelSpeech()
				return
			#if self.isPresentableFocusAncestor:
				#speech.speakObject(self,reason=controlTypes.REASON_FOCUSENTERED)

		#import NVDAObjects
		#old_event_focusEntered = NVDAObjects.NVDAObject.event_focusEntered
		#NVDAObjects.NVDAObject.event_focusEntered = event_focusEntered
		#eventHandler.executeEvent("gainFocus", self.obj)
		self.obj.setFocus()
		#NVDAObjects.NVDAObject.event_focusEntered = old_event_focusEntered

	def OnRawdataToClip(self, event):
		#api.copyToClip(self.obj.raw_data)
		api.copyToClip(self.obj.mathcontent.root.get_mathml())
		ui.message(_("copy"))

	def OnInsert(self, event):
		# asciimath to mathml
		from xml.etree.ElementTree import tostring
		import asciimathml
		from dialogs import AsciiMathEntryDialog
		entryDialog = AsciiMathEntryDialog(self)
		if entryDialog.ShowModal() == wx.ID_OK:
			asciimath = entryDialog.GetValue()
			mathml = tostring(asciimathml.parse(asciimath))
			mathml = mathml.replace('math>', 'mrow>')

			tree = mathml2etree(mathml)

			node = create_node(tree)
			self.obj.mathcontent.insert(node)

class MathMlTextInfo(textInfos.offsets.OffsetsTextInfo):

	def __init__(self, obj, position):
		super(MathMlTextInfo, self).__init__(obj, position)
		self.obj = obj

	def _getStoryLength(self):
		serializes = self.obj.mathcontent.pointer.serialized()
		return len(translate_Unicode(serializes))

	def _getStoryText(self):
		"""Retrieve the entire text of the object.
		@return: The entire text of the object.
		@rtype: unicode
		"""
		serializes = self.obj.mathcontent.pointer.serialized()
		return translate_Unicode(serializes)

	def _getTextRange(self, start, end):
		"""Retrieve the text in a given offset range.
		@param start: The start offset.
		@type start: int
		@param end: The end offset (exclusive).
		@type end: int
		@return: The text contained in the requested range.
		@rtype: unicode
		"""
		text = self._getStoryText()
		return text[start:end] if text else u""

class MathMlReader(mathPres.MathPresentationProvider):

	def __init__(self, *args, **kwargs):
		super(MathMlReader, self).__init__(*args, **kwargs)
		self.mathcontent = None

	def getSpeechForMathMl(self, mathMl):
		tree = mathml2etree(mathMl)
		self.mathcontent = MathContent(A8M_PM.mathrule, tree)
		globalVars.mathcontent = self.mathcontent
		return translate_SpeechCommand(self.mathcontent.pointer.serialized())

	def interactWithMathMl(self, mathMl):
		MathMlReaderInteraction(mathMl=mathMl)

class MathMlReaderInteraction(mathPres.MathInteractionNVDAObject):

	def __init__(self, mathMl, interaction_frame=False):
		super(MathMlReaderInteraction, self).__init__(mathMl=mathMl)

		tree = mathml2etree(mathMl)
		globalVars.math_obj = self
		self.mathcontent = MathContent(A8M_PM.mathrule, tree)
		globalVars.mathcontent = self.mathcontent
		self.raw_data = mathMl
		api.setReviewPosition(self.makeTextInfo(), False)

		self.interactionFrame = None
		if convert_bool(os.environ['IFS']) or interaction_frame:
			self.interactionFrame = InteractionFrame(self)
			self.interactionFrame.Show()
			self.interactionFrame.Raise()
		self.setFocus()

	def _get_mathMl(self):
		return self.mathcontent.root.get_mathml()
		#return self.raw_data

	def makeTextInfo(self, position=textInfos.POSITION_FIRST):
		return MathMlTextInfo(self, position)

	def event_gainFocus(self):
		speech.speak([_("enter interaction mode")])
		super(MathMlReaderInteraction, self).event_gainFocus()
		api.setReviewPosition(self.makeTextInfo(), False)

	#def event_loseFocus(self):
		#pass

	def reportFocus(self):
		#super(MathMlReaderInteraction, self).reportFocus()
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
		return super(MathMlReaderInteraction, self).getScript(gesture)

	def script_navigate(self, gesture):
		r = False
		if gesture.mainKeyName in ["downArrow", "upArrow", "leftArrow", "rightArrow", "home"]:
			r = self.mathcontent.navigate(gesture.mainKeyName)

		if r:
			api.setReviewPosition(self.makeTextInfo(), False)
			if self.mathcontent.pointer.parent:
				if convert_bool(os.environ['AG']) and self.mathcontent.pointer.parent.role_level == A8M_PM.AUTO_GENERATE:
					speech.speak([self.mathcontent.pointer.des])
				elif convert_bool(os.environ['DG']) and self.mathcontent.pointer.parent.role_level == A8M_PM.DIC_GENERATE:
					speech.speak([self.mathcontent.pointer.des])
			else:
				speech.speak([self.mathcontent.pointer.des])
			speech.speak(translate_SpeechCommand(self.mathcontent.pointer.serialized()))
		else:
			speech.speak([_("not move")])

	@script(
		gesture="kb:control+c",
		description=_("copy mathml"),
		category=ADDON_SUMMARY,
	)
	def script_rawdataToClip(self, gesture):
		#api.copyToClip(self.raw_data)
		api.copyToClip(self.mathcontent.root.get_mathml())
		ui.message(_("copy"))

	@script(
		gesture="kb:control+s",
		description=_("snapshot"),
		category=ADDON_SUMMARY,
	)
	def script_snapshot(self, gesture):
		globalVars.math_obj = self
		ui.message(_("snapshot"))

	@script(
		gesture="kb:control+i",
		description=_("Insert math object"),
		category=ADDON_SUMMARY,
	)
	def script_insert(self, gesture):
		wx.CallAfter(self.interactionFrame.OnInsert, None)

	@script(
		gesture="kb:control+d",
		description=_("Delete math object"),
		category=ADDON_SUMMARY,
	)
	def script_delete(self, gesture):
		self.mathcontent.delete()

	@script(
		gesture="kb:control+m",
		description=_("Show Access8Math interaction window"),
		category=ADDON_SUMMARY,
	)
	def script_showMenu(self, gesture):
		if not self.interactionFrame:
			MathMlReaderInteraction(mathMl=self.raw_data, interaction_frame=True)
		else:
			ui.message(_("Access8Math interaction window already showed"))

try:
	config.conf["Access8Math"]
except:
	config.conf["Access8Math"] = {}

provider_list = [
	MathMlReader,
]

try:
	reader = MathPlayer()
	provider_list.append(MathPlayer)
	mathPres.registerProvider(reader, speech=True, braille=True, interaction=True)
except:
	log.warning("MathPlayer 4 not available")

try:
	if config.conf["Access8Math"]["provider"] == "MathMlReader":
		provider = MathMlReader
	elif config.conf["Access8Math"]["provider"] == "MathPlayer":
		provider = MathPlayer
	else:
		config.conf["Access8Math"]["provider"] = "MathMlReader"
		provider = MathMlReader
except:
	config.conf["Access8Math"]["provider"] = "MathMlReader"
	provider = MathMlReader

try:
	reader = provider()
	config.conf["Access8Math"]["provider"] = reader.__class__.__name__
except:
	provider = MathMlReader
	reader = provider()
	config.conf["Access8Math"]["provider"] = reader.__class__.__name__

mathPres.registerProvider(reader, speech=True, braille=False, interaction=True)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		xml_NVDA = sys.modules['xml']
		sys.modules['xml'] = globalPlugins.MathMlReader.xml

		import configure
		configure.environ_from_config()
		A8M_PM.config_from_environ()
		self.language = os.environ['LANGUAGE']
		self.create_menu()

	def create_menu(self):
		self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu
		self.menu = wx.Menu()

		# add
		self.generalSettings = self.menu.Append(
			wx.ID_ANY,
			_("&General settings...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onGeneralSettings, self.generalSettings)

		# add
		self.ruleSettings = self.menu.Append(
			wx.ID_ANY,
			_("&Rule settings...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onRuleSettings, self.ruleSettings)

		# add
		self.unicodeDictionary = self.menu.Append(
			wx.ID_ANY,
			_("&unicode dictionary...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onUnicodeDictionary, self.unicodeDictionary)

		# add
		self.mathRule = self.menu.Append(
			wx.ID_ANY,
			_("&math rule...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onMathRule, self.mathRule)

		# add
		self.newLanguageAdding = self.menu.Append(
			wx.ID_ANY,
			_("&New language adding...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onNewLanguageAdding, self.newLanguageAdding)

		'''# add
		self.asciiMath = self.menu.Append(
			wx.ID_ANY,
			_("&asciimath...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onAsciiMathAdd, self.asciiMath)

		# add
		self.latex = self.menu.Append(
			wx.ID_ANY,
			_("&latex...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onLatexAdd, self.latex)'''

		# add
		self.about = self.menu.Append(
			wx.ID_ANY,
			_("&About...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onAbout, self.about)

		self.Access8Math_item = self.toolsMenu.AppendSubMenu(self.menu, _("Access8Math"), _("Access8Math"))

	def terminate(self):
		try:
			self.toolsMenu.RemoveItem(self.Access8Math_item)
		except (RuntimeError, AttributeError, wx.PyDeadObjectError):
			pass

	@script(
		gesture="kb:control+alt+m",
		description=_("Change mathml provider"),
		category=ADDON_SUMMARY,
	)
	def script_change_provider(self, gesture):
		try:
			if config.conf["Access8Math"]["provider"] == "MathMlReader":
				provider = MathPlayer
			elif config.conf["Access8Math"]["provider"] == "MathPlayer":
				provider = MathMlReader
			else:
				provider = MathMlReader
		except:
			config.conf["Access8Math"]["provider"] = "MathMlReader"
			provider = MathMlReader

		try:
			reader = provider()
			config.conf["Access8Math"]["provider"] = reader.__class__.__name__
		except:
			provider = MathMlReader
			reader = provider()
			config.conf["Access8Math"]["provider"] = reader.__class__.__name__

		mathPres.registerProvider(reader, speech=True, braille=False, interaction=True)

		ui.message(_("mathml provider change to %s")%config.conf["Access8Math"]["provider"])

	@script(
		description=_("Shows the Access8Math settings dialog."),
		category=ADDON_SUMMARY,
	)
	def script_settings(self, gesture):
		wx.CallAfter(self.onGeneralSettings, None)

	def onGeneralSettings(self, evt):
		from dialogs import GeneralSettingsDialog
		gui.mainFrame._popupSettingsDialog(GeneralSettingsDialog)

	def onRuleSettings(self, evt):
		from dialogs import RuleSettingsDialog
		gui.mainFrame._popupSettingsDialog(RuleSettingsDialog)

	def onNewLanguageAdding(self, evt):
		from dialogs import NewLanguageAddingDialog
		NewLanguageAddingDialog(gui.mainFrame).Show()

	def onUnicodeDictionary(self, evt):
		self.language = os.environ['LANGUAGE']
		from dialogs import UnicodeDicDialog
		gui.mainFrame._popupSettingsDialog(UnicodeDicDialog, self.language)

	def onMathRule(self, evt):
		self.language = os.environ['LANGUAGE']
		from dialogs import MathRuleDialog
		gui.mainFrame._popupSettingsDialog(MathRuleDialog, self.language)

	def onAbout(self, evt):
		aboutMessage = _(
u"""Access8Math
Version: 2.3
URL: https://addons.nvda-project.org/addons/access8math.en.html
Copyright (C) 2017-2018 Access8Math Contributors
Access8Math is covered by the GNU General Public License (Version 2). You are free to share or change this software in any way you like as long as it is accompanied by the license and you make all source code available to anyone who wants it. This applies to both original and modified copies of this software, plus any derivative works.
It can be viewed online at: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
Access8Math has been sponsored by "Taiwan Visually Impaired People Association"(vipastaiwan@gmail.com) in 2018, hereby express our sincere appreciation.
If you feel this add-on is helpful, please don't hesitate to give support to "Taiwan Visually Impaired People Association" and authors."""
		)
		gui.messageBox(aboutMessage, _("About Access8Math"), wx.OK)

	def onAsciiMathAdd(self, evt):
		from xml.etree.ElementTree import tostring
		import asciimathml
		from dialogs import AsciiMathEntryDialog
		entryDialog = AsciiMathEntryDialog(gui.mainFrame)
		if entryDialog.ShowModal() == wx.ID_OK:
			asciimath = entryDialog.GetValue()
			mathml = tostring(asciimathml.parse(asciimath))
			mathml = unicode(mathml)
			MathMlReaderInteraction(mathMl=mathml, interaction_frame=True)

	def onLatexAdd(self, evt):
		import latex2mathml.converter
		from dialogs import LatexEntryDialog
		entryDialog = LatexEntryDialog(gui.mainFrame)
		if entryDialog.ShowModal() == wx.ID_OK:
			latex = entryDialog.GetValue()
			mathml = latex2mathml.converter.convert(latex)
			if sys.version_info.major == 2:
				import HTMLParser
				mathml = HTMLParser.HTMLParser().unescape(mathml)
			elif sys.version_info.major >= 3:
				import html
				mathml = html.unescape(mathml)

			MathMlReaderInteraction(mathMl=mathml, interaction_frame=True)
