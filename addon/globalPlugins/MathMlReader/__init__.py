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
import languageHandler
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
			command = speech.BreakCommand(time=int(time) +int(item_interval_time))
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
		self.languageChoices = available_languages_dict.values()
		self.languageList = sHelper.addLabeledControl(languageLabel, wx.Choice, choices=self.languageChoices)
		try:
			index = available_languages_dict.keys().index(language)
		except:
			initialize_config()
			index = available_languages_dict.keys().index(language)
		self.languageList.Selection = index

		global item_interval_time
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		item_interval_timeLabel = _("&Item interval time:")
		self.item_interval_timeChoices = item_interval_time_option
		self.item_interval_timeList = sHelper.addLabeledControl(item_interval_timeLabel, wx.Choice, choices=self.item_interval_timeChoices)
		try:
			index = item_interval_time_option.index(item_interval_time)
		except:
			initialize_config()
			index = item_interval_time_option.index(item_interval_time)
		self.item_interval_timeList.Selection = index

		for k,v in self.CheckBox_settings.items():
			setattr(self, k +"CheckBox", sHelper.addItem(wx.CheckBox(self, label=v)))
			getattr(self, k +"CheckBox").SetValue(globals()[k])

	def postInit(self):
		self.languageList.SetFocus()

	def onOk(self,evt):

		global language, item_interval_time

		try:
			config.conf["Access8Math"]["language"] = language = available_languages_dict.keys()[self.languageList.GetSelection()]
			config.conf["Access8Math"]["item_interval_time"] = item_interval_time = item_interval_time_option[self.item_interval_timeList.GetSelection()]
			for k in self.CheckBox_settings.keys():
				config.conf["Access8Math"][k] = unicode(globals()[k])
		except:
			initialize_config()
			config.conf["Access8Math"]["language"] = language = available_languages_dict.keys()[self.languageList.GetSelection()]
			for k in self.CheckBox_settings.keys():
				config.conf["Access8Math"][k] = unicode(globals()[k])

		os.environ['LANGUAGE'] = language
		for k in self.CheckBox_settings.keys():
			globals()[k] = getattr(self, k +"CheckBox").IsChecked()
			os.environ[k] = unicode(globals()[k])

		A8M_PM.config_from_environ()

		try:
			api.setReviewPosition(MathMlTextInfo(globalVars.math_obj, textInfos.POSITION_FIRST), False)
		except:
			pass

		return super(GeneralSettingsDialog, self).onOk(evt)

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

		return 		super(RuleSettingsDialog, self).onOk(evt)

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
				if AG and self.mathcontent.pointer.parent.role_level == A8M_PM.AUTO_GENERATE:
					speech.speak([self.mathcontent.pointer.des])
				elif DG and self.mathcontent.pointer.parent.role_level == A8M_PM.DIC_GENERATE:
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

def initialize_config():
	config.conf["Access8Math"] = {}
	config.conf["Access8Math"]["language"] = "Windows"
	config.conf["Access8Math"]["item_interval_time"] = "50"
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
available_languages_dict = {k: v for k, v in available_languages}

item_interval_time_option = [unicode(i) for i in range(1, 101)]

try:
	language = config.conf["Access8Math"]["language"]
	item_interval_time = config.conf["Access8Math"]["item_interval_time"]
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

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = _("Access8Math")

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		xml_NVDA = sys.modules['xml']
		sys.modules['xml'] = globalPlugins.MathMlReader.xml

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

	def onNewLanguageAdding(self, evt):
		from dialogs import NewLanguageAddingDialog
		NewLanguageAddingDialog(gui.mainFrame).Show()

	def onUnicodeDictionary(self, evt):
		from dialogs import UnicodeDicDialog
		global language
		gui.mainFrame._popupSettingsDialog(UnicodeDicDialog, language)

	def onMathRule(self, evt):
		from dialogs import MathRuleDialog
		global language
		gui.mainFrame._popupSettingsDialog(MathRuleDialog, language)

	def onAbout(self,evt):
		import gui
		# Translators: The title of the dialog to show about info for NVDA.
		aboutMessage = _(
u"""Access8Math
Version: 2.0
URL: https://addons.nvda-project.org/addons/access8math.en.html
Copyright (C) 2017-2018 Access8Math Contributors
Access8Math is covered by the GNU General Public License (Version 2). You are free to share or change this software in any way you like as long as it is accompanied by the license and you make all source code available to anyone who wants it. This applies to both original and modified copies of this software, plus any derivative works.
It can be viewed online at: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
Access8Math has been sponsored by "Taiwan Visually Impaired People Association" in 2018, hereby express our sincere appreciation.
If you feel this add-on is helpful, please don't hesitate to give support to "Taiwan Visually Impaired Association" and authors."""
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
