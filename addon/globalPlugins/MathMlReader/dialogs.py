# coding: utf-8

import sys
if sys.version_info.major == 2:
	unicode = unicode
elif sys.version_info.major >= 3:
	unicode = str

from collections import OrderedDict
import io
import os
import shutil
import wx
#from wx.lib.expando import ExpandoTextCtrl

import addonHandler
import api
import config
import core
import gui
from gui import nvdaControls
from gui import guiHelper
from gui.settingsDialogs import SettingsDialog
from logHandler import log
import queueHandler
import tones

if sys.version_info.major == 2:
	import A8M_PM_2 as A8M_PM
elif sys.version_info.major >= 3:
	import A8M_PM_3 as A8M_PM

import configure
from utils import convert_bool
addonHandler.initTranslation()

base_path = os.path.dirname(os.path.abspath(__file__))

class GeneralSettingsDialog(SettingsDialog):
	# Translators: Title of the Access8MathDialog.
	title = _("General Settings")
	CheckBox_settings = OrderedDict([
		("IFS", _("showing Access8Math interaction window when entering interaction mode")),
		("AMM", _("Analyze mathematical meaning of content")),
		("DG", _("Read defined meaning in dictionary")),
		("AG", _("Read of auto-generated meaning")),
	])

	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		languageLabel = _("&Language:")
		self.languageChoices = list(available_languages_dict.values())
		self.language = os.environ['LANGUAGE']
		self.languageList = sHelper.addLabeledControl(languageLabel, wx.Choice, choices=self.languageChoices)
		try:
			index = list(available_languages_dict.keys()).index(self.language)
		except:
			configure.initialize_config()
			index = list(available_languages_dict.keys()).index(self.language)
		self.languageList.Selection = index

		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		item_interval_timeLabel = _("&Item interval time:")
		self.item_interval_timeChoices = [unicode(i) for i in range(1, 101)]
		self.item_interval_timeList = sHelper.addLabeledControl(item_interval_timeLabel, wx.Choice, choices=self.item_interval_timeChoices)
		try:
			index = self.item_interval_timeChoices.index(os.environ['item_interval_time'])
		except:
			configure.initialize_config()
			index = self.item_interval_timeChoices.index(os.environ['item_interval_time'])
		self.item_interval_timeList.Selection = index

		for k,v in self.CheckBox_settings.items():
			setattr(self, k +"CheckBox", sHelper.addItem(wx.CheckBox(self, label=v)))
			value = convert_bool(os.environ[k])
			getattr(self, k +"CheckBox").SetValue(value)

	def postInit(self):
		self.languageList.SetFocus()

	def onOk(self,evt):

		try:
			config.conf["Access8Math"]["language"] = os.environ['LANGUAGE'] = list(available_languages_dict.keys())[self.languageList.GetSelection()]
			config.conf["Access8Math"]["item_interval_time"] = os.environ['item_interval_time'] = self.item_interval_timeChoices[self.item_interval_timeList.GetSelection()]
			for k in self.CheckBox_settings.keys():
				config.conf["Access8Math"][k] = os.environ[k] = unicode(getattr(self, k +"CheckBox").IsChecked())
		except:
			configure.initialize_config()
			config.conf["Access8Math"]["language"] = os.environ['LANGUAGE'] = list(available_languages_dict.keys())[self.languageList.GetSelection()]
			config.conf["Access8Math"]["item_interval_time"] = os.environ['item_interval_time'] = self.item_interval_timeChoices[self.item_interval_timeList.GetSelection()]
			for k in self.CheckBox_settings.keys():
				config.conf["Access8Math"][k] = os.environ[k] = unicode(getattr(self, k +"CheckBox").IsChecked())

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
			value = convert_bool(os.environ[k])
			getattr(self, k +"CheckBox").SetValue(value)

	def postInit(self):
		getattr(self, list(self.CheckBox_settings.keys())[0] +"CheckBox").SetFocus()

	def onOk(self,evt):
		try:
			for k in self.CheckBox_settings.keys():
				config.conf["Access8Math"][k] = os.environ[k] = unicode(getattr(self, k +"CheckBox").IsChecked())
		except:
			configure.initialize_config()
			for k in self.CheckBox_settings.keys():
				config.conf["Access8Math"][k] = os.environ[k] = unicode(getattr(self, k +"CheckBox").IsChecked())

		A8M_PM.config_from_environ()

		try:
			api.setReviewPosition(MathMlTextInfo(globalVars.math_obj, textInfos.POSITION_FIRST), False)
		except:
			pass

		return 		super(RuleSettingsDialog, self).onOk(evt)

