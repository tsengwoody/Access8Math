from xml.etree.ElementTree import ParseError

import addonHandler
import api
import config
from logHandler import log
import mathPres
import speech

from ..reader import MathContent
from ..output import translate_Braille, translate_SpeechCommand_CapNotification

addonHandler.initTranslation()


class Access8MathProvider(mathPres.MathPresentationProvider):
	def getSpeechForMathMl(self, mathMl):
		speechSequence = []

		try:
			mathcontent = MathContent(config.conf["Access8Math"]["settings"]["language"], mathMl)
			speechSequence = translate_SpeechCommand_CapNotification(mathcontent.pointer.serialized())
		except ParseError as error:
			speechSequence = [_("Illegal MathML")]
			log.error(f"ParseError in getSpeechForMathMl: {error}\nCaused by MathML:\n{mathMl}")
		except BaseException as error:
			speechSequence = [_("Error processing MathML")]
			log.error(f"Error in getSpeechForMathMl:\n{error}\nCaused by MathML:\n{mathMl}")

		return speechSequence

	def getBrailleForMathMl(self, mathMl):
		cells = ""

		try:
			mathcontent = MathContent(config.conf["Access8Math"]["settings"]["language"], mathMl)
			cells = translate_Braille(mathcontent.root.brailleserialized())
		except ParseError as error:
			cells = chr(0x2800)
			speech.speak([_("Illegal MathML")])
			log.error(f"ParseError in getBrailleForMathMl: {error}\nCaused by MathML:\n{mathMl}")
		except BaseException as error:
			cells = chr(0x2800)
			speech.speak([_("Error processing MathML")])
			log.error(f"Error in getBrailleForMathMl:\n{error}\nCaused by MathML:\n{mathMl}")

		def inrange(cell):
			return 0x2800 <= ord(cell) < 0x2800 + 256

		cells = [cell if inrange(cell) else chr(0x2800) for cell in cells]
		return "".join(cells)

	def interactWithMathMl(self, mathMl):
		try:
			from ..interaction import A8MInteraction
			mathcontent = MathContent(config.conf["Access8Math"]["settings"]["language"], mathMl)
			vw = A8MInteraction(parent=api.getFocusObject())
			vw.set(data=mathcontent, name="")
			vw.setFocus()
		except ParseError as error:
			speech.speak([_("Illegal MathML")])
			log.error(f"ParseError in interactWithMathMl: {error}\nCaused by MathML:\n{mathMl}")
		except BaseException as error:
			speech.speak([_("Error processing MathML")])
			log.error(f"Error in interactWithMathMl:\n{error}\nCaused by MathML:\n{mathMl}")
