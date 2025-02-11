from collections.abc import Iterable
import re
import os
from xml.sax.saxutils import escape

import brailleTables
import config
from logHandler import log
import louisHelper
from speechXml import SsmlParser
from speech.commands import BreakCommand, PitchCommand
from speech.speech import _getSpellingCharAddCapNotification
from synthDriverHandler import getSynth

BRAILLE_UNICODE_PATTERNS_START = 0x2800
BREAK_PATTERN = re.compile(r'^<break time="(?P<time>[\d]*)ms" />$')


def clean(serializes: list):
	result = [item for item in serializes if item != ""]
	if result:
		if BREAK_PATTERN.match(result[0]):
			result.pop(0)
		if BREAK_PATTERN.match(result[-1]):
			result.pop()
	result = [escape(item) if isinstance(item, str) else item for item in result]
	return result


def flatten(lines):
	"""
	convert tree to linear using generator
	@param lines:
	@type list
	@rtype
	"""
	for line in lines:
		if isinstance(line, Iterable) and not isinstance(line, str):
			for sub in flatten(line):
				yield sub
		else:
			yield line


def interleave_lists(a1, a2):
	output = []
	min_length = min(len(a1), len(a2))

	# Interleave elements from both lists
	for i in range(min_length):
		output.append(a1[i])
		output.append(a2[i])

	# Append remaining elements from the longer list
	output.extend(a1[min_length:])
	output.extend(a2[min_length:])

	return output


class A8MSsmlParser(SsmlParser):
	def _elementHandler(self, tagName: str, attrs: dict | None = None):
		processedTagName = "".join(tagName.title().split("-"))
		funcName = f"parse{processedTagName}"
		if (func := getattr(self, funcName, None)) is None:
			log.debugWarning(f"Unsupported tag: {tagName}")
			return
		for command in func(attrs):
			# If the last command in the sequence is of the same type, we can remove it.
			if self._speechSequence and type(self._speechSequence[-1]) is type(command):
				self._speechSequence.pop()
			self._speechSequence.append(command)


def translate_SpeechCommand(serializes):
	"""
	convert Access8Math serialize object to SpeechCommand
	@param lines: source serializes
	@type list
	@rtype SpeechCommand
	"""
	item = clean(flatten(serializes))
	item = interleave_lists(item, ['<break time="{ms}ms" />'.format(ms=10 * config.conf["Access8Math"]["settings"]["item_interval_time"])] * (len(item) - 1))
	ssml = "<speak>" + "".join(item) + "</speak>"
	parser = A8MSsmlParser()
	print(ssml)
	speechSequence = parser.convertFromXml(ssml)
	return speechSequence


def translate_SpeechCommand_CapNotification(serializes):
	command = []
	for item in translate_SpeechCommand(serializes):
		if isinstance(item, str):
			seq = getCharAddCapNotification(item)
			command.extend(list(seq))
		else:
			command.append(item)
	return command


def translate_Unicode(serializes):
	"""
	convert Access8Math serialize object to SpeechCommand
	@param lines: source serializes
	@type list
	@rtype SpeechCommand
	"""
	pattern = re.compile(r'<break time="(?P<time>[\d]*)ms" />')
	result = ""

	for c in serializes:
		result += "\n"
		for item in flatten(c):
			ssml = "<speak>" + "".join(item) + "</speak>"
			parser = A8MSsmlParser()
			sequence = parser.convertFromXml(ssml)
			sequence = [command for command in sequence if type(command) is not BreakCommand]
			string = " ".join(sequence).strip()
			result = result + " " + string

	# replace mutiple blank to single blank
	pattern = re.compile(r'[ ]+')
	sequence = pattern.sub(lambda m: ' ', result)

	# replace blank line to none
	pattern = re.compile(r'\n\s*\n')
	sequence = pattern.sub(lambda m: '\n', sequence)

	# strip blank at start and end line
	temp = ''
	for i in sequence.split('\n'):
		temp = temp + i.strip() + '\n'
	sequence = temp
	return sequence.strip()

	speechSequence = []
	for s in serializes:
		for item in flatten(s):
			ssml = "<speak>" + "".join(item) + "</speak>"
			parser = A8MSsmlParser()
			sequence = parser.convertFromXml(ssml)
			sequence = [command for command in sequence if type(command) is not BreakCommand]
			string = " ".join(sequence).strip()
			if string != "":
				speechSequence.append(string)

		speechSequence = "\n".join(speechSequence)
	return speechSequence.strip()


def translate_Braille(serializes):
	"""
	convert Access8Math serialize object to braille
	@param lines: source serializes
	@type list
	@rtype str
	"""
	temp = ''
	for string in flatten(serializes):
		brailleCells, brailleToRawPos, rawToBraillePos, brailleCursorPos = louisHelper.translate([os.path.join(brailleTables.TABLES_DIR, config.conf["braille"]["translationTable"]), "braille-patterns.cti"], string, mode=4)
		temp += "".join([chr(BRAILLE_UNICODE_PATTERNS_START + cell) for cell in brailleCells])
	return "".join(temp)


def getCharAddCapNotification(text: str):
	if len(text) != 1 or not text.isupper():
		return [text]

	synth = getSynth()
	synthConfig = config.conf["speech"][synth.name]

	if PitchCommand in synth.supportedCommands:
		capPitchChange = synthConfig["capPitchChange"]
	else:
		capPitchChange = 0

	seq = list(_getSpellingCharAddCapNotification(
		text,
		sayCapForCapitals=synthConfig["sayCapForCapitals"],
		capPitchChange=capPitchChange,
		beepForCapitals=synthConfig["beepForCapitals"],
	))
	return seq
