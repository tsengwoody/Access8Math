import json
import os
import shutil
import wx

import addonHandler
import gui

from lib.viewHTML import raw2review

addonHandler.initTranslation()

PATH = os.path.dirname(__file__)

wildcard = \
	"Text (*.txt)|*.txt|"\
	"All (*.*)|*.*"

class EditorFrame(wx.Frame):
	# Translators: The name of the document in the Editor when it has never been saved to a file
	def __init__(self, parent, filename=_("New document")):
		style = wx.DEFAULT_FRAME_STYLE & (~wx.CLOSE_BOX)
		super(EditorFrame, self).__init__(parent, size=(400, 300), style=style)

		self.parent = parent
		self.dirname  = "."
		self.filename = filename
		self.review_folder = os.path.join(PATH, 'web', 'review')
		self.modify = False

		# Simplified init method.	   
		self.CreateInteriorWindowComponents()
		self.CreateExteriorWindowComponents()
		self.CenterOnScreen()

		Hotkey(self)

	def SetTitle(self):
		# Translators: The title of the Editor window
		super(EditorFrame, self).SetTitle(_("%s - Access8Math Editor") % self.filename)

	def CreateInteriorWindowComponents(self):
		self.control = wx.TextCtrl(self, -1, value="", style=wx.TE_MULTILINE)
		self.control.Bind(wx.EVT_TEXT, self.OnTextChanged)

	def CreateExteriorWindowComponents(self):
		self.SetTitle()

		# frameIcon = wx.Icon(os.path.join(self.icons_dir,
			# "icon_wxWidgets.ico"),
			# type=wx.BITMAP_TYPE_ICO)
		# self.SetIcon(frameIcon)

		self.CreateMenu()
		self.CreateStatusBar()
		self.BindEvents()

	def CreateMenu(self):
		menuBar = wx.MenuBar()

		fileMenu = wx.Menu()

		for id, label, helpText, handler in [
			(
				wx.ID_NEW,
				# Translators: A menu item in the Editor window
				_("&New"),
				# Translators: The help description text shown in the status bar in the Editor window when a menu item is selected
				_("Open a new editor."),
				self.OnNew
			), (
				wx.ID_OPEN,
				# Translators: A menu item in the Editor window
				_("&Open..."),
				# Translators: The help description text shown in the status bar in the Editor window when a menu item is selected
				_("Open a new file."),
				self.OnOpen
			), (
				wx.ID_SAVE,
				# Translators: A menu item in the Editor window
				_("&Save"),
				# Translators: The help description text shown in the status bar in the Editor window when a menu item is selected
				_("Save the current file."),
				self.OnSave
			), (
				wx.ID_SAVEAS,
				# Translators: A menu item in the Editor window
				_("Save &as..."),
				# Translators: The help description text shown in the status bar in the Editor window when a menu item is selected
				_("Save the file under a different name."),
				self.OnSaveAs
			), (
				wx.ID_ANY,
				# Translators: A menu item in the Editor window
				_("Re&load from disk"),
				# Translators: The help description text shown in the status bar in the Editor window when a menu item is selected
				_("Reload the file from disk."),
				self.OnReload
			), (
				wx.ID_EXIT,
				# Translators: A menu item in the Editor window
				_("E&xit"),
				# Translators: The help description text shown in the status bar in the Editor window when a menu item is selected
				_("Terminate the program."),
				self.OnExit
			)
		]:
			if id == None:
				fileMenu.AppendSeparator()
			else:
				item = fileMenu.Append(id, label, helpText)

				# Bind some events to an events handler.
				self.Bind(wx.EVT_MENU, handler, item)

		# Add the fileMenu to the menuBar.
		# Translators: A menu item in the Editor window
		menuBar.Append(fileMenu, _("&File"))

		viewMenu = wx.Menu()

		for id, label, helpText, handler in [
			(
				wx.ID_ANY,
				# Translators: A menu item in the Editor window
				_("Preview"),
				# Translators: The help description text shown in the status bar in the Editor window when a menu item is selected
				_("Preview HTML file"),
				self.OnPreview
			), (
				wx.ID_ANY,
				# Translators: A menu item in the Editor window
				_("Export..."),
				# Translators: The help description text shown in the status bar in the Editor window when a menu item is selected
				_("Export HTML file"),
				self.OnExport
			),
		]:
			if id == None:
				viewMenu.AppendSeparator()
			else:
				item = viewMenu.Append(id, label, helpText)

				# Bind some events to an events handler.
				self.Bind(wx.EVT_MENU, handler, item)

		# Add the fileMenu to the menuBar.
		# Translators: A menu item in the Editor window
		menuBar.Append(viewMenu, _("&View"))

		# Add the menuBar to the frame.
		self.SetMenuBar(menuBar)

	def BindEvents(self):
		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

	def DefaultFileDialogOptions(self):
		return dict(
			defaultFile=self.filename,
			defaultDir=self.dirname,
			wildcard=wildcard,
		)
   
	def AskUserForFilename(self, **dialogOptions):
		with wx.FileDialog(self, **dialogOptions) as dialog:
			if dialog.ShowModal() == wx.ID_OK:
				userProvidedFilename = True
				self.filename = dialog.GetFilename()
				self.dirname = dialog.GetDirectory()
				# Update the window title with the new filename.
				self.SetTitle() 
			else:
				userProvidedFilename = False
		# dialog.Destroy()
		return userProvidedFilename

	def OnNew(self, event):
		frame = self.__class__(parent=self.parent)
		frame.Show(True)

	def OnOpen(self, event):
		# Translators: The title of the Editor's Open file window
		if self.AskUserForFilename(message=_("Open file"), style=wx.FD_OPEN, **self.DefaultFileDialogOptions()):
			with open(os.path.join(self.dirname, self.filename), 'r', encoding='utf-8') as file:
				self.control.SetValue(file.read())
			self.modify = False

	def OnSave(self, event):
		# Translators: The name of the document in the Editor when it has never been saved to a file
		if self.filename == _("New document"):
			# Translators: The title of the Editor's Save file window
			if self.AskUserForFilename(message=_("Save file"), style=wx.FD_SAVE, **self.DefaultFileDialogOptions()):
				with open(os.path.join(self.dirname, self.filename), 'w', encoding='utf-8') as file:
					file.write(self.control.GetValue())
				self.modify = False
				return True
			else:
				return False
		else:
			with open(os.path.join(self.dirname, self.filename), 'w', encoding='utf-8') as file:
				file.write(self.control.GetValue())
			self.modify = False
			return True

	def OnSaveAs(self, event):
		# Translators: The title of the Editor's Save as file window
		if self.AskUserForFilename(message=_("Save file"), style=wx.FD_SAVE, **self.DefaultFileDialogOptions()):
			with open(os.path.join(self.dirname, self.filename), 'w', encoding='utf-8') as file:
				file.write(self.control.GetValue())
			self.modify = False

	def OnReload(self, event):
		# Translators: The name of the document in the Editor when it has never been saved to a file
		if self.filename == _("New document"):
			pass
		else:
			with open(os.path.join(self.dirname, self.filename), 'r', encoding='utf-8') as file:
				self.control.SetValue(file.read())
			self.modify = False

	def OnExit(self, event):
		if self.modify:
			# Translators: The name of the document in the Editor when it has never been saved to a file
			if self.filename == _("New document"):
				path = ' "' + self.filename + '"'
			else:
				path = ' "' + os.path.join(self.dirname, self.filename) + '"'
			val = gui.messageBox(
				# Translators: The message displayed
				_("Save file{path}?").format(path=path),
				# Translators: The title of the dialog
				_("Save"),
				wx.YES_NO | wx.YES_DEFAULT | wx.CANCEL | wx.ICON_QUESTION, self
			)
			if val == wx.YES:
				result = self.OnSave(event)
				if result:
					self.Destroy()
			elif val == wx.NO:
				self.Destroy()
		else:
			self.Destroy()

	def OnPreview(self, event):
		save_result = False
		# Translators: The name of the document in the Editor when it has never been saved to a file
		if self.filename == _("New document"):
			save_result = self.OnSave(event)
		else:
			if self.modify:
				val = gui.messageBox(
					# Translators: The message displayed
					_("Preview will only include the saved content. The content in the editor has been modified since the last save, do you want to save and preview it?"),
					# Translators: The title of the dialog
					_("Preview"),
					wx.YES_NO | wx.YES_DEFAULT | wx.CANCEL | wx.ICON_QUESTION, self
				)
				if val == wx.YES:
					save_result = self.OnSave(event)
				elif val == wx.NO:
					save_result = True
				elif val == wx.CANCEL:
					return
			else:
				save_result = True

		if not save_result:
			return

		raw2review(self.dirname, self.filename, self.review_folder)
		dst = os.path.join(self.review_folder, 'Access8Math.json')
		with open(dst, 'r', encoding='utf8') as f:
			metadata = json.load(f)
		entry_file = metadata['entry']
		os.startfile(os.path.join(self.review_folder, entry_file))

	def OnExport(self, event):
		save_result = False
		# Translators: The name of the document in the Editor when it has never been saved to a file
		if self.filename == _("New document"):
			save_result = self.OnSave(event)
		else:
			if self.modify:
				val = gui.messageBox(
					# Translators: The message displayed
					_("Export will only include the saved content. The content in the editor has been modified since the last save, do you want to save and export it?"),
					# Translators: The title of the dialog
					_("Export"),
					wx.YES_NO | wx.YES_DEFAULT | wx.CANCEL | wx.ICON_QUESTION, self
				)
				if val == wx.YES:
					save_result = self.OnSave(event)
				elif val == wx.NO:
					save_result = True
				elif val == wx.CANCEL:
					return
			else:
				save_result = True

		if not save_result:
			return

		raw2review(self.dirname, self.filename, self.review_folder)
		with wx.FileDialog(
			# Translators: The title of the Editor's Export file window
			self, message=_("Export file..."),
			defaultDir=self.dirname, wildcard="zip files (*.zip)|*.zip"
		) as entryDialog:
			if entryDialog.ShowModal() != wx.ID_OK:
				return
			dst = entryDialog.GetPath()
		dst = dst[:-4]
		shutil.make_archive(dst, 'zip', self.review_folder)

	def OnCloseWindow(self, event):
		pass
		# self.Destroy()

	def Destroy(self):
		super().Destroy()

	def OnTextChanged(self, event):
		self.modify = True


