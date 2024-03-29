"""# Access8Math: Allows access math content written by MathML and write math as MathML
# Copyright (C) 2017-2022 Tseng Woody <tsengwoody.tw@gmail.com>
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details."""
# coding: utf-8

import os
import sys
import shutil

import addonHandler
import api
import appModules
import config
import controlTypes
import globalPluginHandler
import globalVars
import gui
from languageHandler import getWindowsLanguage
from logHandler import log
import mathPres
from mathPres.mathPlayer import MathPlayer
from NVDAObjects.IAccessible import IAccessible
from scriptHandler import script
import textInfos
import tones
import ui

import wx

insert_path_count = 0
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# sys.path.insert(0, BASE_DIR)

PATH = os.path.dirname(__file__)

PYTHON_PATH = os.path.join(PATH, 'python')
sys.path.insert(0, PYTHON_PATH)
insert_path_count += 1

PACKAGE_PATH = os.path.join(PATH, 'package')
sys.path.insert(0, PACKAGE_PATH)
insert_path_count += 1

sys.path.insert(0, PATH)
insert_path_count += 1

# python xml import
import python.xml as xml
sys.modules['xml'] = xml

config.conf.spec["Access8Math"] = {
	"settings": {
		"language": "string(default=Windows)",
		"braille_language": "string(default=en)",
		"item_interval_time": "integer(default=50,min=0,max=100)",
		"interaction_frame_show": "boolean(default=false)",
		"analyze_math_meaning": "boolean(default=true)",
		"auto_generate": "boolean(default=false)",
		"dictionary_generate": "boolean(default=true)",
		"no_move_beep": "boolean(default=true)",
		"command_mode": "boolean(default=false)",
		"navigate_mode": "boolean(default=false)",
		"shortcut_mode": "boolean(default=false)",
		"writeNavAudioIndication": "boolean(default=true)",
		"writeNavAcrossLine": "boolean(default=true)",
		"HTML_document_display": "string(default=markdown)",
		"HTML_math_display": "string(default=block)",
		"color": "string(default=#000000)",
		"bg_color": "string(default=#ffffff)",
		"LaTeX_delimiter": "string(default=bracket)",
		"Nemeth_delimiter": "string(default=at)",
		"speech_source": "string(default=Access8Math)",
		"braille_source": "string(default=Access8Math)",
		"interact_source": "string(default=Access8Math)",
	},
	"rules": {
		"SingleMsubsupType": "boolean(default=true)",
		"SingleMsubType": "boolean(default=true)",
		"SingleMsupType": "boolean(default=true)",
		"SingleMunderoverType": "boolean(default=true)",
		"SingleMunderType": "boolean(default=true)",
		"SingleMoverType": "boolean(default=true)",
		"SingleFractionType": "boolean(default=true)",
		"SingleSqrtType": "boolean(default=true)",
		"PowerType": "boolean(default=true)",
		"SquarePowerType": "boolean(default=true)",
		"CubePowerType": "boolean(default=true)",
		"SetType": "boolean(default=true)",
		"AbsoluteType": "boolean(default=true)",
		"MatrixType": "boolean(default=true)",
		"DeterminantType": "boolean(default=true)",
		"AddIntegerFractionType": "boolean(default=true)",
	}
}

import A8M_PM
from .command.context import A8MFEVContextMenuView
from .dialogs import NewLanguageAddingDialog, UnicodeDicDialog, MathRuleDialog, MathReaderSettingsPanel, Access8MathSettingsDialog
from .editor import EditorFrame
from .interaction import A8MProvider, A8MInteraction
from .lib.storage import explorer
from .writer import TextMathEditField

for i in range(insert_path_count):
	del sys.path[0]

addonHandler.initTranslation()
ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]
ADDON_VERSION = addonHandler.getCodeAddon().manifest["version"]

aboutMessage = _("""Access8Math
Version: {addonVersion}
URL: https://addons.nvda-project.org/addons/access8math.en.html
Copyright (C) {copyrightFirstYear}-{copyrightLastYear} Access8Math Contributors
Access8Math is covered by the GNU General Public License (Version 2). You are free to share or change this software in any way you like as long as it is accompanied by the license and you make all source code available to anyone who wants it. This applies to both original and modified copies of this software, plus any derivative works.
It can be viewed online at: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html""").format(
	addonVersion=ADDON_VERSION,
	copyrightFirstYear=2017,
	copyrightLastYear=2024,
)


ROLE_WINDOW = controlTypes.Role.WINDOW
ROLE_EDITABLETEXT = controlTypes.Role.EDITABLETEXT

