import addonHandler
import api
import eventHandler
from keyboardHandler import KeyboardInputGesture
from scriptHandler import script

import wx

from delimiter import LaTeX as LaTeX_delimiter, AsciiMath as AsciiMath_delimiter
delimiter_dict = {**AsciiMath_delimiter, **LaTeX_delimiter}

from .clipboard import clearClipboard
from .models import MenuModel
from .views import MenuView, MenuViewTextInfo

addonHandler.initTranslation()


def batch(section, mode):
	old_all_index = section.all_index
	text = section.batch(mode)

	try:
		temp = api.getClipData()
	except:
		temp = ''

	api.copyToClip(text)

	KeyboardInputGesture.fromName("control+a").send()
	KeyboardInputGesture.fromName("control+v").send()

	def move():
		with section.__enter__() as manager:
			manager.move(all_index=old_all_index)
	wx.CallLater(100, move)

	if temp != '':
		wx.CallLater(100, api.copyToClip, temp)
	else:
		wx.CallLater(100, clearClipboard)


class A8MBatchCommandModel(MenuModel):
	def __init__(self):
		super().__init__()
		self.data = [
			{
				"id": "mathblock",
				# Translators: batch menu
				"name": _("math block"),
				"type": "menu",
				"items": [
					{
						"id": "latex2asciimath",
						# Translators: batch menu
						"name": _("LaTeX to AsciiMath"),
						"type": "item",
					},
					{
						"id": "asciimath2latex",
						# Translators: batch menu
						"name": _("AsciiMath to LaTeX"),
						"type": "item",
					},
					{
						"id": "reverse",
						# Translators: batch menu
						"name": _("LaTeX and AsciiMath reverse translate"),
						"type": "item",
					},
				],
			},
			{
				"id": "delimiter",
				# Translators: batch menu
				"name": _("LaTeX delimiter"),
				"type": "menu",
				"items": [
					{
						"id": "bracket2dollar",
						# Translators: batch menu
						"name": _("bracket to dollar"),
						"type": "item",
					},
					{
						"id": "dollar2bracket",
						# Translators: batch menu
						"name": _("dollar to bracket"),
						"type": "item",
					},
				],
			},
		]


class A8MBatchCommandView(MenuView):
	# Translators: alt+m window
	name = _("batch command")

	def __init__(self, section):
		super().__init__(MenuModel=A8MBatchCommandModel, TextInfo=MenuViewTextInfo)
		self._section = section

	@script(
		gestures=["kb:enter"]
	)
	def script_enter(self, gesture):
		if self.data.pointer['id'] in ['asciimath2latex', 'latex2asciimath', 'reverse', 'bracket2dollar', 'dollar2bracket']:
			batch(self._section, mode=self.data.pointer['id'])
		eventHandler.executeEvent("gainFocus", self.parent)
