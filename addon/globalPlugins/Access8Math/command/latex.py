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

import os
from python.csv import DictReader

def load():
	BASE_DIR = os.path.dirname(__file__)
	path = os.path.join(BASE_DIR, 'latexs.csv')
	data = {}
	with open(path, 'r', encoding='utf-8') as src_file:
		src_dict_csv = DictReader(src_file)
		for row in src_dict_csv:
			id_ = row.pop('id')
			latex = row.pop('latex')
			offset = int(row.pop('offset'))
			data[id_] = {
				"text": latex,
				"offset": offset,
			}

	return data

latexCommand = load()

def command(text, offset):
	gestures = text2gestures(text)
	for gesture in gestures:
		gesture.send()

	leftArrow = KeyboardInputGesture(set(), 37, 75, True)
	rightArrow = KeyboardInputGesture(set(), 39, 77, True)
	if offset > 0:
		for i in range(abs(offset)):
			rightArrow.send()
	else:
		for i in range(abs(offset)):
			leftArrow.send()

class A8MLaTeXCommandModel(MenuModel):
	def __init__(self):
		super().__init__()
		self.data = [
			{
				"id": "common",
				"name": _("common"),
				"type": "menu",
				"items": [
					{
						"id": "frac",
						"name": _("fractions"),
						"type": "item",
					},
					{
						"id": "sqrt",
						"name": _("square root"),
						"type": "item",
					},
					{
						"id": "root",
						"name": _("root"),
						"type": "item",
					},
				],
			},
			{
				"id": "operator",
				"name": _("operator"),
				"type": "menu",
				"items": [
					{
						"id": "times",
						"name": _("times"),
						"type": "item",
					},
					{
						"id": "div",
						"name": _("divide"),
						"type": "item",
					},
					{
						"id": "circ",
						"name": _("circle"),
						"type": "item",
					},
				],
			},
			{
				"id": "relation",
				"name": _("relation"),
				"type": "menu",
				"items": [
					{
						"id": "parallel",
						"name": _("parallel"),
						"type": "item",
					},
					{
						"id": "perp",
						"name": _("perpendicular"),
						"type": "item",
					},
					{
						"id": "cong",
						"name": _("full equal"),
						"type": "item",
					},
				],
			},
			{
				"id": "arrow",
				"name": _("arrow"),
				"type": "menu",
				"items": [
					{
						"id": "leftarrow",
						"name": _("left arrow"),
						"type": "item",
					},
					{
						"id": "rightarrow",
						"name": _("right arrow"),
						"type": "item",
					},
					{
						"id": "leftrightarrow",
						"name": _("left right arrow"),
						"type": "item",
					},
					{
						"id": "uparrow",
						"name": _("up arrow"),
						"type": "item",
					},
					{
						"id": "downarrow",
						"name": _("down arrow"),
						"type": "item",
					},
					{
						"id": "updownarrow",
						"name": _("up down arrow"),
						"type": "item",
					},
				],
			},
			{
				"id": "other",
				"name": _("other"),
				"type": "menu",
				"items": [
					{
						"id": "triangle",
						"name": _("triangle"),
						"type": "item",
					},
					{
						"id": "angle",
						"name": _("angle"),
						"type": "item",
					},
					{
						"id": "overline",
						"name": _("line segment"),
						"type": "item",
					},
					{
						"id": "degree",
						"name": _("degree"),
						"type": "item",
					},
				],
			},
		]


class A8MLaTeXCommandView(MenuView):
	name = _("LaTeX command")
	def __init__(self):
		super().__init__(MenuModel=A8MLaTeXCommandModel, TextInfo=A8MLaTeXCommandViewTextInfo)

	@script(
		gestures=["kb:enter"]
	)
	def script_enter(self, gesture):
		self.command()

	def command(self):
		try:
			kwargs = latexCommand[self.data.pointer['id']]
			command(**kwargs)
		except:
			tones.beep(100, 100)
			return
		eventHandler.executeEvent("gainFocus", self.parent)


class A8MLaTeXCommandViewTextInfo(MenuViewTextInfo):
	pass
