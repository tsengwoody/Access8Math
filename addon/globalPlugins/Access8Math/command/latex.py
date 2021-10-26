import addonHandler
import api
import eventHandler
from keyboardHandler import KeyboardInputGesture
from scriptHandler import script
import tones
import ui
import wx

from delimiter import LaTeX as LaTeX_delimiter, AsciiMath as AsciiMath_delimiter, delimiter as delimiter_setting
delimiter_dict = {**AsciiMath_delimiter, **LaTeX_delimiter}

from .clipboard import clearClipboard
from .models import MenuModel
from .views import MenuView, MenuViewTextInfo

from lib.dataProcess import joinObjectArray, groupByField

addonHandler.initTranslation()

import os
from python.csv import DictReader, DictWriter


def load(path):
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


def save(path, latexAll):
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

	shortcuts = [{"id": row["id"], "shortcut": row["shortcut"]} for row in latexAll]
	rows = joinObjectArray(shortcuts, old_rows, "id")

	with open(path, 'w', encoding='utf-8', newline='') as dst_file:
		dst_dict_csv = DictWriter(dst_file, fieldnames=fields)
		dst_dict_csv.writeheader()
		for row in rows:
			dst_dict_csv.writerow(row)

	return rows


def data2commandMap(latexAll):
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


def data2shortcutMap(latexAll):
	data = {}
	for row in latexAll:
		shortcut = row['shortcut']
		if shortcut != -1:
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


