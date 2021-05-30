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

def markLaTeX():
	try:
		temp = api.getClipData()
	except:
		temp = ''
	api.copyToClip(r'\(\)')

	KeyboardInputGesture.fromName("control+v").send()

	leftArrow = KeyboardInputGesture.fromName("leftArrow")
	leftArrow.send()
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
	def __init__(self):
		super().__init__(MenuModel=A8MMarkCommandModel, TextInfo=A8MMarkCommandViewTextInfo)

	@script(
		gestures=["kb:enter"]
	)
	def script_enter(self, gesture):
		self.markLaTeX()

	def markLaTeX(self):
		eventHandler.executeEvent("gainFocus", self.parent)
		markLaTeX()


class A8MMarkCommandViewTextInfo(MenuViewTextInfo):
	pass