available_readers = []
available_readers.append("Access8Math")

mathCAT = None
try:
	from globalPlugins.MathCAT import MathCAT
	mathCAT = MathCAT()
	available_readers.append("MathCAT")
except BaseException:
	log.warning("MathCAT not available")
	for item in ["speech_source", "braille_source", "interact_source"]:
		if config.conf["Access8Math"]["settings"][item] == "MathCAT" and not mathCAT:
			config.conf["Access8Math"]["settings"][item] = "Access8Math"

mathPlayer = None
try:
	mathPlayer = MathPlayer()
	available_readers.append("MathPlayer")
except BaseException:
	log.warning("MathPlayer 4 not available")
	for item in ["speech_source", "braille_source", "interact_source"]:
		if config.conf["Access8Math"]["settings"][item] == "MathPlayer" and not mathPlayer:
			config.conf["Access8Math"]["settings"][item] = "Access8Math"

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
			except BaseException:
				tones.beep(100, 100)
		wx.CallLater(100, run)


editor_dialog = None


def disableInSecureMode(decoratedCls):
	if globalVars.appArgs.secure:
		return globalPluginHandler.GlobalPlugin
	return decoratedCls


@disableInSecureMode
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self, *args, **kwargs):
		if config.conf["Access8Math"]["settings"]["language"] == "Windows":
			config.conf["Access8Math"]["settings"]["language"] = getWindowsLanguage()

		from lib.latex import latexData
		latexData.initialize()
		super().__init__(*args, **kwargs)

		A8M_PM.initialize(config.conf["Access8Math"])

		self.language = config.conf["Access8Math"]["settings"]["language"]
		self.create_menu()
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(MathReaderSettingsPanel)

	def terminate(self):
		from lib.latex import latexData
		latexData.terminate()
		try:
			self.toolsMenu.Remove(self.Access8Math_item)
		except (AttributeError, RuntimeError):
			pass

		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(MathReaderSettingsPanel)

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if getattr(obj, 'windowClassName', None) == "wxWindowNR" and obj.role == ROLE_WINDOW and obj.name == _("Access8Math interaction window"):
			clsList.insert(0, AppWindowRoot)
		if getattr(obj, 'windowClassName', None) == "Edit" and obj.role == ROLE_EDITABLETEXT:
			clsList.insert(0, TextMathEditField)

	def create_menu(self):
		self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu

		self.menu = wx.Menu()

		self.editor = self.menu.Append(
			wx.ID_ANY,
			_("&Editor...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onEditor, self.editor)

		self.settings = self.menu.Append(
			wx.ID_ANY,
			_("&Settings...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onSettings, self.settings)

		l10nMenu = wx.Menu()

		self.speechUnicodeDictionary = l10nMenu.Append(
			wx.ID_ANY,
			_("Speech &unicode dictionary...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onSpeechUnicodeDictionary, self.speechUnicodeDictionary)

		self.speechMathRule = l10nMenu.Append(
			wx.ID_ANY,
			_("Speech &math rule...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onSpeechMathRule, self.speechMathRule)

		self.brailleUnicodeDictionary = l10nMenu.Append(
			wx.ID_ANY,
			_("Braille &unicode dictionary...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onBrailleUnicodeDictionary, self.brailleUnicodeDictionary)

		self.brailleMathRule = l10nMenu.Append(
			wx.ID_ANY,
			_("Braille &math rule...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onBrailleMathRule, self.brailleMathRule)

		self.newLanguageAdding = l10nMenu.Append(
			wx.ID_ANY,
			_("&New language adding...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onNewLanguageAdding, self.newLanguageAdding)

		self.menu.AppendSubMenu(
			l10nMenu,
			_("&Localization"),
		)

		self.cleanWorkspace = self.menu.Append(
			wx.ID_ANY,
			_("&Clean Workspace...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onCleanWorkspace, self.cleanWorkspace)

		self.about = self.menu.Append(
			wx.ID_ANY,
			_("&About...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onAbout, self.about)

		self.Access8Math_item = self.toolsMenu.AppendSubMenu(self.menu, _("Access8Math"), _("Access8Math"))

	@script(
		description=_("Switch math speech reader"),
		category=ADDON_SUMMARY,
	)
	def script_speech_source_switch(self, gesture):
		key = "speech_source"
		try:
			index = available_readers.index(str(config.conf["Access8Math"]["settings"][key]))
		except BaseException:
			index = 0
		index = (index + 1) % len(available_readers)
		config.conf["Access8Math"]["settings"][key] = available_readers[index]
		ui.message(_("Math speech reader switch to %s") % config.conf["Access8Math"]["settings"][key])

	@script(
		description=_("Switch math Braille reader"),
		category=ADDON_SUMMARY,
	)
	def script_braille_source_switch(self, gesture):
		key = "braille_source"
		try:
			index = available_readers.index(str(config.conf["Access8Math"]["settings"][key]))
		except BaseException:
			index = 0
		index = (index + 1) % len(available_readers)
		config.conf["Access8Math"]["settings"][key] = available_readers[index]
		ui.message(_("Math braille reader switch to %s") % config.conf["Access8Math"]["settings"][key])

	@script(
		description=_("Switch math interact reader"),
		category=ADDON_SUMMARY,
	)
	def script_interact_source_switch(self, gesture):
		key = "interact_source"
		try:
			index = available_readers.index(str(config.conf["Access8Math"]["settings"][key]))
		except BaseException:
			index = 0
		index = (index + 1) % len(available_readers)
		config.conf["Access8Math"]["settings"][key] = available_readers[index]
		ui.message(_("Math interact reader switch to %s") % config.conf["Access8Math"]["settings"][key])

	@script(
		description=_("Pop up the editor"),
		category=ADDON_SUMMARY,
		gesture="kb:NVDA+alt+e",
	)
	def script_editor_popup(self, gesture):
		def show():
			try:
				filename = explorer.get_selected_file()
			except BaseException:
				filename = None
			if filename:
				try:
					self.edit(path=filename)
				except BaseException:
					obj = api.getFocusObject()
					document = obj.makeTextInfo(textInfos.POSITION_ALL)
					editor_content = document.text
					self.edit(content=editor_content)
			else:
				obj = api.getFocusObject()
				document = obj.makeTextInfo(textInfos.POSITION_ALL)
				editor_content = document.text
				self.edit(content=editor_content)
		wx.CallAfter(show)

	def edit(self, content=None, path=None):
		if path:
			frame = EditorFrame(path)
		if content or content == '':
			frame = EditorFrame()
			frame.control.SetValue(content)
		frame.Show(True)

	@script(
		description=_("Open virtual context menu"),
		category=ADDON_SUMMARY,
		gestures=["kb:NVDA+applications", "kb:NVDA+shift+f10"],
	)
	def script_open_virtual_context_menu(self, gesture):
		obj = api.getFocusObject()
		if isinstance(obj.appModule, appModules.explorer.AppModule):
			try:
				filename = explorer.get_selected_file()
			except BaseException:
				filename = None
			if filename:
				try:
					A8MFEVContextMenuView(
						path=filename
					).setFocus()
				except BaseException:
					ui.message(_("open path failed"))
			else:
				ui.message(_("get path failed"))

	def onSettings(self, evt):
		wx.CallAfter(gui.mainFrame._popupSettingsDialog, Access8MathSettingsDialog)

	def onNewLanguageAdding(self, evt):
		NewLanguageAddingDialog(gui.mainFrame).Show()

	def onSpeechUnicodeDictionary(self, evt):
		gui.mainFrame._popupSettingsDialog(
			UnicodeDicDialog, config.conf["Access8Math"],
			language=config.conf["Access8Math"]["settings"]["language"], category='speech'
		)

	def onSpeechMathRule(self, evt):
		gui.mainFrame._popupSettingsDialog(
			MathRuleDialog, config.conf["Access8Math"],
			language=config.conf["Access8Math"]["settings"]["language"], category='speech'
		)

	def onBrailleUnicodeDictionary(self, evt):
		gui.mainFrame._popupSettingsDialog(
			UnicodeDicDialog, config.conf["Access8Math"],
			language=config.conf["Access8Math"]["settings"]["language"], category='braille'
		)

	def onBrailleMathRule(self, evt):
		gui.mainFrame._popupSettingsDialog(
			MathRuleDialog, config.conf["Access8Math"],
			language=config.conf["Access8Math"]["settings"]["language"], category='braille'
		)

	def onEditor(self, editor_content):
		self.edit(content='')

	def onCleanWorkspace(self, evt):
		for item in [
			os.path.join(PATH, 'web', 'export'),
			os.path.join(PATH, 'web', 'workspace'),
		]:
			try:
				shutil.rmtree(item)
			except BaseException:
				pass

		A8M_PM.clean_user_data()

		gui.messageBox(_("Workspace has already been cleaned"), _("Clean Workspace"), wx.OK)

	def onAbout(self, evt):
		gui.messageBox(aboutMessage, _("About Access8Math"), wx.OK)