latexMenuData = [
	{
		"id": "frac",
		# Translators: LaTeX command - fractions
		"name": _("fractions"),
	},
	{
		"id": "sqrt",
		# Translators: LaTeX command - square root
		"name": _("square root"),
	},
	{
		"id": "root",
		# Translators: LaTeX command - root
		"name": _("root"),
	},
	{
		"id": "sumupdown",
		# Translators: LaTeX command - summation
		"name": _("summation"),
	},
	{
		"id": "vector",
		# Translators: LaTeX command - vector
		"name": _("vector"),
	},
	{
		"id": "limit",
		# Translators: LaTeX command - limit
		"name": _("limit"),
	},
	{
		"id": "times",
		# Translators: LaTeX command - times
		"name": _("times"),
	},
	{
		"id": "div",
		# Translators: LaTeX command - divide
		"name": _("divide"),
	},
	{
		"id": "pm",
		# Translators: LaTeX command - plus-minus sign
		"name": _("plus-minus sign"),
	},
	{
		"id": "ge",
		# Translators: LaTeX command - greater than or equal to
		"name": _("greater than or equal to"),
	},
	{
		"id": "le",
		# Translators: LaTeX command - less than or equal to
		"name": _("less than or equal to"),
	},
	{
		"id": "ne",
		# Translators: LaTeX command - not equal to
		"name": _("not equal to"),
	},
	{
		"id": "approx",
		# Translators: LaTeX command - approximate
		"name": _("approximate"),
	},
	{
		"id": "parallel",
		# Translators: LaTeX command - parallel
		"name": _("parallel"),
	},
	{
		"id": "perp",
		# Translators: LaTeX command - perpendicular
		"name": _("perpendicular"),
	},
	{
		"id": "cong",
		# Translators: LaTeX command - full equal
		"name": _("full equal"),
	},
	{
		"id": "sim",
		# Translators: LaTeX command - similar
		"name": _("similar"),
	},
	{
		"id": "because",
		# Translators: LaTeX command - because
		"name": _("because"),
	},
	{
		"id": "therefore",
		# Translators: LaTeX command - therefore
		"name": _("therefore"),
	},
	{
		"id": "leftarrow",
		# Translators: LaTeX command - left arrow
		"name": _("left arrow"),
	},
	{
		"id": "rightarrow",
		# Translators: LaTeX command - right arrow
		"name": _("right arrow"),
	},
	{
		"id": "leftrightarrow",
		# Translators: LaTeX command - left right arrow
		"name": _("left right arrow"),
	},
	{
		"id": "uparrow",
		# Translators: LaTeX command - up arrow
		"name": _("up arrow"),
	},
	{
		"id": "downarrow",
		# Translators: LaTeX command - down arrow
		"name": _("down arrow"),
	},
	{
		"id": "updownarrow",
		# Translators: LaTeX command - up down arrow
		"name": _("up down arrow"),
	},
	{
		"id": "overline",
		# Translators: LaTeX command - line segment
		"name": _("line segment"),
	},
	{
		"id": "overleftrightarrow",
		# Translators: LaTeX command - line
		"name": _("line"),
	},
	{
		"id": "overrightarrow",
		# Translators: LaTeX command - ray
		"name": _("ray"),
	},
	{
		"id": "arc",
		# Translators: LaTeX command - arc
		"name": _("arc"),
	},
	{
		"id": "triangle",
		# Translators: LaTeX command - triangle
		"name": _("triangle"),
	},
	{
		"id": "angle",
		# Translators: LaTeX command - angle
		"name": _("angle"),
	},
	{
		"id": "degree",
		# Translators: LaTeX command - degree
		"name": _("degree"),
	},
	{
		"id": "circ",
		# Translators: LaTeX command - circle
		"name": _("circle"),
	},
	{
		"id": "binom",
		# Translators: LaTeX command - binomial coefficient
		"name": _("binomial coefficient"),
	},
	{
		"id": "matrix2X2",
		# Translators: LaTeX command - matrix (2X2)
		"name": _("matrix (2X2)"),
	},
	{
		"id": "matrix3X3",
		# Translators: LaTeX command - matrix (3X3)
		"name": _("matrix (3X3)"),
	},
	{
		"id": "determinant2X2",
		# Translators: LaTeX command - determinant (2X2)
		"name": _("determinant (2X2)"),
	},
	{
		"id": "determinant3X3",
		# Translators: LaTeX command - determinant (3X3)
		"name": _("determinant (3X3)"),
	},
	{
		"id": "simultaneous-equations",
		# Translators: LaTeX command - simultaneous equations
		"name": _("simultaneous equations"),
	},
	{
		"id": "in",
		# Translators: LaTeX command - belong to
		"name": _("belong to"),
	},
	{
		"id": "notin",
		# Translators: LaTeX command - not belong to
		"name": _("not belong to"),
	},
	{
		"id": "subset",
		# Translators: LaTeX command - lie in
		"name": _("lie in"),
	},
	{
		"id": "subsetneqq",
		# Translators: LaTeX command - properly lie in
		"name": _("properly lie in"),
	},
	{
		"id": "not-subset",
		# Translators: LaTeX command - not lie in
		"name": _("not lie in"),
	},
	{
		"id": "supset",
		# Translators: LaTeX command - include
		"name": _("include"),
	},
	{
		"id": "supsetneqq",
		# Translators: LaTeX command - properly include
		"name": _("properly include"),
	},
	{
		"id": "not-supset",
		# Translators: LaTeX command - not include
		"name": _("not include"),
	},
	{
		"id": "cap",
		# Translators: LaTeX command - intersection set
		"name": _("intersection set"),
	},
	{
		"id": "cup",
		# Translators: LaTeX command - union set
		"name": _("union set"),
	},
	{
		"id": "setminus",
		# Translators: LaTeX command - difference set
		"name": _("difference set"),
	},
	{
		"id": "complement",
		# Translators: LaTeX command - complement
		"name": _("complement"),
	},
	{
		"id": "emptyset",
		# Translators: LaTeX command - empty set
		"name": _("empty set"),
	},
	{
		"id": "natural-number",
		# Translators: LaTeX command - natural number
		"name": _("natural number"),
	},
	{
		"id": "real-number",
		# Translators: LaTeX command - real number
		"name": _("real number"),
	},
	{
		"id": "logarithm",
		# Translators: LaTeX command - logarithm
		"name": _("logarithm"),
	},
	{
		"id": "infty",
		# Translators: LaTeX command - infty
		"name": _("infty"),
	},
	{
		"id": "forall",
		# Translators: LaTeX command - for all
		"name": _("for all"),
	},
	{
		"id": "exists",
		# Translators: LaTeX command - exists
		"name": _("exists"),
	},
	{
		"id": "repeating-decimal",
		# Translators: LaTeX command - repeating decimal
		"name": _("repeating decimal"),
	},
]
latexData = []
latexAll = []
latexShortcut = {}
latexCommand = {}
latexMenu = {}

