# coding=utf-8

import api
import config
from keyboardHandler import KeyboardInputGesture
import tones
import ui


class WriterRoutingMixin:
	def script_writeNav(self, gesture):
		if gesture.mainKeyName in ["space", "enter", "numpadEnter"]:
			self.script_interact(gesture)
		elif gesture.mainKeyName in ["downArrow", "upArrow", "home", "end", "pageUp", "pageDown"]:
			self.script_navigateLine(gesture)
		elif gesture.mainKeyName == "c" and "control" in gesture.modifierNames:
			self.script_navigateCopy(gesture)
		elif gesture.mainKeyName == "v" and "control" in gesture.modifierNames:
			self.script_navigatePaste(gesture)
		elif gesture.mainKeyName == "x" and "control" in gesture.modifierNames:
			self.script_navigateCut(gesture)
		elif gesture.mainKeyName == "t" and "control" in gesture.modifierNames:
			self.script_translate(gesture)
		elif gesture.mainKeyName in ["delete", "backspace"]:
			self.script_navigateDelete(gesture)
		else:
			self.script_navigate(gesture)

	def script_navigate(self, gesture):
		with self.section_manager as manager:
			selected = False
			if gesture.mainKeyName == "downArrow":
				result = manager.move(type_='any', step=0)
				if "shift" in gesture.modifierNames:
					selected = True
			elif gesture.mainKeyName == "leftArrow":
				if "alt" in gesture.modifierNames or config.conf["Access8Math"]["settings"]["writeNavAcrossLine"]:
					result = manager.move(type_='any', step=-1)
				else:
					result = manager.move(type_='notacrossline', step=-1)
				if "shift" in gesture.modifierNames:
					selected = True
			elif gesture.mainKeyName == "rightArrow":
				if "alt" in gesture.modifierNames or config.conf["Access8Math"]["settings"]["writeNavAcrossLine"]:
					result = manager.move(type_='any', step=1)
				else:
					result = manager.move(type_='notacrossline', step=1)
				if "shift" in gesture.modifierNames:
					selected = True
			elif gesture.mainKeyName == "tab":
				if "shift" in gesture.modifierNames:
					result = manager.move(type_='interactivable', step=-1)
				else:
					result = manager.move(type_='interactivable', step=1)
			elif gesture.mainKeyName == "t":
				if "shift" in gesture.modifierNames:
					result = manager.move(type_='text', step=-1)
				else:
					result = manager.move(type_='text', step=1)
			elif gesture.mainKeyName == "l":
				if "shift" in gesture.modifierNames:
					result = manager.move(type_='latex', step=-1)
				else:
					result = manager.move(type_='latex', step=1)
			elif gesture.mainKeyName == "a":
				if "shift" in gesture.modifierNames:
					result = manager.move(type_='asciimath', step=-1)
				else:
					result = manager.move(type_='asciimath', step=1)
			elif gesture.mainKeyName == "n":
				if "shift" in gesture.modifierNames:
					result = manager.move(type_='nemeth', step=-1)
				else:
					result = manager.move(type_='nemeth', step=1)
			elif gesture.mainKeyName == "m":
				if "shift" in gesture.modifierNames:
					result = manager.move(type_='mathml', step=-1)
				else:
					result = manager.move(type_='mathml', step=1)
			elif gesture.mainKeyName == "home":
				result = manager.start()
			elif gesture.mainKeyName == "end":
				result = manager.end()
			else:
				result = None

			if not result:
				result = manager.move(type_='any', step=0)
				tones.beep(100, 50)

			mode = "raw" if "alt" in gesture.modifierNames else "view"
			if selected:
				manager.caret.updateSelection()
			else:
				self.displayBlocks([result], mode)

	def script_navigateLine(self, gesture):
		with self.section_manager as manager:
			selected = False
			if gesture.mainKeyName == "upArrow":
				results = manager.moveLine(step=-1)
				if "shift" in gesture.modifierNames:
					selected = True
			elif gesture.mainKeyName == "downArrow":
				results = manager.moveLine(step=1)
				if "shift" in gesture.modifierNames:
					selected = True
			elif gesture.mainKeyName == "home":
				results = manager.moveLine(step=0, type=gesture.mainKeyName)
				if "shift" in gesture.modifierNames:
					selected = True
			elif gesture.mainKeyName == "end":
				results = manager.moveLine(step=0, type=gesture.mainKeyName)
				if "shift" in gesture.modifierNames:
					selected = True
			elif gesture.mainKeyName == "pageUp":
				results = manager.moveLine(step=-10)
				if "shift" in gesture.modifierNames:
					selected = True
			elif gesture.mainKeyName == "pageDown":
				results = manager.moveLine(step=10)
				if "shift" in gesture.modifierNames:
					selected = True
			else:
				results = []
				if "shift" in gesture.modifierNames:
					selected = True

			if len(results) == 0:
				results = manager.moveLine(step=0)
				tones.beep(100, 50)

			mode = "view"
			if selected:
				manager.caret.updateSelection()
			else:
				self.displayBlocks(results, mode)

	def script_navigateCopy(self, gesture):
		with self.section_manager as manager:
			result = manager.move(type_='any', step=0)
			api.copyToClip(result["raw"])
			ui.message(_("{data} copied to clipboard").format(data=result["raw"]))

	def script_navigatePaste(self, gesture):
		with self.section_manager as manager:
			manager.endMargin()
			KeyboardInputGesture.fromName("control+v").send()
			ui.message(_("{data} inserted to document").format(data=api.getClipData()))

	def script_navigateCut(self, gesture):
		with self.section_manager as manager:
			result = manager.move(type_='any', step=0)
			manager.caret.updateSelection()
			KeyboardInputGesture.fromName("control+x").send()
			ui.message(_("{data} cut from document").format(data=result["raw"]))

	def script_navigateDelete(self, gesture):
		with self.section_manager as manager:
			result = manager.move(type_='any', step=0)
			manager.caret.updateSelection()
			KeyboardInputGesture.fromName("delete").send()
			ui.message(_("{data} deleted from document").format(data=result["raw"]))
