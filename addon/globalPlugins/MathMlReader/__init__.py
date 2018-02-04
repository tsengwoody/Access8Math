# coding: utf-8
# Access8Math: Allows access math content written by MathML in NVDA
# Copyright (C) 2017-2018 Tseng Woody <tsengwoody.tw@gmail.com>
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.

import os
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
		quote_pattern = re.compile(ur"([\"\'])(.*?)\1")
		mathMl = quote_pattern.sub(lambda m: m.group(1) +cgi.escape(m.group(2)) +m.group(1), mathMl)
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
		MathMlReaderInteraction(provider=self, mathMl=mathMl).setFocus()

class MathMlReaderInteraction(mathPres.MathInteractionNVDAObject):

	def __init__(self, provider=None, mathMl=None):
		super(MathMlReaderInteraction, self).__init__(provider=provider, mathMl=mathMl)

		gtlt_pattern = re.compile(ur"([\>])(.*?)([\<])")
		mathMl = gtlt_pattern.sub(lambda m: m.group(1) +cgi.escape(HTMLParser.HTMLParser().unescape(m.group(2))) +m.group(3), mathMl)
		quote_pattern = re.compile(ur"([\"\'])(.*?)\1")
		mathMl = quote_pattern.sub(lambda m: m.group(1) +cgi.escape(m.group(2)) +m.group(1), mathMl)
		parser = ET.XMLParser()
		try:
			tree = ET.fromstring(mathMl.encode('utf-8'), parser=parser)
		except BaseException as e:
			globalVars.raw_data = mathMl
			raise SystemError(e)
		globalVars.math_root = self.mathml_tree = self.pointer = create_node(tree)
		self.raw_data = mathMl
		api.setReviewPosition(self.makeTextInfo(), False)

	def _get_mathMl(self):
		return self.raw_data

	def makeTextInfo(self, position=textInfos.POSITION_FIRST):
		return MathMlTextInfo(self, position)

	'''def event_gainFocus(self):
		super(MathMlReaderInteraction, self).event_gainFocus()
		api.setReviewPosition = interaction_setReviewPosition

	def event_loseFocus(self):
		api.setReviewPosition = not_interaction_setReviewPosition'''

	def reportFocus(self):
		super(MathMlReaderInteraction, self).reportFocus()
		speech.speak(translate_SpeechCommand(self.mathml_tree.serialized()))
		api.setReviewPosition(self.makeTextInfo(), False)

	def getScript(self, gesture):
		if isinstance(gesture, KeyboardInputGesture) and "NVDA" not in gesture.modifierNames and (
			gesture.mainKeyName in {
				"leftArrow", "rightArrow", "upArrow", "downArrow",
				"home", "end",
				"space", "backspace", "enter",
			}
			or len(gesture.mainKeyName) == 1
		):
			return self.script_navigate
		'''elif isinstance(gesture, BrailleInputGesture):
			return self.script_not_action'''
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
		elif gesture.mainKeyName == "space":
			globalVars.math_obj = self
			globalVars.math_root = self.mathml_tree
			globalVars.math_pointer = self.pointer
			globalVars.math_pointer_gm = globalVars.math_pointer.get_mathml()
			speech.speak([_("copy"),])

		if r is not None:
			self.pointer = r
			api.setReviewPosition(self.makeTextInfo(), False)
			speech.speak([self.pointer.des])
			speech.speak(translate_SpeechCommand(self.pointer.serialized()))
		else:
			speech.speak([_("not move")])

provider_list = [
	u"MathMlReader",
]

try:
	provider = MathPlayer()
	provider_list.append(u"MathPlayer")
except:
	log.warning("MathPlayer 4 not available")

provider=None
language=None

def initialize_config():
	config.conf["Access8Math"] = {}
	config.conf["Access8Math"]["version"] = "1.0.2"
	config.conf["Access8Math"]["language"] = language = "Windows"
	config.conf["Access8Math"]["provider"] = provider = "MathMlReader"
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
except:
	initialize_config()

