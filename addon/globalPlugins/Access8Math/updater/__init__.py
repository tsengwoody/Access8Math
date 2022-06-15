# Add-on Updater
# Copyright 2018-2022 Joseph Lee, released under GPL.

# Note: proof of concept implementation of NVDA Core issue 3208
# URL: https://github.com/nvaccess/nvda/issues/3208

import globalPluginHandler
import time
import gui
from gui.nvdaControls import CustomCheckListBox, AutoWidthColumnListCtrl
import wx
# What if this is run from NVDA source?
try:
	import updateCheck
	canUpdate = True
except RuntimeError:
	canUpdate = False
import globalVars
import config
from logHandler import log
from . import addonHandlerEx
try:
	from . import addonGuiEx
except RuntimeError:
	canUpdate = False
from . import addonUtils
from .skipTranslation import translate
import addonHandler
addonHandler.initTranslation()

# Overall update check routine was inspired by StationPlaylist Studio add-on (Joseph Lee).)

addonUpdateCheckInterval = 86400
updateChecker = None


# To avoid freezes, a background thread will run after the global plugin constructor calls wx.CallAfter.
def autoUpdateCheck():
	currentTime = time.time()
	whenToCheck = addonUtils.updateState["lastChecked"] + addonUpdateCheckInterval
	if currentTime >= whenToCheck:
		addonUtils.updateState["lastChecked"] = currentTime
		if addonUtils.updateState["autoUpdate"]:
			startAutoUpdateCheck(addonUpdateCheckInterval)
		addonHandlerEx.autoAddonUpdateCheck()
	else:
		startAutoUpdateCheck(whenToCheck - currentTime)


# Start or restart auto update checker.
def startAutoUpdateCheck(interval):
	global updateChecker
	if updateChecker is not None:
		wx.CallAfter(updateChecker.Stop)
	updateChecker = wx.PyTimer(autoUpdateCheck)
	wx.CallAfter(updateChecker.Start, interval * 1000, True)


def endAutoUpdateCheck():
	global updateChecker
	addonUtils.updateState["lastChecked"] = time.time()
	if updateChecker is not None:
		wx.CallAfter(updateChecker.Stop)
		wx.CallAfter(autoUpdateCheck)


if canUpdate:
	addonGuiEx.AddonUpdaterManualUpdateCheck.register(endAutoUpdateCheck)


class AddonUpdaterPanel(gui.SettingsPanel):
	# Translators: This is the label for the Access8Math Updater settings panel.
	title = _("Updater")

	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self.autoUpdateCheckBox = sHelper.addItem(
			# Translators: This is the label for a checkbox in the
			# Add-on Updater settings panel.
			wx.CheckBox(self, label=_("Automatically check for add-on &updates"))
		)
		self.autoUpdateCheckBox.SetValue(addonUtils.updateState["autoUpdate"])

	def onSave(self):
		addonUtils.updateState["autoUpdate"] = self.autoUpdateCheckBox.IsChecked()
		global updateChecker
		if updateChecker and updateChecker.IsRunning():
			updateChecker.Stop()
		updateChecker = None
		if addonUtils.updateState["autoUpdate"]:
			addonUtils.updateState["lastChecked"] = time.time()
			wx.CallAfter(autoUpdateCheck)
