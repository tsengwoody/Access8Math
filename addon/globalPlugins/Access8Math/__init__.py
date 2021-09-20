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
import tones
import ui

import wx

import A8M_PM
from A8M_PM import MathContent

from interaction import A8MProvider, A8MInteraction, show_main_frame, main_frame
from writer import TextMathEditField

addonHandler.initTranslation()
ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

aboutMessage = _("""Access8Math
Version: 3.1
URL: https://addons.nvda-project.org/addons/access8math.en.html
Copyright (C) 2017-2021 Access8Math Contributors
Access8Math is covered by the GNU General Public License (Version 2). You are free to share or change this software in any way you like as long as it is accompanied by the license and you make all source code available to anyone who wants it. This applies to both original and modified copies of this software, plus any derivative works.
It can be viewed online at: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
Access8Math has been sponsored by "Taiwan Visually Impaired People Association"(accessibility@twvip.org) in 2018~2019, hereby express our sincere appreciation.
If you feel this add-on is helpful, please don't hesitate to give support to "Taiwan Visually Impaired People Association" and authors.""")

mathPlayer = None
try:
	mathPlayer = MathPlayer()
except:
	config.conf["Access8Math"]["settings"]["speech_source"] = "Access8Math"
	config.conf["Access8Math"]["settings"]["braille_source"] = "Access8Math"
	config.conf["Access8Math"]["settings"]["interact_source"] = "Access8Math"
	log.warning("MathPlayer 4 not available")

reader = A8MProvider()
mathPres.registerProvider(reader, speech=True, braille=True, interaction=True)

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
		description=_("speech source switch"),
		category=ADDON_SUMMARY,
	)
	def script_speech_source_switch(self, gesture):
		if config.conf["Access8Math"]["settings"]["speech_source"] == "Access8Math" and mathPlayer:
			config.conf["Access8Math"]["settings"]["speech_source"] = "MathPlayer"
		elif config.conf["Access8Math"]["settings"]["speech_source"] == "MathPlayer":
			config.conf["Access8Math"]["settings"]["speech_source"] = "Access8Math"
		else:
			config.conf["Access8Math"]["settings"]["speech_source"] = "Access8Math"
		ui.message(_("MathML speech source switch to %s")%config.conf["Access8Math"]["settings"]["speech_source"])

	@script(
		description=_("braille source switch"),
		category=ADDON_SUMMARY,
	)
	def script_braille_source_switch(self, gesture):
		if config.conf["Access8Math"]["settings"]["braille_source"] == "Access8Math" and mathPlayer:
			config.conf["Access8Math"]["settings"]["braille_source"] = "MathPlayer"
		elif config.conf["Access8Math"]["settings"]["braille_source"] == "MathPlayer":
			config.conf["Access8Math"]["settings"]["braille_source"] = "Access8Math"
		else:
			config.conf["Access8Math"]["settings"]["braille_source"] = "Access8Math"
		ui.message(_("MathML braille source switch to %s")%config.conf["Access8Math"]["settings"]["braille_source"])

	@script(
		description=_("interact source switch"),
		category=ADDON_SUMMARY,
	)
	def script_interact_source_switch(self, gesture):
		if config.conf["Access8Math"]["settings"]["interact_source"] == "Access8Math" and mathPlayer:
			config.conf["Access8Math"]["settings"]["interact_source"] = "MathPlayer"
		elif config.conf["Access8Math"]["settings"]["interact_source"] == "MathPlayer":
			config.conf["Access8Math"]["settings"]["interact_source"] = "Access8Math"
		else:
			config.conf["Access8Math"]["settings"]["interact_source"] = "Access8Math"
		ui.message(_("MathML interact source switch to %s")%config.conf["Access8Math"]["settings"]["interact_source"])

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
		gui.messageBox(aboutMessage, _("About Access8Math"), wx.OK)
