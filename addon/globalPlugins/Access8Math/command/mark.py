import addonHandler
import api
import eventHandler
from keyboardHandler import KeyboardInputGesture
from scriptHandler import script
import wx

from delimiter import LaTeX as LaTeX_delimiter, AsciiMath as AsciiMath_delimiter, delimiter as delimiter_setting
delimiter_dict = {**AsciiMath_delimiter, **LaTeX_delimiter}

from .clipboard import clearClipboard
from .models import MenuModel
from .views import MenuView, MenuViewTextInfo

addonHandler.initTranslation()


def mark(section, type_):
	delimiter = delimiter_dict[delimiter_setting[type_]]
	delimiter_start = delimiter["start"]
	delimiter_end = delimiter["end"]

	try:
		temp = api.getClipData()
	except BaseException:
		temp = ''
	api.copyToClip(r'{delimiter_start}{selection}{delimiter_end}'.format(
		selection=section.selection.text,
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
				"id": "latex",
				# Translators: mark command category - LaTeX
				"name": _("LaTeX"),
				"type": "item",
			},
			{
				"id": "asciimath",
				# Translators: mark command category - AsciiMath
				"name": _("AsciiMath"),
				"type": "item",
			},
		]


class A8MMarkCommandView(MenuView):
	# Translators: alt+m window
	name = _("mark command")

	def __init__(self, section):
		super().__init__(MenuModel=A8MMarkCommandModel, TextInfo=MenuViewTextInfo)
		self._section = section

	@script(
		gestures=["kb:enter"]
	)
	def script_enter(self, gesture):
		mark(self._section, type_=self.data.pointer['id'])
		eventHandler.executeEvent("gainFocus", self.parent)
