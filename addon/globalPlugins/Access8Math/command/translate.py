import addonHandler
import api
import eventHandler
from keyboardHandler import KeyboardInputGesture
from scriptHandler import script
import wx

from delimiter import LaTeX as LaTeX_delimiter, AsciiMath as AsciiMath_delimiter, delimiter as delimiter_setting
delimiter_dict = {**AsciiMath_delimiter, **LaTeX_delimiter}

from lib.mathProcess import latex2asciimath, asciimath2latex

from .clipboard import clearClipboard
from .models import MenuModel
from .views import MenuView, MenuViewTextInfo

addonHandler.initTranslation()


def translate(section, type_):
	delimiter = delimiter_dict[delimiter_setting[type_]]
	delimiter_start = delimiter["start"]
	delimiter_end = delimiter["end"]

	if section.pointer['type'] == 'latex' and type_ == 'asciimath':
		data = latex2asciimath(section.pointer['data'])
	elif section.pointer['type'] == 'asciimath' and type_ == 'latex':
		data = asciimath2latex(section.pointer['data'])
		data = data[1:-1]
	else:
		return

	result = section.move(type='any', step=0)
	if result:
		section.caret.updateSelection()

	try:
		temp = api.getClipData()
	except:
		temp = ''

	api.copyToClip(r'{delimiter_start}{data}{delimiter_end}'.format(
		data=data,
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


class A8MTranslateCommandModel(MenuModel):
	def __init__(self):
		super().__init__()
		self.data = [
			{
				"id": "latex",
				# Translators: translate command category - LaTeX
				"name": _("LaTeX"),
				"type": "item",
			},
			{
				"id": "asciimath",
				# Translators: translate command category - AsciiMath
				"name": _("AsciiMath"),
				"type": "item",
			},
		]


class A8MTranslateCommandView(MenuView):
	# Translators: alt+m window
	name = _("translate command")

	def __init__(self, section):
		super().__init__(MenuModel=A8MTranslateCommandModel, TextInfo=MenuViewTextInfo)
		self._section = section

	@script(
		gestures=["kb:enter"]
	)
	def script_enter(self, gesture):
		self.translate(self.data.pointer['id'], self._section)

	def translate(self, id, section):
		translate(section, type_=id)
		eventHandler.executeEvent("gainFocus", self.parent)
