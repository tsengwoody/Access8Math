# coding: utf-8
# Access8Math: Allows access math content written by MathML in NVDA
# Copyright (C) 2017-2018 Tseng Woody <tsengwoody.tw@gmail.com>
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.

from collections import OrderedDict
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

import addonHandler
addonHandler.initTranslation()
import api
from brailleInput import BrailleInputGesture
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

from languageHandler_custom import getAvailableLanguages
import wxgui

def translate_SpeechCommand(serializes):
	pattern = re.compile(r'[@](?P<time>[\d]*)[@]')
	speechSequence = []
	for r in serializes:
		time_search = pattern.search(r)
		try:
			time = time_search.group('time')
			command = speech.BreakCommand(time=int(time)+90)
			speechSequence.append(command)
		except:
			speechSequence.append(r)

	return speechSequence

def translate_Unicode(serializes):
	pattern = re.compile(r'[@](?P<time>[\d]*)[@]')
	sequence = ''
	for r in serializes:
		time_search = pattern.search(r)
		try:
			time = time_search.group('time')
		except:
			sequence = sequence +unicode(r)
		sequence = sequence +u' '
	pattern = re.compile(ur'[ ]+')
	sequence = pattern.sub(lambda m: u' ', sequence)
	return sequence.strip()

class InteractionFrame(wxgui.GenericFrame):
	def __init__(self, obj):
		self.obj = obj
		super(InteractionFrame, self).__init__(wx.GetApp().TopWindow, title=_("Access8Math interaction window"))

	def menuData(self):
		return [
			(_("&Menu"), (
				(_("&About"),_("Information about this program"), self.OnAbout),
				(_("&Exit"),_("Terminate the program"), self.OnExit),
			))
		]

	def buttonData(self):
		return (
			(_("interaction"), self.OnInteraction),
			(_("copy"), self.OnRawdataToClip),
		)

	def OnNew(self, event): pass
	def OnOpen(self, event): pass
	def OnSave(self, event): pass
	def OnColor(self, event): pass
	def OnAbout(self, event): pass
	def OnExit(self,event):
		self.Close(True)  # Close the frame.

	def OnInteraction(self,event):
		self.obj.interactionFrameNVDAobj = self.obj.parent = api.getFocusObject()
		eventHandler.executeEvent("gainFocus", self.obj)

	def OnRawdataToClip(self,event):
		api.copyToClip(self.obj.raw_data)
		ui.message(_("copy"))

class GeneralSettingsDialog(SettingsDialog):
	# Translators: Title of the Access8MathDialog.
	title = _("General Settings")
	CheckBox_settings = OrderedDict([
		("AMM", _("Analyze mathematical meaning of content")),
		("DG", _("Read defined meaning in dictionary")),
		("AG", _("Read of auto-generated meaning")),
	])

	def makeSettings(self, settingsSizer):
		global language
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		languageLabel = _("&Language:")
		self.languageChoices = available_languages_long
		self.languageList = sHelper.addLabeledControl(languageLabel, wx.Choice, choices=self.languageChoices)
		try:
			index = available_languages_short.index(language)
		except:
			initialize_config()
			index = available_languages_short.index(language)
		self.languageList.Selection = index

		for k,v in self.CheckBox_settings.items():
			setattr(self, k +"CheckBox", sHelper.addItem(wx.CheckBox(self, label=v)))
			getattr(self, k +"CheckBox").SetValue(globals()[k])

	def postInit(self):
		self.languageList.SetFocus()

	def onOk(self,evt):
		super(GeneralSettingsDialog, self).onOk(evt)

		global language
		os.environ['LANGUAGE'] = language
		for k in self.CheckBox_settings.keys():
			globals()[k] = getattr(self, k +"CheckBox").IsChecked()
			os.environ[k] = unicode(globals()[k])

		try:
			config.conf["Access8Math"]["language"] = language = available_languages_short[self.languageList.GetSelection()]
			for k in self.CheckBox_settings.keys():
				config.conf["Access8Math"][k] = unicode(globals()[k])
		except:
			initialize_config()
			config.conf["Access8Math"]["language"] = language = available_languages_short[self.languageList.GetSelection()]
			for k in self.CheckBox_settings.keys():
				config.conf["Access8Math"][k] = unicode(globals()[k])

		A8M_PM.config_from_environ()

		try:
			api.setReviewPosition(MathMlTextInfo(globalVars.math_obj, textInfos.POSITION_FIRST), False)
		except:
			pass

