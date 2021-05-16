import addonHandler
import eventHandler
from keyboardHandler import KeyboardInputGesture
from scriptHandler import script
import tones
import ui

from .gesture import text2gestures
from .models import MenuModel
from .views import MenuView, MenuViewTextInfo

addonHandler.initTranslation()

def markLaTeX():
	gestures = text2gestures(r'\(\)')
	for gesture in gestures:
		gesture.send()

	leftArrow = KeyboardInputGesture(set(), 37, 75, True)
	leftArrow.send()
	leftArrow.send()


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