class AddSymbolDialog(wx.Dialog):

	def __init__(self, parent):
		# Translators: This is the label for the add symbol dialog.
		super(AddSymbolDialog,self).__init__(parent, title=_("Add Symbol"))
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		sHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)

		# Translators: This is the label for the edit field in the add symbol dialog.
		symbolText = _("Symbol:")
		self.identifierTextCtrl = sHelper.addLabeledControl(symbolText, wx.TextCtrl)

		sHelper.addDialogDismissButtons(self.CreateButtonSizer(wx.OK | wx.CANCEL))

		mainSizer.Add(sHelper.sizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.identifierTextCtrl.SetFocus()
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

class UnicodeDicDialog(SettingsDialog):

	def __init__(self,parent, language):
		self.language = language
		try:
			symbol = A8M_PM.load_unicode_dic(language=self.language)
		except LookupError:
			symbol = A8M_PM.load_unicode_dic(language='Windows')
		self.A8M_symbol = symbol
		# Translators: This is the label for the symbol pronunciation dialog.
		# %s is replaced by the language for which symbol pronunciation is being edited.
		self.title = _("unicode dictionary (%s)")%self.language
		super(UnicodeDicDialog, self).__init__(parent)

	def makeSettings(self, settingsSizer):
		symbols = self.symbols = [list(i) for i in self.A8M_symbol.items()]

		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: The label for symbols list in symbol pronunciation dialog.
		symbolsText = _("&Symbols")
		try:
			#NVDA version >= 2019.2 syntax with autoSizeColumn keyword
			self.symbolsList = sHelper.addLabeledControl(symbolsText, nvdaControls.AutoWidthColumnListCtrl, autoSizeColumn=0, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
		except TypeError:
			#NVDA version <= 2019.1.1 syntax with autoSizeColumnIndex keyword
			self.symbolsList = sHelper.addLabeledControl(symbolsText, nvdaControls.AutoWidthColumnListCtrl, autoSizeColumnIndex=0, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
		# Translators: The label for a column in symbols list used to identify a symbol.
		self.symbolsList.InsertColumn(0, _("Symbol"))
		self.symbolsList.InsertColumn(1, _("Replacement"))
		for origin, replacement in symbols:
			item = self.symbolsList.Append((origin, replacement, ))
			self.updateListItem(item, replacement)

		self.symbolsList.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.onListItemFocused)

		# Translators: The label for the group of controls in symbol pronunciation dialog to change the pronunciation of a symbol.
		changeSymbolText = _("Change selected symbol")
		changeSymbolHelper = sHelper.addItem(guiHelper.BoxSizerHelper(self, sizer=wx.StaticBoxSizer(wx.StaticBox(self, label=changeSymbolText), wx.VERTICAL)))

		# Used to ensure that event handlers call Skip(). Not calling skip can cause focus problems for controls. More 
		# generally the advice on the wx documentation is: "In general, it is recommended to skip all non-command events
		# to allow the default handling to take place. The command events are, however, normally not skipped as usually 
		# a single command such as a button click or menu item selection must only be processed by one handler."
		def skipEventAndCall(handler):
			def wrapWithEventSkip(event):
				if event:
					event.Skip()
				return handler()
			return wrapWithEventSkip

		
		# Translators: The label for the edit field in symbol pronunciation dialog to change the replacement text of a symbol.
		replacementText = _("&Replacement")
		self.replacementEdit = changeSymbolHelper.addLabeledControl(replacementText, wx.TextCtrl)
		self.replacementEdit.Bind(wx.EVT_TEXT, skipEventAndCall(self.onSymbolEdited))

		# disable the "change symbol" controls until a valid item is selected.
		self.replacementEdit.Disable()

		bHelper = sHelper.addItem(guiHelper.ButtonHelper(orientation=wx.HORIZONTAL))
		# Translators: The label for a button in the Symbol Pronunciation dialog to add a new symbol.
		addButton = bHelper.addButton(self, label=_("&Add"))

		# Translators: The label for a button in the Symbol Pronunciation dialog to remove a symbol.
		self.removeButton = bHelper.addButton(self, label=_("Re&move"))
		self.removeButton.Disable()

		# Translators: The label for a button to recover default value.
		recoverDefaultButton = bHelper.addButton(self, label=_("&Recover default"))

		# Translators: The label for a button to import unicode.dic.
		importButton = bHelper.addButton(self, label=_("&Import"))

		# Translators: The label for a button to export unicode.dic.
		exportButton = bHelper.addButton(self, label=_("Exp&ort"))

		addButton.Bind(wx.EVT_BUTTON, self.OnAddClick)
		self.removeButton.Bind(wx.EVT_BUTTON, self.OnRemoveClick)
		recoverDefaultButton.Bind(wx.EVT_BUTTON, self.OnRecoverDefaultClick)
		importButton.Bind(wx.EVT_BUTTON, self.OnImportClick)
		exportButton.Bind(wx.EVT_BUTTON, self.OnExportClick)

		self.editingItem = None

	def postInit(self):
		self.symbolsList.SetFocus()

	def load(self, path):
		symbol = self.A8M_symbol = A8M_PM.load_unicode_dic(path)

		symbols = self.symbols = [list(i) for i in self.A8M_symbol.items()]
		for origin, replacement in symbols:
			item = self.symbolsList.Append((origin, replacement, ))
			self.updateListItem(item, replacement)

		return True

	def save(self, path, symbol):
		A8M_PM.save_unicode_dic(symbol, path=path)
		return True

	def clear(self):
		self.symbolsList.DeleteAllItems()
		self.symbols = []
		self.editingItem = None

		self.replacementEdit.SetValue("")
		self.replacementEdit.Disable()
		self.removeButton.Disable()

	def updateListItem(self, item, replacement):
		self.symbolsList.SetStringItem(item, 1, replacement)

	def onSymbolEdited(self):
		if self.editingItem is not None:
			# Update the symbol the user was just editing.
			item = self.editingItem
			symbol = self.symbols[item]
			symbol[1] = self.replacementEdit.Value
			self.updateListItem(item, symbol[1])

	def onListItemFocused(self, evt):
		# Update the editing controls to reflect the newly selected symbol.
		item = evt.GetIndex()
		symbol = self.symbols[item]
		self.editingItem = item
		# ChangeValue and Selection property used because they do not cause EVNT_CHANGED to be fired.
		self.replacementEdit.ChangeValue(symbol[1])
		#self.removeButton.Enabled = not self.symbolProcessor.isBuiltin(symbol.identifier)
		self.removeButton.Enable()
		self.replacementEdit.Enable()
		evt.Skip()

	def OnAddClick(self, evt):
		with AddSymbolDialog(self) as entryDialog:
			if entryDialog.ShowModal() != wx.ID_OK:
				return
			identifier = entryDialog.identifierTextCtrl.GetValue()
			if not identifier:
				return
		for index, symbol in enumerate(self.symbols):
			if identifier == symbol[0]:
				# Translators: An error reported in the Symbol Pronunciation dialog when adding a symbol that is already present.
				gui.messageBox(_('Symbol "%s" is already present.') % identifier,
					_("Error"), wx.OK | wx.ICON_ERROR)
				self.symbolsList.Select(index)
				self.symbolsList.Focus(index)
				self.symbolsList.SetFocus()
				return
		addedSymbol = [identifier, '']
		self.symbols.append(addedSymbol)
		item = self.symbolsList.Append((addedSymbol[0], addedSymbol[1],))
		self.updateListItem(item, addedSymbol[1])
		self.symbolsList.Select(item)
		self.symbolsList.Focus(item)
		self.symbolsList.SetFocus()

	def OnRemoveClick(self, evt):
		index = self.symbolsList.GetFirstSelected()
		symbol = self.symbols[index]
		# Deleting from self.symbolsList focuses the next item before deleting,
		# so it must be done *before* we delete from self.symbols.
		self.symbolsList.DeleteItem(index)
		del self.symbols[index]
		index = min(index, self.symbolsList.ItemCount - 1)
		self.symbolsList.Select(index)
		self.symbolsList.Focus(index)
		# We don't get a new focus event with the new index, so set editingItem.
		self.editingItem = index
		self.symbolsList.SetFocus()

	def OnRecoverDefaultClick(self, evt):
		path = base_path
		if not self.language == 'Windows':
			path = base_path +'/locale/{0}'.format(self.language)
		pathname = os.path.join(path, 'unicode.dic')

		self.clear()
		self.load(pathname)

	def OnImportClick(self, evt):
		with wx.FileDialog(self, message=_("Import file..."), defaultDir=base_path, wildcard="dictionary files (*.dic)|*.dic") as entryDialog:
			if entryDialog.ShowModal() != wx.ID_OK:
				return
			pathname = entryDialog.GetPath()

		self.clear()
		self.load(pathname)

	def OnExportClick(self, evt):
		with wx.FileDialog(self, message=_("Export file..."), defaultDir=base_path, defaultFile="export.dic", wildcard="dictionary files (*.dic)|*.dic", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as entryDialog:
			if entryDialog.ShowModal() != wx.ID_OK:
				return
			pathname = entryDialog.GetPath()

		self.A8M_symbol = {}
		for symbol in self.symbols:
			self.A8M_symbol[symbol[0]] = symbol[1]

		self.save(pathname, self.A8M_symbol)

	def onOk(self, evt):
		self.onSymbolEdited()
		self.editingItem = None

		self.A8M_symbol = {}
		for symbol in self.symbols:
			self.A8M_symbol[symbol[0]] = symbol[1]

		try:
			A8M_PM.save_unicode_dic(self.A8M_symbol, language=self.language)
		except IOError as e:
			log.error("Error saving user unicode dictionary: %s" % e)

		A8M_PM.config_from_environ()

		super(UnicodeDicDialog, self).onOk(evt)

class RuleEntryDialog(wx.Dialog):
	def __init__(self, parent, mathrule, title=_("Edit Math Rule Entry")):
		super(RuleEntryDialog,self).__init__(parent,title=title)
		self.mathrule = mathrule
		self.mathrule_child_count = len(self.mathrule[1].role)
		childChoices = [unicode(i) for i in range(self.mathrule_child_count)]
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		sHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)

		labelText = _("&description")

		groupLabelText = _("description")
		descriptionGroup = guiHelper.BoxSizerHelper(self, sizer=wx.StaticBoxSizer(wx.StaticBox(self, label=groupLabelText), wx.VERTICAL))

		labelText = _("&description")
		self.descriptionWidget = descriptionGroup.addLabeledControl(labelText, wx.TextCtrl)
		self.descriptionWidget.SetValue(self.mathrule[1].description)
		sHelper.addItem(descriptionGroup)

		self.so_widgets = []
		groupLabelText = _("Serialized ordering")
		serializedOrderingGroup = guiHelper.BoxSizerHelper(self, sizer=wx.StaticBoxSizer(wx.StaticBox(self, label=groupLabelText), wx.VERTICAL))
		for index, item in enumerate(self.mathrule[1].serialized_order):
			groupLabelText = _("Ordering %d")%(index)
			itemGroup = guiHelper.BoxSizerHelper(self, sizer=wx.StaticBoxSizer(wx.StaticBox(self, label=groupLabelText), wx.HORIZONTAL))
			if isinstance(item, int):
				labelText = _("Child")
				widget = itemGroup.addLabeledControl(labelText, wx.Choice, choices=childChoices)
				widget.Selection = item
				self.so_widgets.append(widget)
			elif isinstance(item, tuple):
				# before item
				labelText = _("Before item text &%d")%(index)
				widget = itemGroup.addLabeledControl(labelText, wx.TextCtrl)
				widget.SetValue(item[0])
				self.so_widgets.append(widget)
				# after item
				labelText = _("After item text &%d")%(index)
				widget = itemGroup.addLabeledControl(labelText, wx.TextCtrl)
				widget.SetValue(item[1])
				self.so_widgets.append(widget)
			else:
				if index==0:
					labelText = _("Start text &%d")%(index)
				elif index == len(self.mathrule[1].serialized_order)-1:
					labelText = _("End text &%d")%(index)
				else:
					labelText = _("&Interval text &%d")%(index)
				widget = itemGroup.addLabeledControl(labelText, wx.TextCtrl)
				widget.SetValue(unicode(item))
				self.so_widgets.append(widget)
			serializedOrderingGroup.addItem(itemGroup)
		sHelper.addItem(serializedOrderingGroup)

		self.role_widgets = []
		groupLabelText = _("Child role")
		childRoleGroup = guiHelper.BoxSizerHelper(self, sizer=wx.StaticBoxSizer(wx.StaticBox(self, label=groupLabelText), wx.VERTICAL))
		for index, item in enumerate(self.mathrule[1].role):
			labelText = _("&Child %d meaning")%(index)
			widget = childRoleGroup.addLabeledControl(labelText, wx.TextCtrl)
			widget.SetValue(unicode(item))
			self.role_widgets.append(widget)
		sHelper.addItem(childRoleGroup)

		sHelper.addDialogDismissButtons(self.CreateButtonSizer(wx.OK|wx.CANCEL))

		mainSizer.Add(sHelper.sizer,border=20,flag=wx.ALL)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)

		try:
			self.descriptionWidget.SetFocus()
		except:
			pass

		self.Bind(wx.EVT_BUTTON,self.onOk,id=wx.ID_OK)

	def onOk(self,evt):

		self.mathrule[1].description = self.descriptionWidget.GetValue()

		for index, item in enumerate(self.mathrule[1].serialized_order):
			if isinstance(item, int):
				self.mathrule[1].serialized_order[index] = self.so_widgets[index].GetSelection()
			elif isinstance(item, tuple):
				self.mathrule[1].serialized_order[index] = (self.so_widgets[index].GetValue(), u'*')
			else:
				self.mathrule[1].serialized_order[index] = self.so_widgets[index].GetValue()

		for index, item in enumerate(self.mathrule[1].role):
			self.mathrule[1].role[index] = self.role_widgets[index].GetValue()

		try:
			self.ruleEntry = ''
		except Exception as e:
			log.debugWarning("Could not add dictionary entry due to (regex error) : %s" % e)
			# Translators: This is an error message to let the user know that the dictionary entry is not valid.
			gui.messageBox(_("Regular Expression error: \"%s\".")%e, _("Dictionary Entry Error"), wx.OK|wx.ICON_WARNING, self)
			return 
		evt.Skip()

class MathRuleDialog(SettingsDialog):

	def __init__(self,parent, language):
		self.language = language
		try:
				mathrule = A8M_PM.load_math_rule(language=self.language)
		except LookupError:
				mathrule = A8M_PM.load_math_rule(language='Windows')

		self.A8M_mathrule = mathrule
		# Translators: This is the label for the symbol pronunciation dialog.
		# %s is replaced by the language for which symbol pronunciation is being edited.
		self.title = _("math rule (%s)")%self.language
		#self.mathrules = list(self.A8M_mathrule.items())
		self.mathrules = [(k, v) for k, v in self.A8M_mathrule.items() if k not in ['node', 'none'] ]
		super(MathRuleDialog, self).__init__(parent)

	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: The label for symbols list in symbol pronunciation dialog.
		mathrulesText = _("&Mathrules")
		try:
			#NVDA version >= 2019.2 syntax with autoSizeColumn keyword
			self.mathrulesList = sHelper.addLabeledControl(mathrulesText, nvdaControls.AutoWidthColumnListCtrl, autoSizeColumn=0, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
		except TypeError:
			#NVDA version <= 2019.1.1 syntax with autoSizeColumnIndex keyword
			self.mathrulesList = sHelper.addLabeledControl(mathrulesText, nvdaControls.AutoWidthColumnListCtrl, autoSizeColumnIndex=0, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
		# Translators: The label for a column in symbols list used to identify a symbol.
		self.mathrulesList.InsertColumn(0, _("Rule"))
		self.mathrulesList.InsertColumn(1, _("Description"))

		self.refresh()

		self.mathrulesList.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.onListItemFocused)

		# Used to ensure that event handlers call Skip(). Not calling skip can cause focus problems for controls. More 
		# generally the advice on the wx documentation is: "In general, it is recommended to skip all non-command events
		# to allow the default handling to take place. The command events are, however, normally not skipped as usually 
		# a single command such as a button click or menu item selection must only be processed by one handler."
		def skipEventAndCall(handler):
			def wrapWithEventSkip(event):
				if event:
					event.Skip()
				return handler()
			return wrapWithEventSkip

		bHelper = sHelper.addItem(guiHelper.ButtonHelper(orientation=wx.HORIZONTAL))

		# Translators: The label for a button to edit math rule.
		self.editButton = bHelper.addButton(self, label=_("&Edit"))
		self.editButton.Disable()

		# Translators: The label for a button to example math rule.
		self.exampleButton = bHelper.addButton(self, label=_("E&xample"))
		self.exampleButton.Disable()

		# Translators: The label for a button to recover default value.
		recoverDefaultButton = bHelper.addButton(self, label=_("&Recover default"))

		# Translators: The label for a button to import math.rule.
		importButton = bHelper.addButton(self, label=_("&Import"))

		# Translators: The label for a button to export math.rule.
		exportButton = bHelper.addButton(self, label=_("Exp&ort"))

		self.editButton.Bind(wx.EVT_BUTTON, self.OnEditClick)
		self.exampleButton.Bind(wx.EVT_BUTTON, self.OnExampleClick)
		recoverDefaultButton.Bind(wx.EVT_BUTTON, self.OnRecoverDefaultClick)
		importButton.Bind(wx.EVT_BUTTON, self.OnImportClick)
		exportButton.Bind(wx.EVT_BUTTON, self.OnExportClick)

	def postInit(self):
		self.mathrulesList.SetFocus()

	def load(self, path):
		mathrule = self.A8M_mathrule = A8M_PM.load_math_rule(path)

		self.mathrules = [(k, v) for k, v in self.A8M_mathrule.items() if k not in ['node', 'none'] ]
		self.refresh()

		return True

	def save(self, path, mathrule):
		A8M_PM.save_math_rule(mathrule, path=path)
		return True

	def clear(self):
		self.mathrules = []
		self.refresh()

	def refresh(self):
		self.mathrulesList.DeleteAllItems()
		for item in self.mathrules:
			self.mathrulesList.Append((item[0], item[1].description,))

	def onListItemFocused(self, evt):
		# ChangeValue and Selection property used because they do not cause EVNT_CHANGED to be fired.
		self.editButton.Enable()
		self.exampleButton.Enable()
		evt.Skip()

	def OnEditClick(self, evt):
		import copy
		index = self.mathrulesList.GetFirstSelected()
		mathrule = copy.deepcopy(self.mathrules[index])
		entryDialog = RuleEntryDialog(self, mathrule)
		if entryDialog.ShowModal()==wx.ID_OK:
			self.mathrules[index] = copy.deepcopy(entryDialog.mathrule)

			for key, mathrule in self.mathrules:
				self.A8M_mathrule[key] = mathrule

			self.refresh()
			self.mathrulesList.Select(index)
			self.mathrulesList.Focus(index)
			self.mathrulesList.SetFocus()
		entryDialog.Destroy()

	def OnExampleClick(self, evt):
		import copy
		from __init__ import MathMlReaderInteraction
		index = self.mathrulesList.GetFirstSelected()
		mathrule = copy.deepcopy(self.mathrules[index])
		interaction = MathMlReaderInteraction(mathMl=mathrule[1].example).mathcontent.set_mathrule(self.A8M_mathrule)

	def OnRecoverDefaultClick(self, evt):
		path = base_path
		if not self.language == 'Windows':
			path = base_path +'/locale/{0}'.format(self.language)
		pathname = os.path.join(path, 'math.rule')

		self.clear()
		self.load(pathname)

	def OnImportClick(self, evt):
		with wx.FileDialog(self, message=_("Import file..."), defaultDir=base_path, wildcard="rule files (*.rule)|*.rule") as entryDialog:
			if entryDialog.ShowModal() != wx.ID_OK:
				return
			pathname = entryDialog.GetPath()

		self.clear()
		self.load(pathname)

	def OnExportClick(self, evt):
		with wx.FileDialog(self, message=_("Export file..."), defaultDir=base_path, defaultFile="export.rule", wildcard="rule files (*.rule)|*.rule", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as entryDialog:
			if entryDialog.ShowModal() != wx.ID_OK:
				return
			pathname = entryDialog.GetPath()

		temp = {}
		for key, mathrule in self.mathrules:
			temp[key] = mathrule
		temp['node'] = self.A8M_mathrule['node']
		temp['none'] = self.A8M_mathrule['none']

		try:
			A8M_PM.save_math_rule(temp, path=pathname)
		except IOError as e:
			log.error("Error saving user unicode dictionary: %s" % e)

	def onOk(self, evt):
		for key, mathrule in self.mathrules:
			self.A8M_mathrule[key] = mathrule

		try:
			A8M_PM.save_math_rule(self.A8M_mathrule, language=self.language)
		except IOError as e:
			log.error("Error saving user unicode dictionary: %s" % e)

		A8M_PM.config_from_environ()

		super(MathRuleDialog, self).onOk(evt)

class NewLanguageAddingDialog(wx.Dialog):
	def __init__(self, parent):
		super(NewLanguageAddingDialog,self).__init__(parent, title=_("New language adding"))
		import languageHandler
		self.mainSizer=wx.BoxSizer(wx.VERTICAL)
		self.sHelper = guiHelper.BoxSizerHelper(self, orientation=wx.HORIZONTAL)

		exist_languages = os.listdir(os.path.join(base_path, 'locale'))
		self.languageNames = languageHandler.getAvailableLanguages()[:-1]
		self.languageNames = [x for x in self.languageNames if not x[0] in exist_languages]
		languageChoices = [x[1] for x in self.languageNames]
		# Translators: The label for a setting in general settings to select NVDA's interface language (once selected, NVDA must be restarted; the option user default means the user's Windows language will be used).
		languageLabelText = _("&Language:")
		self.languageList=self.sHelper.addLabeledControl(languageLabelText, wx.Choice, choices=languageChoices)
		self.languageIndex = self.languageList.Selection = 0

		languageListSize = self.languageList.GetSize()
		self.certainLanguageList = self.sHelper.addItem(wx.Choice(self, size=languageListSize))
		#self.certainLanguageList=self.sHelper.addLabeledControl(languageLabelText, wx.Choice, choices=[], size=languageListSize)
		self.certainLanguageList.Hide()

		self.certainButton = self.sHelper.addItem(wx.Button(self, label=_("&Select")))
		self.certainButton.Bind(wx.EVT_BUTTON, self.OnCertainClick)
		self.certainLanguage = None

		self.uncertainButton = self.sHelper.addItem(wx.Button(self, label=_("&Unselect")))
		self.uncertainButton.Bind(wx.EVT_BUTTON, self.OnUncertainClick)
		self.uncertainButton.Hide()

		#bHelper = sHelper.addItem(guiHelper.ButtonHelper(orientation=wx.HORIZONTAL))
		self.bHelper = guiHelper.ButtonHelper(orientation=wx.HORIZONTAL)

		# Add button
		self.unicodeDicButton = self.bHelper.addButton(self, label=_("unicode dictionary"))
		self.mathRuleButton = self.bHelper.addButton(self, label=_("math rule"))
		self.OkButton = self.bHelper.addButton(self, label=_("OK"), id=wx.ID_OK)

		# Bind button
		self.unicodeDicButton.Bind(wx.EVT_BUTTON, self.OnUnicodeDicClick)
		self.mathRuleButton.Bind(wx.EVT_BUTTON, self.OnMathRuleClick)
		self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)

		# Hide button
		self.unicodeDicButton.Disable()
		self.mathRuleButton.Disable()
		self.OkButton.Disable()

		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

		self.mainSizer.Add(self.sHelper.sizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		self.mainSizer.Add(self.bHelper.sizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)

		self.mainSizer.Fit(self)
		self.SetSizer(self.mainSizer)

	def OnCertainClick(self, evt):
		self.languageIndex = self.languageList.Selection
		self.certainLanguage = self.languageNames[self.languageIndex][0]
		src = os.path.join(base_path, 'locale', 'en')
		dst = os.path.join(base_path, 'locale', self.certainLanguage)
		try:
			shutil.copytree(src, dst, ignore=shutil.ignore_patterns('*_user.*'))
		except:
			return

		self.languageList.Clear()
		self.languageList.Append(self.languageNames[self.languageIndex][1])
		self.languageList.Selection = 0

		self.certainButton.Hide()
		self.uncertainButton.Show()
		self.unicodeDicButton.Enable()
		self.mathRuleButton.Enable()
		self.OkButton.Enable()

		self.uncertainButton.SetFocus()

		self.mainSizer.Fit(self)
		#self.mainSizer.Layout()
		self.SetSizer(self.mainSizer)

	def OnUncertainClick(self, evt):
		dst = os.path.join(base_path, 'locale', self.certainLanguage)
		try:
			shutil.rmtree(dst)
		except:
			return

		self.certainLanguage = None

		self.languageList.Clear()
		languageChoices = [x[1] for x in self.languageNames]
		self.languageList.AppendItems(languageChoices)
		self.languageList.Selection = self.languageIndex

		self.certainButton.Show()
		self.uncertainButton.Hide()
		self.unicodeDicButton.Disable()
		self.mathRuleButton.Disable()
		self.OkButton.Disable()

		self.certainButton.SetFocus()

		self.mainSizer.Fit(self)
		#self.mainSizer.Layout()
		self.SetSizer(self.mainSizer)

	def OnUnicodeDicClick(self, evt):
		gui.mainFrame._popupSettingsDialog(UnicodeDicDialog, self.certainLanguage)

	def OnMathRuleClick(self, evt):
		gui.mainFrame._popupSettingsDialog(MathRuleDialog, self.certainLanguage)

	def OnCloseWindow(self, evt):
		if self.certainLanguage:
			dst = os.path.join(base_path, 'locale', self.certainLanguage)
			try:
				shutil.rmtree(dst)
			except:
				return
			self.certainLanguage = None
		self.Destroy()

	def onOk(self, evt):
		if gui.messageBox(
			# Translators: The message displayed
			_("For the new language to add, NVDA must be restarted. Press enter to restart NVDA, or cancel to exit at a later time."),
			# Translators: The title of the dialog
			_("New language add"),wx.OK|wx.CANCEL|wx.ICON_WARNING,self
		)==wx.OK:
			queueHandler.queueFunction(queueHandler.eventQueue,core.restart)
		self.Destroy()

class AsciiMathEntryDialog(wx.TextEntryDialog):
	def __init__(self, parent, message=_("Write AsciiMath Entry")):
		super(AsciiMathEntryDialog,self).__init__(parent=parent,message=message)

class LatexEntryDialog(wx.TextEntryDialog):
	def __init__(self, parent, message=_("Write Latex Entry")):
		super(LatexEntryDialog,self).__init__(parent=parent,message=message)

from languageHandler_custom import getAvailableLanguages
path = os.path.dirname(os.path.abspath(__file__))
try:
	available_languages = getAvailableLanguages(path)
	available_languages = available_languages[:-1]
except BaseException as e:
	available_languages = []

available_languages.append(("Windows", _("build-in")))
available_languages_dict = {k: v for k, v in available_languages}