os.environ['LANGUAGE'] = language
from A8M_PM import *

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		xml_NVDA = sys.modules['xml']
		sys.modules['xml'] = globalPlugins.MathMlReader.xml

		# Gui
		self.prefsMenu = gui.mainFrame.sysTrayIcon.preferencesMenu
		self.settingsItem = self.prefsMenu.Append(
			wx.ID_ANY,
			# Translators: name of the option in the menu.
			_("&Access8Math settings...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onSettings, self.settingsItem)

	def script_change_next_language(self, gesture):
		try:
			language = config.conf["Access8Math"]["language"]
		except:
			initialize_config()
			language = config.conf["Access8Math"]["language"]

		index = (available_languages_short.index(language) +1)% len(available_languages_short)
		config.conf["Access8Math"]["language"] = language = available_languages_short[index]
		import A8M_PM
		A8M_PM.symbol = A8M_PM.load_unicode_dic(language)
		A8M_PM.math_role, A8M_PM.math_rule = A8M_PM.load_math_rule(language)
		try:
			api.setReviewPosition(MathMlTextInfo(globalVars.math_obj, textInfos.POSITION_FIRST), False)
		except:
			pass
		ui.message(_("Access8Math language change to %s")%available_languages[index][1])

	def script_change_previous_language(self, gesture):
		try:
			language = config.conf["Access8Math"]["language"]
		except:
			initialize_config()
			language = config.conf["Access8Math"]["language"]

		index = (available_languages_short.index(language) -1)% len(available_languages_short)
		config.conf["Access8Math"]["language"] = language = available_languages_short[index]
		import A8M_PM
		A8M_PM.symbol = A8M_PM.load_unicode_dic(language)
		A8M_PM.math_role, A8M_PM.math_rule = A8M_PM.load_math_rule(language)
		try:
			api.setReviewPosition(MathMlTextInfo(globalVars.math_obj, textInfos.POSITION_FIRST), False)
		except:
			pass
		ui.message(_("Access8Math language change to %s")%available_languages[index][1])

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

	__gestures={
		"kb:control+alt+l": "change_next_language",
		"kb:control+alt+shift+l": "change_previous_language",
		"kb:control+alt+m": "change_provider",
	}

	def onSettings(self, evt):
		gui.mainFrame._popupSettingsDialog(AddonSettingsDialog)

	def script_settings(self, gesture):
		wx.CallAfter(self.onSettings, None)
	script_settings.category = SCRCAT_CONFIG
	# Translators: message presented in input mode.
	script_settings.__doc__ = _("Shows the NumLock Manager settings dialog.")

class AddonSettingsDialog(SettingsDialog):

# Translators: Title of the Access8MathDialog.
	title = _("Access8Math")

	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: The label for a setting in NumLockManagerDialog.
		languageLabel = _("&Language:")
		self.languageChoices = available_languages_long
		self.languageList = sHelper.addLabeledControl(languageLabel, wx.Choice, choices=self.languageChoices)
		index = available_languages_short.index(config.conf["Access8Math"]["language"])
		self.languageList.Selection = index

	def postInit(self):
		self.languageList.SetFocus()

	def onOk(self,evt):
		super(AddonSettingsDialog, self).onOk(evt)
		try:
			config.conf["Access8Math"]["language"] = language = available_languages_short[self.languageList.GetSelection()]
		except:
			initialize_config()
			config.conf["Access8Math"]["language"] = language = available_languages_short[self.languageList.GetSelection()]

		import A8M_PM
		A8M_PM.symbol = A8M_PM.load_unicode_dic(language)
		A8M_PM.math_role, A8M_PM.math_rule = A8M_PM.load_math_rule(language)
		try:
			api.setReviewPosition(MathMlTextInfo(globalVars.math_obj, textInfos.POSITION_FIRST), False)
		except:
			pass
