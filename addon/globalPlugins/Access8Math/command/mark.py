import addonHandler
import api
import eventHandler
from keyboardHandler import KeyboardInputGesture
from scriptHandler import script
import tones
import ui
import wx

from .clipboard import clearClipboard
from .models import MenuModel
from .views import MenuView, MenuViewTextInfo

addonHandler.initTranslation()

def markLaTeX(selection, delimiter):
	delimiter_start = delimiter["start"]
	delimiter_end = delimiter["end"]

	try:
		temp = api.getClipData()
	except:
		temp = ''
	api.copyToClip(r'{delimiter_start}{selection}{delimiter_end}'.format(
		selection=selection,
		delimiter_start=delimiter_start,
		delimiter_end=delimiter_end,
		))

	KeyboardInputGesture.fromName("control+v").send()

	leftArrow = KeyboardInputGesture.fromName("leftArrow")
	for i in range(len(delimiter_end)):
		leftArrow.send()

	if temp != '':
		wx.CallLater(100, api.copyToClip, temp)
	else:
		wx.CallLater(100, clearClipboard)


class A8MMarkCommandModel(MenuModel):
	def __init__(self):
		super().__init__()
		self.data = [
			{
				"id": "LaTeX",
				"name": _("LaTeX"),
				"type": "item",
			},
		]


class A8MMarkCommandView(MenuView):
	name = _("mark command")
	def __init__(self, selection, delimiter):
		super().__init__(MenuModel=A8MMarkCommandModel, TextInfo=A8MMarkCommandViewTextInfo)
		self._selection = selection
		self.delimiter = delimiter

	@script(
		gestures=["kb:enter"]
	)
	def script_enter(self, gesture):
		self.markLaTeX()

	def markLaTeX(self):
		eventHandler.executeEvent("gainFocus", self.parent)
		markLaTeX(self._selection, self.delimiter)


class A8MMarkCommandViewTextInfo(MenuViewTextInfo):
	pass
