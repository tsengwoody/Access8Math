# coding: utf-8
# Access8Math: Allows access math content written by MathML in NVDA
# Copyright (C) 2017-2018 Tseng Woody <tsengwoody.tw@gmail.com>
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.

from collections import Iterable, OrderedDict
import os
import re
import sys
path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path)
Base_Dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, Base_Dir)
import cgi
import HTMLParser
import xml
from xml.etree import ElementTree as ET

import A8M_PM
from A8M_PM import MathContent
import dialogs
from utils import convert_bool

import addonHandler
addonHandler.initTranslation()
import api
import config
import eventHandler
import globalPlugins
import globalPluginHandler
import globalVars
import globalCommands
from globalCommands import SCRCAT_CONFIG
import gui
from gui import guiHelper
from gui.settingsDialogs import SettingsDialog
from keyboardHandler import KeyboardInputGesture
from logHandler import log
import mathPres
from mathPres.mathPlayer import MathPlayer
import speech
import textInfos
import textInfos.offsets
import tones
import ui
import wx

import wxgui

def event_focusEntered(self):
	if self.role in (controlTypes.ROLE_MENUBAR,controlTypes.ROLE_POPUPMENU,controlTypes.ROLE_MENUITEM):
		speech.cancelSpeech()
		return
	#if self.isPresentableFocusAncestor:
		#speech.speakObject(self,reason=controlTypes.REASON_FOCUSENTERED)

def mathml2etree(mathMl):
	gtlt_pattern = re.compile(ur"([\>])(.*?)([\<])")
	mathMl = gtlt_pattern.sub(lambda m: m.group(1) +cgi.escape(HTMLParser.HTMLParser().unescape(m.group(2))) +m.group(3), mathMl)
	quote_pattern = re.compile(ur"=([\"\'])(.*?)\1")
	mathMl = quote_pattern.sub(lambda m: '=' +m.group(1) +cgi.escape(m.group(2)) +m.group(1), mathMl)
	parser = ET.XMLParser()
	try:
		tree = ET.fromstring(mathMl.encode('utf-8'), parser=parser)
	except BaseException as e:
		raise SystemError(e)
	return tree

def flatten(l):
	for el in l:
		if isinstance(el, Iterable) and not isinstance(el, basestring):
			for sub in flatten(el):
				yield sub
		else:
			yield el

def translate_SpeechCommand(serializes):
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
	pattern = re.compile(ur'[ ]+')
	sequence = pattern.sub(lambda m: u' ', sequence)

	# replace blank line to none
	pattern = re.compile(ur'\n\s*\n')
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
		super(InteractionFrame, self).__init__(wx.GetApp().TopWindow, title=_("Access8Math interaction window"))

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

	def OnExit(self,event):
		self.Close(True)  # Close the frame.

	def OnInteraction(self,event):
		self.obj.parent = api.getFocusObject()
		#import NVDAObjects
		#old_event_focusEntered = NVDAObjects.NVDAObject.event_focusEntered
		#NVDAObjects.NVDAObject.event_focusEntered = event_focusEntered
		eventHandler.executeEvent("gainFocus", self.obj)
		#NVDAObjects.NVDAObject.event_focusEntered = old_event_focusEntered

	def OnRawdataToClip(self,event):
		#api.copyToClip(self.obj.raw_data)
		api.copyToClip(self.obj.mathcontent.root.get_mathml())
		ui.message(_("copy"))

	def OnInsert(self,event):
		# asciimath to mathml
		from xml.etree.ElementTree import tostring
		import asciimathml
		from dialogs import AsciiMathEntryDialog
		entryDialog = AsciiMathEntryDialog(self)
		if entryDialog.ShowModal()==wx.ID_OK:
			asciimath = entryDialog.GetValue()
			mathMl = tostring(asciimathml.parse(asciimath))
			mathMl = mathMl.replace('math>', 'mrow>')

			tree = mathml2etree(mathMl)

			from A8M_PM import create_node
			node = create_node(tree)
			self.obj.mathcontent.insert(node)

class MathMlTextInfo(textInfos.offsets.OffsetsTextInfo):

	def __init__(self,obj,position):
		super(MathMlTextInfo,self).__init__(obj,position)
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

	def _getTextRange(self,start,end):
		"""Retrieve the text in a given offset range.
		@param start: The start offset.
		@type start: int
		@param end: The end offset (exclusive).
		@type end: int
		@return: The text contained in the requested range.
		@rtype: unicode
		"""
		text=self._getStoryText()
		return text[start:end] if text else u""

class MathMlReader(mathPres.MathPresentationProvider):

	def getSpeechForMathMl(self, mathMl):
		tree = mathml2etree(mathMl)
		self.mathcontent = MathContent(A8M_PM.mathrule , tree)
		globalVars.mathcontent = self.mathcontent
		return translate_SpeechCommand(self.mathcontent.pointer.serialized())

	def interactWithMathMl(self, mathMl):
		MathMlReaderInteraction(mathMl=mathMl)