greekAlphabetMenuData = [
	{
		"id": "alpha",
		# Translators: greek alphabet command - alpha
		"name": _("alpha"),
	},
	{
		"id": "beta",
		# Translators: greek alphabet command - beta
		"name": _("beta"),
	},
	{
		"id": "gamma",
		# Translators: greek alphabet command - gamma
		"name": _("gamma"),
	},
	{
		"id": "delta",
		# Translators: greek alphabet command - delta
		"name": _("delta"),
	},
	{
		"id": "epsilon",
		# Translators: greek alphabet command - epsilon
		"name": _("epsilon"),
	},
	{
		"id": "zeta",
		# Translators: greek alphabet command - zeta
		"name": _("zeta"),
	},
	{
		"id": "eta",
		# Translators: greek alphabet command - eta
		"name": _("eta"),
	},
	{
		"id": "theta",
		# Translators: greek alphabet command - theta
		"name": _("theta"),
	},
	{
		"id": "iota",
		# Translators: greek alphabet command - iota
		"name": _("iota"),
	},
	{
		"id": "kappa",
		# Translators: greek alphabet command - kappa
		"name": _("kappa"),
	},
	{
		"id": "lambda",
		# Translators: greek alphabet command - lambda
		"name": _("lambda"),
	},
	{
		"id": "mu",
		# Translators: greek alphabet command - mu
		"name": _("mu"),
	},
	{
		"id": "nu",
		# Translators: greek alphabet command - nu
		"name": _("nu"),
	},
	{
		"id": "xi",
		# Translators: greek alphabet command - xi
		"name": _("xi"),
	},
	{
		"id": "o",
		# Translators: greek alphabet command - o
		"name": _("o"),
	},
	{
		"id": "pi",
		# Translators: greek alphabet command - pi
		"name": _("pi"),
	},
	{
		"id": "rho",
		# Translators: greek alphabet command - rho
		"name": _("rho"),
	},
	{
		"id": "sigma",
		# Translators: greek alphabet command - sigma
		"name": _("sigma"),
	},
	{
		"id": "tau",
		# Translators: greek alphabet command - tau
		"name": _("tau"),
	},
	{
		"id": "upsilon",
		# Translators: greek alphabet command - upsilon
		"name": _("upsilon"),
	},
	{
		"id": "phi",
		# Translators: greek alphabet command - phi
		"name": _("phi"),
	},
	{
		"id": "chi",
		# Translators: greek alphabet command - chi
		"name": _("chi"),
	},
	{
		"id": "psi",
		# Translators: greek alphabet command - psi
		"name": _("psi"),
	},
	{
		"id": "omega",
		# Translators: greek alphabet command - down omega
		"name": _("omega"),
	},
]
greekAlphabetData = []
greekAlphabetAll = []
greekAlphabetShortcut = {}
greekAlphabetCommand = {}
greekAlphabetMenu = {}


def initialize():
	global latexData, latexAll, latexCommand, latexShortcut, latexMenu
	BASE_DIR = os.path.dirname(__file__)
	path = os.path.join(BASE_DIR, 'latexs.csv')
	latexData = load(path)
	latexAll = joinObjectArray(latexData, latexMenuData, key="id")
	latexMenu = [{
		**i, **{
			"type": "item",
		}
	} for i in latexAll]
	latexMenu = groupByField(latexMenu, 'category', lambda i: i, lambda i: i)
	latexCommand = data2commandMap(latexAll)
	latexShortcut = data2shortcutMap(latexAll)

	global greekAlphabetData, greekAlphabetAll, greekAlphabetCommand, greekAlphabetShortcut, greekAlphabetMenu
	BASE_DIR = os.path.dirname(__file__)
	path = os.path.join(BASE_DIR, 'GreekAlphabets.csv')
	greekAlphabetData = load(path)
	greekAlphabetAll = joinObjectArray(greekAlphabetData, greekAlphabetMenuData, key="id")
	greekAlphabetMenu = [{
		**i, **{
			"type": "item",
		}
	} for i in greekAlphabetAll]
	greekAlphabetMenu = groupByField(greekAlphabetMenu, 'category', lambda i: i, lambda i: i)
	greekAlphabetCommand = data2commandMap(greekAlphabetAll)
	greekAlphabetShortcut = data2shortcutMap(greekAlphabetAll)


def terminate():
	BASE_DIR = os.path.dirname(__file__)
	path = os.path.join(BASE_DIR, 'latexs.csv')
	save(path, latexAll)