class RuleSettingsDialog(SettingsDialog):
	# Translators: Title of the Access8MathDialog.
	title = _("Rule Settings")
	CheckBox_settings = OrderedDict([
		("SingleMsubsupType", _("Simplified subscript and superscript")),
		("SingleMsubType", _("Simplified subscript")),
		("SingleMsupType", _("Simplified superscript")),
		("SingleMunderoverType", _("Simplified underscript and overscript")),
		("SingleMunderType", _("Simplified underscript")),
		("SingleMoverType", _("Simplified overscript")),
		("SingleFractionType", _("Simplified fraction")),
		("SingleSqrtType", _("Simplified square root")),
		("PowerType", _("Power")),
		("SquarePowerType", _("Square power")),
		("CubePowerType", _("Cube power")),
		("SetType", _("Set")),
		("AbsoluteType", _("Absolute value")),
		("MatrixType", _("Matrix")),
		("DeterminantType", _("Determinant")),
		("AddIntegerFractionType", _("Integer and fraction")),
	])

	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		for k,v in self.CheckBox_settings.items():
			setattr(self, k +"CheckBox", sHelper.addItem(wx.CheckBox(self, label=v)))
			getattr(self, k +"CheckBox").SetValue(globals()[k])

	def postInit(self):
		getattr(self, self.CheckBox_settings.keys()[0] +"CheckBox").SetFocus()

	def onOk(self,evt):
		super(RuleSettingsDialog, self).onOk(evt)

		for k in self.CheckBox_settings.keys():
			globals()[k] = getattr(self, k +"CheckBox").IsChecked()
			os.environ[k] = unicode(globals()[k])

		try:
			for k in self.CheckBox_settings.keys():
				config.conf["Access8Math"][k] = unicode(globals()[k])
		except:
			initialize_config()
			for k in self.CheckBox_settings.keys():
				config.conf["Access8Math"][k] = unicode(globals()[k])

		A8M_PM.config_from_environ()

		try:
			api.setReviewPosition(MathMlTextInfo(globalVars.math_obj, textInfos.POSITION_FIRST), False)
		except:
			pass

class MathMlTextInfo(textInfos.offsets.OffsetsTextInfo):

	def __init__(self,obj,position):
		super(MathMlTextInfo,self).__init__(obj,position)
		self.obj = obj

	def _getStoryLength(self):
		serializes = self.obj.pointer.serialized()
		return len(translate_Unicode(serializes))

	def _getStoryText(self):
		"""Retrieve the entire text of the object.
		@return: The entire text of the object.
		@rtype: unicode
		"""
		serializes = self.obj.pointer.serialized()
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
		gtlt_pattern = re.compile(ur"([\>])(.*?)([\<])")
		mathMl = gtlt_pattern.sub(lambda m: m.group(1) +cgi.escape(HTMLParser.HTMLParser().unescape(m.group(2))) +m.group(3), mathMl)
		quote_pattern = re.compile(ur"=([\"\'])(.*?)\1")
		mathMl = quote_pattern.sub(lambda m: '=' +m.group(1) +cgi.escape(m.group(2)) +m.group(1), mathMl)
		parser = ET.XMLParser()
		try:
			tree = ET.fromstring(mathMl.encode('utf-8'), parser=parser)
		except BaseException as e:
			globalVars.raw_data = mathMl
			raise SystemError(e)
		node = create_node(tree)
		globalVars.nodes = node
		return translate_SpeechCommand(node.serialized())

	def interactWithMathMl(self, mathMl):
		MathMlReaderInteraction(provider=self, mathMl=mathMl)

