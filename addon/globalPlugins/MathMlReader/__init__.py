# coding: utf-8
import os
import sys
path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path)
Base_Dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, Base_Dir)
import cgi
import HTMLParser
import xml
from xml.etree import ElementTree as ET

import addonHandler
addonHandler.initTranslation()
import api
import config
import globalPlugins
import globalPluginHandler
import globalVars
from keyboardHandler import KeyboardInputGesture
from logHandler import log
import mathPres
from mathPres.mathPlayer import MathPlayer
import speech
import textInfos
import textInfos.offsets
import tones
import ui

from A8M_PM import *

#globalVars.appArgs.configPath

def translate_SpeechCommand(serializes):
	pattern = re.compile(r'[@](?P<time>[\d]*)[@]')
	speechSequence = []
	for r in serializes:
		time_search = pattern.search(r)
		try:
			time = time_search.group('time')
			command = speech.BreakCommand(time=int(time)+90)
			speechSequence.append(command)
		except:
			speechSequence.append(r)

	return speechSequence

def translate_Unicode(serializes):
	pattern = re.compile(r'[@](?P<time>[\d]*)[@]')
	sequence = ''
	for r in serializes:
		time_search = pattern.search(r)
		try:
			time = time_search.group('time')
		except:
			sequence = sequence +unicode(r)

	return sequence

class MathMlTextInfo(textInfos.offsets.OffsetsTextInfo):

	def __init__(self,obj,position):
		super(MathMlTextInfo,self).__init__(obj,position)
		self.obj = obj

	def _getStoryLength(self):
		serializes = self.obj.serialized()
		return len(translate_Unicode(serializes))

	def _getStoryText(self):
		"""Retrieve the entire text of the object.
		@return: The entire text of the object.
		@rtype: unicode
		"""
		serializes = self.obj.serialized()
		return translate_Unicode(serializes)

	def _getTextRange(self,start,end):
		"""Retrieve the text in a given offset range.
		@param start: The start offset.
		@type start: int
		@param end: The end offset (exclusive).
		@type end: int
		@return: The text contained in the requested range.
		@rtype: unicode
		"""
		text=self._getStoryText()
		return text[start:end] if text else u""

class MathMlReader(mathPres.MathPresentationProvider):

	def getSpeechForMathMl(self, mathMl):
		gtlt_pattern = re.compile(ur"([\>])(.*?)([\<])")
		mathMl = gtlt_pattern.sub(lambda m: m.group(1) +cgi.escape(HTMLParser.HTMLParser().unescape(m.group(2))) +m.group(3), mathMl)
		quote_pattern = re.compile(ur"([\"\'])(.*?)\1")
		mathMl = quote_pattern.sub(lambda m: m.group(1) +cgi.escape(m.group(2)) +m.group(1), mathMl)
		parser = ET.XMLParser()
		try:
			tree = ET.fromstring(mathMl.encode('utf-8'), parser=parser)
		except BaseException as e:
			globalVars.raw_data = mathMl
			raise SystemError(e)
		node = create_node(tree)
		globalVars.nodes = node
		return translate_SpeechCommand(node.serialized())

	def interactWithMathMl(self, mathMl):
		MathMlReaderInteraction(provider=self, mathMl=mathMl).setFocus()

