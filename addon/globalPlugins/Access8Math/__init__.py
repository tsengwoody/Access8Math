"""# Access8Math: Allows access math content written by MathML and write math as MathML
# Copyright (C) 2017-2021 Tseng Woody <tsengwoody.tw@gmail.com>
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details."""
# coding: utf-8

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)
PATH = os.path.dirname(__file__)
PYTHON_PATH = os.path.join(PATH, 'python')
sys.path.insert(0, PYTHON_PATH)
PACKAGE_PATH = os.path.join(PATH, 'package')
sys.path.insert(0, PACKAGE_PATH)
sys.path.insert(0, PATH)

# python xml import
import globalPlugins.Access8Math.python.xml as xml
xml_NVDA = sys.modules['xml']
sys.modules['xml'] = xml

import _config

import addonHandler
import api
import config
import controlTypes
import globalPluginHandler
import globalVars
import gui
from logHandler import log
import mathPres
from mathPres.mathPlayer import MathPlayer
from NVDAObjects.IAccessible import IAccessible
from scriptHandler import script
import speech
import tones
import ui

import wx

import A8M_PM
from A8M_PM import MathContent

from interaction import *
from writer import TextMathEditField

addonHandler.initTranslation()
ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

provider_list = [
	A8MProvider,
]

try:
	reader = MathPlayer()
	provider_list.append(MathPlayer)
	mathPres.registerProvider(reader, speech=True, braille=True, interaction=True)
except:
	log.warning("MathPlayer 4 not available")

try:
	if config.conf["Access8Math"]["settings"]["provider"] == "Access8Math":
		provider = A8MProvider
	elif config.conf["Access8Math"]["settings"]["provider"] == "MathPlayer":
		provider = MathPlayer
	else:
		config.conf["Access8Math"]["settings"]["provider"] = "Access8Math"
		provider = A8MProvider
	reader = provider()
except:
	config.conf["Access8Math"]["settings"]["provider"] = "Access8Math"
	provider = A8MProvider
	reader = provider()

mathPres.registerProvider(reader, speech=True, braille=False, interaction=True)


class AppWindowRoot(IAccessible):
	def event_focusEntered(self):
		def run():
			parent = api.getFocusObject()
			vw = A8MInteraction(parent=parent)
			vw.set(data=globalVars.mathcontent, name="")
			try:
				vw.setFocus()
			except:
				tones.beep(100, 100)
		wx.CallLater(100, run)


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self, *args, **kwargs):
		from command.latex import initialize
		initialize()
		super().__init__(*args, **kwargs)

		A8M_PM.initialize(config.conf["Access8Math"])

		self.language = config.conf["Access8Math"]["settings"]["language"]
		self.create_menu()

	def terminate(self):
		from command.latex import terminate
		terminate()
		try:
			self.toolsMenu.Remove(self.Access8Math_item)
		except (AttributeError, RuntimeError):
			pass

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName == "wxWindowNR" and obj.role == controlTypes.ROLE_WINDOW and obj.name == _("Access8Math interaction window"):
			clsList.insert(0, AppWindowRoot)
		if (obj.windowClassName == "Edit"  and obj.role == controlTypes.ROLE_EDITABLETEXT) or (obj.windowClassName == "_WwG" and obj.role == controlTypes.ROLE_PANE):
			clsList.insert(0, TextMathEditField)

	def create_menu(self):
		self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu
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

		writeMenu = wx.Menu()
		self.latex = writeMenu.Append(
			wx.ID_ANY,
			_("&latex...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onLatexAdd, self.latex)

		self.asciiMath = writeMenu.Append(
			wx.ID_ANY,
			_("&asciimath...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onAsciiMathAdd, self.asciiMath)

		self.menu.AppendMenu(
			wx.ID_ANY,
			_("&Write..."),
			writeMenu
		)

		l10nMenu = wx.Menu()
		self.unicodeDictionary = l10nMenu.Append(
			wx.ID_ANY,
			_("&unicode dictionary...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onUnicodeDictionary, self.unicodeDictionary)

		self.mathRule = l10nMenu.Append(
			wx.ID_ANY,
			_("&math rule...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onMathRule, self.mathRule)

		self.newLanguageAdding = l10nMenu.Append(
			wx.ID_ANY,
			_("&New language adding...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onNewLanguageAdding, self.newLanguageAdding)

		self.menu.AppendMenu(
			wx.ID_ANY,
			_("&Localization..."),
			l10nMenu
		)

		self.about = self.menu.Append(
			wx.ID_ANY,
			_("&About...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onAbout, self.about)

		self.Access8Math_item = self.toolsMenu.AppendSubMenu(self.menu, _("Access8Math"), _("Access8Math"))

	@script(
		description=_("switch MathML provider"),
		category=ADDON_SUMMARY,
	)
	def script_switch_provider(self, gesture):
		if config.conf["Access8Math"]["settings"]["provider"] == "Access8Math":
			config.conf["Access8Math"]["settings"]["provider"] = "MathPlayer"
		elif config.conf["Access8Math"]["settings"]["provider"] == "MathPlayer":
			config.conf["Access8Math"]["settings"]["provider"] = "Access8Math"
		else:
			config.conf["Access8Math"]["settings"]["provider"] = "Access8Math"

		try:
			if config.conf["Access8Math"]["settings"]["provider"] == "Access8Math":
				provider = A8MProvider
			elif config.conf["Access8Math"]["settings"]["provider"] == "MathPlayer":
				provider = MathPlayer
			else:
				config.conf["Access8Math"]["settings"]["provider"] = "Access8Math"
				provider = A8MProvider
			reader = provider()
		except:
			config.conf["Access8Math"]["settings"]["provider"] = "Access8Math"
			provider = A8MProvider
			reader = provider()

		mathPres.registerProvider(reader, speech=True, braille=True, interaction=True)

		ui.message(_("mathml provider change to %s")%config.conf["Access8Math"]["settings"]["provider"])

	def onGeneralSettings(self, evt):
		from dialogs import GeneralSettingsDialog
		gui.mainFrame._popupSettingsDialog(GeneralSettingsDialog, config.conf["Access8Math"])

	def onRuleSettings(self, evt):
		from dialogs import RuleSettingsDialog
		gui.mainFrame._popupSettingsDialog(RuleSettingsDialog, config.conf["Access8Math"])

	def onNewLanguageAdding(self, evt):
		from dialogs import NewLanguageAddingDialog
		NewLanguageAddingDialog(gui.mainFrame).Show()

	def onUnicodeDictionary(self, evt):
		self.language = config.conf["Access8Math"]["settings"]["language"]
		from dialogs import UnicodeDicDialog
		gui.mainFrame._popupSettingsDialog(UnicodeDicDialog, config.conf["Access8Math"], self.language)

	def onMathRule(self, evt):
		self.language = config.conf["Access8Math"]["settings"]["language"]
		from dialogs import MathRuleDialog
		gui.mainFrame._popupSettingsDialog(MathRuleDialog, config.conf["Access8Math"], self.language)

	def onAsciiMathAdd(self, evt):
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
				mathcontent = MathContent(config.conf["Access8Math"]["settings"]["language"], mathMl)
				show_main_frame(mathcontent)

	def onLatexAdd(self, evt):
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
				mathcontent = MathContent(config.conf["Access8Math"]["settings"]["language"], mathMl)
				show_main_frame(mathcontent)

	def onAbout(self, evt):
		path = os.path.join(PATH, "locale", self.language, "about.txt")
		with open(path, 'r', encoding='utf8') as f:
			aboutMessage = f.read()
		gui.messageBox(aboutMessage, _("About Access8Math"), wx.OK)
