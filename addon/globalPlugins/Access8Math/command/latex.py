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

from lib.dataProcess import joinObjectArray, groupByField

addonHandler.initTranslation()

import os
from python.csv import DictReader, DictWriter

def load():
	BASE_DIR = os.path.dirname(__file__)
	path = os.path.join(BASE_DIR, 'latexs.csv')
	data = []
	with open(path, 'r', encoding='utf-8') as src_file:
		src_dict_csv = DictReader(src_file)
		for row in src_dict_csv:
			id_ = row.pop('id')
			latex = row.pop('latex')
			offset = int(row.pop('offset'))
			shortcut = row.pop('shortcut')
			category = row.pop('category')
			data.append({
				"id": id_,
				"latex": latex,
				"offset": offset,
				"shortcut": shortcut,
				"category": category,
			})

	return data

def save(latexAll):
	print("YA")
	BASE_DIR = os.path.dirname(__file__)
	path = os.path.join(BASE_DIR, 'latexs.csv')
	src_rows = []
	with open(path, 'r', encoding='utf-8') as src_file:
		src_dict_csv = DictReader(src_file)
		fields = src_dict_csv.fieldnames.copy()
		for row in src_dict_csv:
			id_ = row.pop('id')
			latex = row.pop('latex')
			offset = int(row.pop('offset'))
			shortcut = row.pop('shortcut')
			category = row.pop('category')
			src_rows.append({
				"id": id_,
				"latex": latex,
				"offset": offset,
				"shortcut": shortcut,
				"category": category,
			})

	old_rows = []
	for row in src_rows:
		row.pop('shortcut')
		old_rows.append(row)

	for row in latexAll:
		print(row)

	shortcuts = [{"id": row["id"], "shortcut": row["shortcut"]} for row in latexAll]
	rows = joinObjectArray(shortcuts, old_rows, "id")

	path = os.path.join(BASE_DIR, 'latexs.csv')
	with open(path, 'w', encoding='utf-8', newline='') as dst_file:
		dst_dict_csv = DictWriter(dst_file, fieldnames=fields)
		dst_dict_csv.writeheader()
		for row in rows:
			dst_dict_csv.writerow(row)

	return rows

def data2command(latexAll):
	data = {}
	for row in latexAll:
		id_ = row['id']
		latex = row['latex']
		offset = int(row['offset'])
		data[id_] = {
			"text": latex,
			"offset": offset,
		}

	return data

def data2shortcut(latexAll):
	data = {}
	for row in latexAll:
		shortcut = row['shortcut']
		if int(shortcut) >= 0:
			id_ = row['id']
			name = row['name']
			data[shortcut] = {
				"id": id_,
				"name": name,
				"type": "item",
				"shortcut": shortcut,
			}

	return data

def command(text, offset):
	try:
		temp = api.getClipData()
	except:
		temp = ''
	api.copyToClip(text)

	KeyboardInputGesture.fromName("control+v").send()

	leftArrow = KeyboardInputGesture.fromName("leftArrow")
	rightArrow = KeyboardInputGesture.fromName("rightArrow")
	if offset > 0:
		for i in range(abs(offset)):
			rightArrow.send()
	else:
		for i in range(abs(offset)):
			leftArrow.send()

	if temp != '':
		wx.CallLater(100, api.copyToClip, temp)
	else:
		wx.CallLater(100, clearClipboard)

latexData = []
latexMenuData = [
	{
		"id": "frac",
		"name": _("fractions"),
	},
	{
		"id": "sqrt",
		"name": _("square root"),
	},
	{
		"id": "root",
		"name": _("root"),
	},
	{
		"id": "sumupdown",
		"name": _("summation"),
	},
	{
		"id": "vector",
		"name": _("vector"),
	},
	{
		"id": "limit",
		"name": _("limit"),
	},
	{
		"id": "times",
		"name": _("times"),
	},
	{
		"id": "div",
		"name": _("divide"),
	},
	{
		"id": "pm",
		"name": _("plus-minus sign"),
	},
	{
		"id": "ge",
		"name": _("greater than or equal to"),
	},
	{
		"id": "le",
		"name": _("less than or equal to"),
	},
	{
		"id": "ne",
		"name": _("not equal to"),
	},
	{
		"id": "parallel",
		"name": _("parallel"),
	},
	{
		"id": "perp",
		"name": _("perpendicular"),
	},
	{
		"id": "cong",
		"name": _("full equal"),
	},
	{
		"id": "sim",
		"name": _("similar"),
	},
	{
		"id": "because",
		"name": _("because"),
	},
	{
		"id": "therefore",
		"name": _("therefore"),
	},
	{
		"id": "leftarrow",
		"name": _("left arrow"),
	},
	{
		"id": "rightarrow",
		"name": _("right arrow"),
	},
	{
		"id": "leftrightarrow",
		"name": _("left right arrow"),
	},
	{
		"id": "uparrow",
		"name": _("up arrow"),
	},
	{
		"id": "downarrow",
		"name": _("down arrow"),
	},
	{
		"id": "updownarrow",
		"name": _("up down arrow"),
	},
	{
		"id": "overline",
		"name": _("line segment"),
	},
	{
		"id": "overleftrightarrow",
		"name": _("line"),
	},
	{
		"id": "overrightarrow",
		"name": _("ray"),
	},
	{
		"id": "arc",
		"name": _("arc"),
	},
	{
		"id": "triangle",
		"name": _("triangle"),
	},
	{
		"id": "angle",
		"name": _("angle"),
	},
	{
		"id": "degree",
		"name": _("degree"),
	},
	{
		"id": "circ",
		"name": _("circle"),
	},
	{
		"id": "binom",
		"name": _("binomial coefficient"),
	},
	{
		"id": "matrix2X2",
		"name": _("matrix (2X2)"),
	},
	{
		"id": "matrix3X3",
		"name": _("matrix (3X3)"),
	},
	{
		"id": "determinant2X2",
		"name": _("determinant (2X2)"),
	},
	{
		"id": "determinant3X3",
		"name": _("determinant (3X3)"),
	},
	{
		"id": "simultaneous-equations",
		"name": _("simultaneous equations"),
	},
]
latexAll = []
latexShortcut = {}
latexCommand = {}
latexMenu = {}