class A8MLaTeXCommandModel(MenuModel):
	def __init__(self):
		super().__init__()
		self.data = [
			{
				"id": "shortcut",
				# Translators: LaTeX command category - shortcut
				"name": _("shortcut"),
				"type": "menu",
				"items": [latexShortcut[str(k)] for k in range(1, 13) if str(k) in latexShortcut],
			},
			{
				"id": "common",
				# Translators: LaTeX command category - common
				"name": _("common"),
				"type": "menu",
				"items": latexMenu['common'],
			},
			{
				"id": "operator",
				# Translators: LaTeX command category - operator
				"name": _("operator"),
				"type": "menu",
				"items": latexMenu['operator'],
			},
			{
				"id": "relation",
				# Translators: LaTeX command category - relation
				"name": _("relation"),
				"type": "menu",
				"items": latexMenu['relation'],
			},
			{
				"id": "arrow",
				# Translators: LaTeX command category - arrow
				"name": _("arrow"),
				"type": "menu",
				"items": latexMenu['arrow'],
			},
			{
				"id": "2-dimension",
				# Translators: LaTeX command category - 2-dimension
				"name": _("2-dimension"),
				"type": "menu",
				"items": latexMenu['2-dimension'],
			},
			{
				"id": "set",
				# Translators: LaTeX command category - set
				"name": _("set"),
				"type": "menu",
				"items": latexMenu['set'],
			},
			{
				"id": "other",
				# Translators: LaTeX command category - other
				"name": _("other"),
				"type": "menu",
				"items": latexMenu['other'],
			},
		]
		self.shortcut = latexShortcut
		self.greekAlphabet = greekAlphabetShortcut


class A8MLaTeXCommandView(MenuView):
	# Translators: alt+l window
	name = _("LaTeX command")

	def __init__(self, selection, inSection=True):
		super().__init__(MenuModel=A8MLaTeXCommandModel, TextInfo=A8MLaTeXCommandViewTextInfo)
		self._selection = selection
		self.inSection = inSection

	def update_menu(self):
		global latexMenu, latexShortcut
		latexMenu = [{
			**i, **{
				"type": "item",
			}
		} for i in latexAll]
		latexMenu = groupByField(latexMenu, 'category', lambda i: i, lambda i: i)

		latexShortcut = data2shortcutMap(latexAll)

	def getScript(self, gesture):
		if isinstance(gesture, KeyboardInputGesture):
			if len(gesture.modifierNames) == 0 and gesture.mainKeyName in ["f{}".format(i) for i in range(1, 13)] + ["{}".format(c) for c in "abcdefghijklmnopqrstuvwxyz"]:
				return self.script_set_shortcut
			elif len(gesture.modifierNames) == 0 and gesture.mainKeyName in ["delete", "backspace"]:
				return self.script_reset_shortcut

		return super().getScript(gesture)

	@script(
		gestures=["kb:f{}".format(i) for i in range(1, 13)] + ["kb:f{}".format(c) for c in "abcdefghijklmnopqrstuvwxyz"]
	)
	def script_set_shortcut(self, gesture):
		if self.data.pointer['type'] == 'menu':
			ui.message(_("menu can not set shortcut"))
			return

		id_ = self.data.pointer['id']
		slot = gesture.mainKeyName[1:] if len(gesture.mainKeyName) > 1 else gesture.mainKeyName

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
		gestures=["kb:delete", "kb:backspace"]
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
			if not self.inSection:
				delimiter = delimiter_dict[delimiter_setting["latex"]]
				offset = kwargs["offset"] - len(delimiter["end"])
				text = r"\({}\)".format(kwargs["text"])
				command(text=text, offset=offset)
			else:
				command(**kwargs)
		except:
			tones.beep(100, 100)
			return
		eventHandler.executeEvent("gainFocus", self.parent)

	def greekAlphabetCommand(self, id_):
		try:
			kwargs = greekAlphabetCommand[id_]
			if not self.inSection:
				delimiter = delimiter_dict[self.delimiter["latex"]]
				offset = kwargs["offset"] - len(delimiter["end"])
				text = r"\({}\)".format(kwargs["text"])
				command(text=text, offset=offset)
			else:
				command(**kwargs)
		except:
			tones.beep(100, 100)
			return
		eventHandler.executeEvent("gainFocus", self.parent)


class A8MLaTeXCommandViewTextInfo(MenuViewTextInfo):
	pass
