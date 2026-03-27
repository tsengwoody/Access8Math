# coding=utf-8

import os
import shutil

import addonHandler
import api
import braille
import mathPres
import speech
import textInfos
import ui

from ..command.review import A8MHTMLCommandView
from ..lib.braille import display_braille
from ..lib.mathProcess import latex2mathml, asciimath2mathml, nemeth2latex
from ..lib.viewHTML import Access8MathDocument

addonHandler.initTranslation()

PATH = os.path.dirname(os.path.dirname(__file__))


class WriterActionsMixin:
	def script_view_math(self, gesture):
		document = self.makeTextInfo(textInfos.POSITION_ALL)

		obj = api.getForegroundObject()
		title = obj.name
		if not isinstance(title, str) or not title or title.isspace():
			title = obj.appModule.appName if obj.appModule else None
			if not isinstance(title, str) or not title or title.isspace():
				title = "index.txt"

		name = title.split("-")[0].strip('* ')
		ext = 'txt'

		data_folder = os.path.join(PATH, 'web', 'workspace', 'default')
		entry_file = f'{name}.{ext}'

		try:
			shutil.rmtree(data_folder)
		except BaseException:
			pass
		if not os.path.exists(data_folder):
			os.makedirs(data_folder)
		with open(os.path.join(data_folder, entry_file), "w", encoding="utf8", newline="") as f:
			f.write(document.text)

		ad = Access8MathDocument(os.path.join(data_folder, entry_file))
		ad.raw2review()
		A8MHTMLCommandView(
			ad=ad
		).setFocus()

	def script_interact(self, gesture):
		with self.section_manager as manager:
			if manager.inMath:
				if manager.pointer['type'] == 'latex':
					mathMl = latex2mathml(manager.pointer['data'])
				elif manager.pointer['type'] == 'asciimath':
					mathMl = asciimath2mathml(manager.pointer['data'])
				elif manager.pointer['type'] == 'nemeth':
					mathMl = latex2mathml(nemeth2latex(manager.pointer['data']))
				elif manager.pointer['type'] == 'mathml':
					mathMl = manager.pointer['data']
				mathMl = mathMl.replace("<<", "&lt;<").replace(">>", ">&gt;")
				mathPres.interactionProvider.interactWithMathMl(mathMl)
			else:
				ui.message(_("This block cannot be interacted"))

	def displayBlocks(self, results, mode):
		text = []
		brailleRegion = []
		for result in results:
			if result['data'] == "":
				continue
			if mode == "view" and result['type'] == "latex":
				try:
					mathMl = latex2mathml(result['data'])
					mathMl = mathMl.replace("<<", "&lt;<").replace(">>", ">&gt;")
					text += mathPres.speechProvider.getSpeechForMathMl(mathMl)
					brailleRegion += ["⠀", "".join(mathPres.speechProvider.getBrailleForMathMl(mathMl)), "⠀"]
				except BaseException:
					text += result['data']
					brailleRegion += [result['data']]
			elif mode == "view" and result['type'] == "asciimath":
				try:
					mathMl = asciimath2mathml(result['data'])
					mathMl = mathMl.replace("<<", "&lt;<").replace(">>", ">&gt;")
					text += mathPres.speechProvider.getSpeechForMathMl(mathMl)
					brailleRegion += ["⠀", "".join(mathPres.speechProvider.getBrailleForMathMl(mathMl)), "⠀"]
				except BaseException:
					text += result['data']
					brailleRegion += [result['data']]
			elif mode == "view" and result['type'] == "nemeth":
				try:
					mathMl = latex2mathml(nemeth2latex(result['data']))
					mathMl = mathMl.replace("<<", "&lt;<").replace(">>", ">&gt;")
					text += mathPres.speechProvider.getSpeechForMathMl(mathMl)
					brailleRegion += ["⠀", "".join(mathPres.speechProvider.getBrailleForMathMl(mathMl)), "⠀"]
				except BaseException:
					text += result['data']
					brailleRegion += [result['data']]
			elif mode == "view" and result['type'] == "mathml":
				try:
					mathMl = result['data']
					text += mathPres.speechProvider.getSpeechForMathMl(mathMl)
					brailleRegion += ["⠀", "".join(mathPres.speechProvider.getBrailleForMathMl(mathMl)), "⠀"]
				except BaseException:
					text += result['data']
					brailleRegion += [result['data']]
			else:
				text += [result['data']]
				brailleRegion += [result['data']]
		brailleRegion = [braille.TextRegion("".join(brailleRegion))]

		try:
			speech.speak(text)
			display_braille(brailleRegion)
		except BaseException:
			pass