class MathMlReaderInteraction(mathPres.MathInteractionNVDAObject):

	def __init__(self, provider=None, mathMl=None):
		super(MathMlReaderInteraction, self).__init__(provider=provider, mathMl=mathMl)
		gtlt_pattern = re.compile(ur"([\>])(.*?)([\<])")
		mathMl = gtlt_pattern.sub(lambda m: m.group(1) +cgi.escape(HTMLParser.HTMLParser().unescape(m.group(2))) +m.group(3), mathMl)
		quote_pattern = re.compile(ur"([\"\'])(.*?)\1")
		mathMl = quote_pattern.sub(lambda m: m.group(1) +cgi.escape(m.group(2)) +m.group(1), mathMl)
		parser = ET.XMLParser()
		'''parser._parser.UseForeignDTD(True)
		parser.entity['gt'] = u'>'
		parser.entity['lt'] = u'<'''
		try:
			tree = ET.fromstring(mathMl.encode('utf-8'), parser=parser)
		except BaseException as e:
			globalVars.raw_data = mathMl
			raise SystemError(e)
		self.mathml_tree = self.pointer = create_node(tree)
		self.raw_data = mathMl
		api.setReviewPosition(MathMlTextInfo(self.pointer, textInfos.POSITION_FIRST), False)

	def reportFocus(self):
		super(MathMlReaderInteraction, self).reportFocus()
		speech.speak(translate_SpeechCommand(self.mathml_tree.serialized()))
		api.setReviewPosition(MathMlTextInfo(self.pointer, textInfos.POSITION_FIRST), False)

	def getScript(self, gesture):
		# Pass most keys to MathPlayer. Pretty ugly.

		if isinstance(gesture, KeyboardInputGesture) and "NVDA" not in gesture.modifierNames and (
			gesture.mainKeyName in {
				"leftArrow", "rightArrow", "upArrow", "downArrow",
				"home", "end",
				"space", "backspace", "enter",
			}
			or len(gesture.mainKeyName) == 1
		):
			return self.script_navigate
		return super(MathMlReaderInteraction, self).getScript(gesture)

	def script_navigate(self, gesture):
		r = None
		if gesture.mainKeyName == "downArrow":
			r = self.pointer.down()
		elif gesture.mainKeyName == "upArrow":
			r = self.pointer.up()
		elif gesture.mainKeyName == "leftArrow":
			r = self.pointer.previous_sibling
		elif gesture.mainKeyName == "rightArrow":
			r = self.pointer.next_sibling
		elif gesture.mainKeyName == "space":
			globalVars.math_raw_data = self.raw_data
			globalVars.math_root = self.mathml_tree
			globalVars.math_node = self.pointer
			globalVars.math_ser = translate_Unicode(self.pointer.serialized())
			speech.speak([_("copy"),])

		if r is not None:
			self.pointer = r
			api.setReviewPosition(MathMlTextInfo(self.pointer, textInfos.POSITION_FIRST), False)
#			if gesture.mainKeyName == "leftArrow" or gesture.mainKeyName == "rightArrow":
			speech.speak(self.pointer.des)
			speech.speak(translate_SpeechCommand(self.pointer.serialized()))
		else:
			speech.speak([_("not move")])

provider_list = [
	u"MathMlReader",
	u"MathPlayer"
]

try:
	provider = config.conf["Access8Math"]["provider"]
	if not provider in provider_list:
		raise ValueError()
except ValueError:
	config.conf["Access8Math"]["provider"] = provider = "MathMlReader"
except KeyError:
	config.conf["Access8Math"] = {}
	config.conf["Access8Math"]["version"] = "0.1"
	config.conf["Access8Math"]["provider"] = provider = "MathMlReader"

try:
	exec(
		'reader = {}()'.format(provider)
	)
	config.conf["Access8Math"]["provider"] = reader.__class__.__name__
except:
	log.warning("{} not available".format(provider_list[index]))

mathPres.registerProvider(reader, speech=True, braille=False, interaction=True)

mathPres.registerProvider(reader, speech=True, braille=False, interaction=True)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		xml_NVDA = sys.modules['xml']
		sys.modules['xml'] = globalPlugins.MathMlReader.xml

	def script_change_provider(self, gesture):
		index = (provider_list.index(config.conf["Access8Math"]["provider"]) +1)% len(provider_list)
		try:
			exec(
				'reader = {}()'.format(provider_list[index])
			)
			config.conf["Access8Math"]["provider"] = reader.__class__.__name__
		except:
			log.warning("{} not available".format(provider_list[index]))
		mathPres.registerProvider(reader, speech=True, braille=False, interaction=True)
		ui.message(_("mathml provider change to {0}".format(config.conf["Access8Math"]["provider"])))

	__gestures={
		"kb:control+alt+m": "change_provider",
	}
