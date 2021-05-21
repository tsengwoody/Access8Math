import addonHandler
import api
import eventHandler
from keyboardHandler import KeyboardInputGesture
from scriptHandler import script
import tones
import ui
import wx

from .clipboard import clearClipboard
from .gesture import CTRL
from .models import MenuModel
from .views import MenuView, MenuViewTextInfo

addonHandler.initTranslation()

def markLaTeX():
	api.copyToClip(r'\(\)')
	gesture = KeyboardInputGesture(CTRL, 86, 47, False)
	gesture.send()

	leftArrow = KeyboardInputGesture(set(), 37, 75, True)
	leftArrow.send()
	leftArrow.send()
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