class MathMlReaderInteraction(mathPres.MathInteractionNVDAObject):

	def __init__(self, provider=None, mathMl=None):
		super(MathMlReaderInteraction, self).__init__(provider=provider, mathMl=mathMl)

		gtlt_pattern = re.compile(ur"([\>])(.*?)([\<])")
		mathMl = gtlt_pattern.sub(lambda m: m.group(1) +cgi.escape(HTMLParser.HTMLParser().unescape(m.group(2))) +m.group(3), mathMl)
		quote_pattern = re.compile(ur"=([\"\'])(.*?)\1")
		mathMl = quote_pattern.sub(lambda m: '=' +m.group(1) +cgi.escape(m.group(2)) +m.group(1), mathMl)
		parser = ET.XMLParser()
		try:
			tree = ET.fromstring(mathMl.encode('utf-8'), parser=parser)
		except BaseException as e:
			globalVars.raw_data = mathMl
			raise SystemError(e)
		globalVars.root = self.root = self.pointer = create_node(tree)
		self.raw_data = mathMl
		api.setReviewPosition(self.makeTextInfo(), False)

		self.interactionFrame = InteractionFrame(self)
		self.interactionFrame.Show()
		self.interactionFrame.Raise()

	def _get_mathMl(self):
		return self.raw_data

	def makeTextInfo(self, position=textInfos.POSITION_FIRST):
		return MathMlTextInfo(self, position)

	'''def event_gainFocus(self):
	def event_loseFocus(self):'''

	def reportFocus(self):
		super(MathMlReaderInteraction, self).reportFocus()
		speech.speak(translate_SpeechCommand(self.root.serialized()))
		api.setReviewPosition(self.makeTextInfo(), False)

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
		r = None
		if gesture.mainKeyName == "downArrow":
			r = self.pointer.down()
		elif gesture.mainKeyName == "upArrow":
			r = self.pointer.up()
		elif gesture.mainKeyName == "leftArrow":
			r = self.pointer.previous_sibling
		elif gesture.mainKeyName == "rightArrow":
			r = self.pointer.next_sibling
		elif gesture.mainKeyName == "home":
			r = self.root

		if r is not None:
			self.pointer = r
			api.setReviewPosition(self.makeTextInfo(), False)
			if self.pointer.parent:
				if AG and self.pointer.parent.role_level == A8M_PM.AUTO_GENERATE:
					speech.speak([self.pointer.des])
				elif DG and self.pointer.parent.role_level == A8M_PM.DIC_GENERATE:
					speech.speak([self.pointer.des])
			else:
					speech.speak([self.pointer.des])
			speech.speak(translate_SpeechCommand(self.pointer.serialized()))
		else:
			speech.speak([_("not move")])

	def script_rawdataToClip(self, gesture):
		api.copyToClip(self.raw_data)
		ui.message(_("copy"))

	def script_snapshot(self, gesture):
		globalVars.math_obj = self
		ui.message(_("snapshot"))

	__gestures={
		"kb:control+c": "rawdataToClip",
		"kb:control+s": "snapshot",
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

def initialize_config():
	config.conf["Access8Math"] = {}
	config.conf["Access8Math"]["language"] = "Windows"
	config.conf["Access8Math"]["provider"] = "MathMlReader"
	for k in GeneralSettingsDialog.CheckBox_settings.keys() +RuleSettingsDialog.CheckBox_settings.keys():
		config.conf["Access8Math"][k] = u"True"
	tones.beep(100,100)

try:
	index = provider_list.index(config.conf["Access8Math"]["provider"])% len(provider_list)
except:
	initialize_config()
	index = provider_list.index(config.conf["Access8Math"]["provider"])% len(provider_list)

try:
	exec(
		'reader = {}()'.format(provider_list[index])
	)
	config.conf["Access8Math"]["provider"] = reader.__class__.__name__
except:
	log.warning("{} not available".format(provider_list[index]))
mathPres.registerProvider(reader, speech=True, braille=False, interaction=True)

try:
	available_languages = getAvailableLanguages(path)
	available_languages = available_languages[:-1]
except:
	available_languages = []

available_languages.append(("Windows", _("build-in")))
available_languages_short = [i[0] for i in available_languages]
available_languages_long = [i[1] for i in available_languages]

try:
	language = config.conf["Access8Math"]["language"]
	for k in GeneralSettingsDialog.CheckBox_settings.keys() +RuleSettingsDialog.CheckBox_settings.keys():
		globals()[k] = True if config.conf["Access8Math"][k] in [u'True', u'true', True] else False
except:
	initialize_config()
	language = config.conf["Access8Math"]["language"]
	for k in GeneralSettingsDialog.CheckBox_settings.keys() +RuleSettingsDialog.CheckBox_settings.keys():
		globals()[k] = True if config.conf["Access8Math"][k] in [u'True', u'true', True] else False

os.environ['LANGUAGE'] = language
for k in GeneralSettingsDialog.CheckBox_settings.keys() +RuleSettingsDialog.CheckBox_settings.keys():
	os.environ[k] = unicode(globals()[k])

import A8M_PM
from A8M_PM import create_node

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = _("Access8Math")

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		xml_NVDA = sys.modules['xml']
		sys.modules['xml'] = globalPlugins.MathMlReader.xml

		self.create_menu()

	def create_menu(self):
		self.prefsMenu = gui.mainFrame.sysTrayIcon.preferencesMenu
		self.menu = wx.Menu()
		self.generalSettings = self.menu.Append(
			wx.ID_ANY,
			_("&General settings...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onGeneralSettings, self.generalSettings)
		self.ruleSettings = self.menu.Append(
			wx.ID_ANY,
			_("&Rule settings...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onRuleSettings, self.ruleSettings)

		self.Access8Math_item = self.prefsMenu.AppendSubMenu(self.menu, _("Access8Math"), _("Access8Math"))
		#systray = gui.mainFrame.sysTrayIcon
		#systray.menu.InsertMenu(2,wx.ID_ANY,  _("A&ccess8Math"), self.menu)

	def terminate(self):
		try:
			self.prefsMenu.RemoveItem(self.Access8Math_item)
		except (RuntimeError, AttributeError, wx.PyDeadObjectError):
			pass

	def script_change_next_language(self, gesture):
		try:
			language = config.conf["Access8Math"]["language"]
		except:
			initialize_config()
			language = config.conf["Access8Math"]["language"]

		index = (available_languages_short.index(language) +1)% len(available_languages_short)
		config.conf["Access8Math"]["language"] = language = available_languages_short[index]
		os.environ['LANGUAGE'] = language
		A8M_PM.config_from_environ()

		try:
			api.setReviewPosition(MathMlTextInfo(globalVars.math_obj, textInfos.POSITION_FIRST), False)
		except:
			pass
		ui.message(_("Access8Math language change to %s")%available_languages[index][1])
	script_change_next_language.category = scriptCategory
	# Translators: message presented in input mode.
	script_change_next_language.__doc__ = _("Change next language")

	def script_change_previous_language(self, gesture):
		try:
			language = config.conf["Access8Math"]["language"]
		except:
			initialize_config()
			language = config.conf["Access8Math"]["language"]

		index = (available_languages_short.index(language) -1)% len(available_languages_short)
		config.conf["Access8Math"]["language"] = language = available_languages_short[index]
		os.environ['LANGUAGE'] = language
		A8M_PM.config_from_environ()

		try:
			api.setReviewPosition(MathMlTextInfo(globalVars.math_obj, textInfos.POSITION_FIRST), False)
		except:
			pass
		ui.message(_("Access8Math language change to %s")%available_languages[index][1])
	script_change_previous_language.category = scriptCategory
	# Translators: message presented in input mode.
	script_change_previous_language.__doc__ = _("Change previous language")

	def script_change_provider(self, gesture):
		try:
			index = (provider_list.index(config.conf["Access8Math"]["provider"]) +1)% len(provider_list)
		except:
			initialize_config()
			index = (provider_list.index(config.conf["Access8Math"]["provider"]) +1)% len(provider_list)

		try:
			exec(
				'reader = {}()'.format(provider_list[index])
			)
			config.conf["Access8Math"]["provider"] = reader.__class__.__name__
		except:
			log.warning("{} not available".format(provider_list[index]))
		mathPres.registerProvider(reader, speech=True, braille=False, interaction=True)
		ui.message(_("mathml provider change to %s")%config.conf["Access8Math"]["provider"])
	script_change_provider.category = scriptCategory
	# Translators: message presented in input mode.
	script_change_provider.__doc__ = _("Change mathml provider")

	def onGeneralSettings(self, evt):
		gui.mainFrame._popupSettingsDialog(GeneralSettingsDialog)

	def onRuleSettings(self, evt):
		gui.mainFrame._popupSettingsDialog(RuleSettingsDialog)

	def script_settings(self, gesture):
		wx.CallAfter(self.onSettings, None)
	script_settings.category = scriptCategory
	# Translators: message presented in input mode.
	script_settings.__doc__ = _("Shows the Access8Math settings dialog.")

	__gestures={
		"kb:control+alt+m": "change_provider",
	}