class MathMlReaderInteraction(mathPres.MathInteractionNVDAObject):

	def __init__(self, mathMl, show=False):
		super(MathMlReaderInteraction, self).__init__(mathMl=mathMl)

		tree = mathml2etree(mathMl)
		globalVars.math_obj = self
		self.mathcontent = MathContent(A8M_PM.mathrule , tree)
		globalVars.mathcontent = self.mathcontent
		self.raw_data = mathMl
		api.setReviewPosition(self.makeTextInfo(), False)

		self.interactionFrame = InteractionFrame(self)
		if True:
			self.interactionFrame.Show()
			self.interactionFrame.Raise()
		else:
			#api.setFocusObject(self)
			eventHandler.executeEvent("gainFocus", self)

	def _get_mathMl(self):
		return self.mathcontent.root.get_mathml()
		#return self.raw_data

	def makeTextInfo(self, position=textInfos.POSITION_FIRST):
		return MathMlTextInfo(self, position)

	def event_gainFocus(self):
		speech.speak(_("enter interaction mode"))
		super(MathMlReaderInteraction, self).event_gainFocus()
		api.setReviewPosition(self.makeTextInfo(), False)

	'''def event_loseFocus(self):
		print('QQ')'''

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
			#or len(gesture.mainKeyName) == 1
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

	def script_rawdataToClip(self, gesture):
		#api.copyToClip(self.raw_data)
		api.copyToClip(self.mathcontent.root.get_mathml())
		ui.message(_("copy"))

	def script_snapshot(self, gesture):
		globalVars.math_obj = self
		ui.message(_("snapshot"))

	def script_insert(self, gesture):
		wx.CallAfter(self.interactionFrame.OnInsert, None)

	def script_delete(self, gesture):
		self.mathcontent.delete()

	def script_showMenu(self, gesture):
		self.interactionFrame.Show()
		self.interactionFrame.Raise()
		ui.message(_("show menu"))

	__gestures={
		"kb:control+c": "rawdataToClip",
		""""kb:control+s": "snapshot",
		"kb:control+i": "insert",
		"kb:control+d": "delete","""
		"kb:control+m": "showMenu",
	}

provider_list = [
	u"MathMlReader",
]

try:
	reader = MathPlayer()
	provider_list.append(u"MathPlayer")
	mathPres.registerProvider(reader, speech=True, braille=True, interaction=True)
except:
	log.warning("MathPlayer 4 not available")

try:
	index = provider_list.index(config.conf["Access8Math"]["provider"])% len(provider_list)
except:
	config.conf["Access8Math"]["provider"] = "MathMlReader"
	index = provider_list.index(config.conf["Access8Math"]["provider"])% len(provider_list)

try:
	exec(
		'reader = {}()'.format(provider_list[index])
	)
	config.conf["Access8Math"]["provider"] = reader.__class__.__name__
except:
	log.warning("{} not available".format(provider_list[index]))
mathPres.registerProvider(reader, speech=True, braille=False, interaction=True)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = _("Access8Math")

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		xml_NVDA = sys.modules['xml']
		sys.modules['xml'] = globalPlugins.MathMlReader.xml

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

	def script_change_provider(self, gesture):
		try:
			index = (provider_list.index(config.conf["Access8Math"]["provider"]) +1)% len(provider_list)
		except:
			config.conf["Access8Math"]["provider"] = reader.__class__.__name__
			index = (provider_list.index(config.conf["Access8Math"]["provider"]) +1)% len(provider_list)

		try:
			exec(
				'reader = {}()'.format(provider_list[index])
			)
		except:
			log.warning("{} not available".format(provider_list[index]))
		mathPres.registerProvider(reader, speech=True, braille=False, interaction=True)
		ui.message(_("mathml provider change to %s")%config.conf["Access8Math"]["provider"])
	script_change_provider.category = scriptCategory
	# Translators: message presented in input mode.
	script_change_provider.__doc__ = _("Change mathml provider")

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

	def onAbout(self,evt):
		import gui
		# Translators: The title of the dialog to show about info for NVDA.
		aboutMessage = _(
u"""Access8Math
Version: 2.1
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
		if entryDialog.ShowModal()==wx.ID_OK:
			asciimath = entryDialog.GetValue()
			mathml = tostring(asciimathml.parse(asciimath))
			mathml = unicode(mathml)
			MathMlReaderInteraction(mathMl=mathml, show=True)

	def onLatexAdd(self, evt):
		import latex2mathml.converter
		from dialogs import LatexEntryDialog
		entryDialog = LatexEntryDialog(gui.mainFrame)
		if entryDialog.ShowModal()==wx.ID_OK:
			latex = entryDialog.GetValue()
			mathml = latex2mathml.converter.convert(latex)
			print type(mathml)
			mathml = HTMLParser.HTMLParser().unescape(mathml)
			print type(mathml)
			MathMlReaderInteraction(mathMl=mathml, show=True)

	def script_settings(self, gesture):
		wx.CallAfter(self.onSettings, None)
	script_settings.category = scriptCategory
	# Translators: message presented in input mode.
	script_settings.__doc__ = _("Shows the Access8Math settings dialog.")

	__gestures={
		"kb:control+alt+m": "change_provider",
	}