def initialize():
	global latexData, latexAll, latexCommand, latexShortcut, latexMenu
	latexData = load()
	latexAll = joinObjectArray(latexData, latexMenuData, key="id")
	latexMenu = [{
		**i, **{
			"type": "item",
		}
	} for i in latexAll]
	latexMenu = groupByField(latexMenu, 'category', lambda i:i, lambda i:i)

	latexCommand = data2command(latexAll)
	latexShortcut = data2shortcut(latexAll)

def terminate():
	save(latexAll)

# initialize()


class A8MLaTeXCommandModel(MenuModel):
	def __init__(self):
		super().__init__()
		self.data = [
			{
				"id": "shortcut",
				"name": _("shortcut"),
				"type": "menu",
				"items": [latexShortcut[str(k)] for k in range(1,13) if str(k) in latexShortcut],
			},
			{
				"id": "common",
				"name": _("common"),
				"type": "menu",
				"items": latexMenu['common'],
			},
			{
				"id": "operator",
				"name": _("operator"),
				"type": "menu",
				"items": latexMenu['operator'],
			},
			{
				"id": "relation",
				"name": _("relation"),
				"type": "menu",
				"items": latexMenu['relation'],
			},
			{
				"id": "arrow",
				"name": _("arrow"),
				"type": "menu",
				"items": latexMenu['arrow'],
			},
			{
				"id": "2-dimension",
				"name": _("2-dimension"),
				"type": "menu",
				"items": latexMenu['2-dimension'],
			},
			{
				"id": "other",
				"name": _("other"),
				"type": "menu",
				"items": latexMenu['other'],
			},
		]
		self.shortcut = latexShortcut

class A8MLaTeXCommandView(MenuView):
	name = _("LaTeX command")
	def __init__(self):
		super().__init__(MenuModel=A8MLaTeXCommandModel, TextInfo=A8MLaTeXCommandViewTextInfo)

	def update_menu(self):
		global latexMenu, latexShortcut
		latexMenu = [{
			**i, **{
				"type": "item",
			}
		} for i in latexAll]
		latexMenu = groupByField(latexMenu, 'category', lambda i:i, lambda i:i)

		latexShortcut = data2shortcut(latexAll)

	def getScript(self, gesture):
		if isinstance(gesture, KeyboardInputGesture):
			if len(gesture.modifierNames) == 0 and gesture.mainKeyName in ["f{}".format(i) for i in range(1, 13)]:
				return self.script_set_shortcut
			elif len(gesture.modifierNames) == 0 and gesture.mainKeyName in ["d"]:
				return self.script_reset_shortcut

		return super().getScript(gesture)

	@script(
		gestures=["kb:f{}".format(i) for i in range(1, 13)]
	)
	def script_set_shortcut(self, gesture):
		if self.data.pointer['type'] == 'menu':
			ui.message(_("menu can not set shortcut"))
			return

		id_ = self.data.pointer['id']
		slot = gesture.mainKeyName[1:]

		for item in latexAll:
			if item["id"] == id_:
				item["shortcut"] = slot
				break

		for item in latexAll:
			if item["id"] != id_ and item["shortcut"] == str(slot):
				item["shortcut"] = "-1"

		self.update_menu()
		ui.message(_("set shortcut {slot}").format(slot=slot))
		eventHandler.executeEvent("gainFocus", self.parent)

	@script(
		gestures=["kb:d"]
	)
	def script_reset_shortcut(self, gesture):
		if self.data.pointer['type'] == 'menu':
			ui.message(_("sub menu no shortcut"))
			return

		id_ = self.data.pointer['id']
		slot = self.data.pointer['shortcut']
		if slot == "-1":
			ui.message(_("no set shortcut"))
			return

		for item in latexAll:
			if item["id"] == id_:
				item["shortcut"] = "-1"
				break

		self.update_menu()
		ui.message(_("clear shortcut {slot}").format(slot=slot))
		eventHandler.executeEvent("gainFocus", self.parent)

	@script(
		gestures=["kb:enter"]
	)
	def script_enter(self, gesture):
		self.command(self.data.pointer['id'])

	def command(self, id_):
		try:
			kwargs = latexCommand[id_]
			command(**kwargs)
		except:
			tones.beep(100, 100)
			return
		eventHandler.executeEvent("gainFocus", self.parent)


class A8MLaTeXCommandViewTextInfo(MenuViewTextInfo):
	pass