class Hotkey(object):
	def __init__(self, obj):
		self.obj = obj
		self.obj.control.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
		self.obj.control.Bind(wx.EVT_KEY_UP, self.onKeyUp)

		self.key_down = set([])
		self.key_map_action = [
			{
				'key': [wx.WXK_CONTROL, ord('N')],
				'action': self.OnNew,
			},
			{
				'key': [wx.WXK_CONTROL, ord('O')],
				'action': self.OnOpen,
			},
			{
				'key': [wx.WXK_CONTROL, ord('S')],
				'action': self.OnSave,
			},
			{
				'key': [wx.WXK_CONTROL, ord('W')],
				'action': self.OnExit,
			},
			{
				'key': [wx.WXK_ALT, wx.WXK_F4],
				'action': self.OnExit,
			},
		]

	def OnNew(self, event):
		self.obj.OnNew(event)

	def OnOpen(self, event):
		self.obj.OnOpen(event)

	def OnSave(self, event):
		self.obj.OnSave(event)

	def OnSaveAs(self, event):
		self.obj.OnSaveAs(event)

	def OnReload(self, event):
		self.obj.OnReload(event)

	def OnExit(self, event):
		self.obj.OnExit(event)

	def onKeyDown(self, event):
		keycode = event.GetKeyCode()
		self.key_down.add(keycode)
		action = False
		for item in self.key_map_action:
			if self.key_down == set(item['key']):
				self.key_down.clear()
				item['action'](event)
				action = True
				break
		if not action:
			event.Skip()

	def onKeyUp(self, event):
		keycode = event.GetKeyCode()	
		try:
			self.key_down.remove(keycode)
		except KeyError:
			self.key_down.clear()
		event.Skip()
