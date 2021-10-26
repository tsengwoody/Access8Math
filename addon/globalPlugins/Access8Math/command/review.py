import os
import shutil

import addonHandler
import gui
from scriptHandler import script
import wx

from .models import MenuModel
from .views import MenuView, MenuViewTextInfo

PATH = os.path.dirname(os.path.dirname(__file__))

addonHandler.initTranslation()


class A8MHTMLCommandModel(MenuModel):
	def __init__(self):
		super().__init__()
		self.data = [
			{
				"id": "review",
				"name": _("review"),
				"type": "item",
			},
			{
				"id": "export",
				"name": _("export"),
				"type": "item",
			},
		]


class A8MHTMLCommandView(MenuView):
	name = _("Access8Math HTML")

	def __init__(self, file):
		super().__init__(MenuModel=A8MHTMLCommandModel, TextInfo=A8MHTMLCommandViewTextInfo)
		self.file = file

	@script(
		gestures=["kb:enter"]
	)
	def script_enter(self, gesture):
		if self.data.pointer['id'] == 'review':
			self.OnReview()
		elif self.data.pointer['id'] == 'export':
			self.OnExport()

	def OnReview(self):
		def openfile():
			os.startfile(self.file)
		wx.CallAfter(openfile)

	def OnExport(self):
		def show():
			with wx.FileDialog(gui.mainFrame, message=_("Save file..."), wildcard="zip files (*.zip)|*.zip", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dialog:
				if dialog.ShowModal() != wx.ID_OK:
					return
				src = os.path.join(PATH, 'web', 'review')
				dst = dialog.GetPath()[:-4]
				shutil.make_archive(dst, 'zip', src)
		wx.CallAfter(show)


class A8MHTMLCommandViewTextInfo(MenuViewTextInfo):
	pass
