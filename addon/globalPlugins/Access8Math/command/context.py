import json
import os
import shutil

import addonHandler
import eventHandler
import gui
from scriptHandler import script
import ui
import wx

from .models import MenuModel
from .views import MenuView, MenuViewTextInfo
from ..editor import EditorFrame
from ..lib.viewHTML import Access8MathDocument


addonHandler.initTranslation()


class A8MFEVContextMenuModel(MenuModel):
	def __init__(self):
		super().__init__()
		self.data = [
			{
				"id": "view",
				"name": _("view"),
				"type": "item",
			},
			{
				"id": "edit",
				"name": _("edit"),
				"type": "item",
			},
		]


class A8MFEVContextMenuView(MenuView):
	name = _("virtual context menu")

	def __init__(self, path):
		super().__init__(MenuModel=A8MFEVContextMenuModel, TextInfo=A8MFEVContextMenuViewTextInfo)
		self.path = path
		self.ad = Access8MathDocument(path)

	@script(
		gestures=["kb:enter"]
	)
	def script_enter(self, gesture):
		if self.data.pointer['id'] == 'view':
			self.OnView()
		elif self.data.pointer['id'] == 'edit':
			self.OnEdit()

	def OnView(self):
		self.ad.raw2review()
		os.startfile(os.path.join(self.ad.review_entry))
		eventHandler.executeEvent("gainFocus", self.parent)

	def OnEdit(self):
		def show():
			try:
				frame = EditorFrame(self.path).Show(True)
			except BaseException as e:
				ui.message(_("open path failed"))
				print(e)
		eventHandler.executeEvent("gainFocus", self.parent)
		wx.CallAfter(show)


class A8MFEVContextMenuViewTextInfo(MenuViewTextInfo):
	pass
