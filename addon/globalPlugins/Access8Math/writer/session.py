# coding=utf-8

import re

import api
import config
import textInfos

from ..delimiter import LaTeX as LaTeX_delimiter, AsciiMath as AsciiMath_delimiter, Nemeth as Nemeth_delimiter
from ..lib.mathProcess import textmath2laObjFactory
from .navigation import WriterNavigationMixin


class SectionManager(WriterNavigationMixin):
	def __init__(self):
		self.reset()

	def reset(self):
		self.section_index = -1
		self.points = None

	def __enter__(self):
		self.obj = api.getFocusObject()
		self.caret = self.obj.makeTextInfo(textInfos.POSITION_CARET)
		self.reset()
		points = textmath2laObjFactory(
			delimiter={
				"latex": config.conf["Access8Math"]["settings"]["LaTeX_delimiter"],
				"asciimath": "graveaccent",
				"nemeth": config.conf["Access8Math"]["settings"]["Nemeth_delimiter"],
			}
		)(self.obj.makeTextInfo(textInfos.POSITION_ALL).text)
		self.points = list(filter(lambda point: point['start'] < point['end'], points))
		temp = []
		for point in self.points:
			del point['index']
			temp.append(point)
		self.points = temp
		for index, point in enumerate(self.points):
			if self.caret._startOffset >= point['start'] and self.caret._startOffset < point['end']:
				self.section_index = index

		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		pass

	@property
	def pointer(self):
		try:
			pointer = self.points[self.section_index]
		except BaseException:
			pointer = None

		return pointer

	@property
	def delimiter(self):
		if self.pointer['type'] == 'latex':
			result = LaTeX_delimiter[config.conf["Access8Math"]["settings"]["LaTeX_delimiter"]]
		elif self.pointer['type'] == 'asciimath':
			result = AsciiMath_delimiter["graveaccent"]
		elif self.pointer['type'] == 'nemeth':
			result = Nemeth_delimiter[config.conf["Access8Math"]["settings"]["Nemeth_delimiter"]]
		else:
			result = {
				"start": "",
				"end": "",
				"type": self.pointer['type'],
			}
		return result

	@property
	def inSection(self):
		if self.pointer is None:
			return True

		delimiter_start_length = len(self.delimiter["start"])
		delimiter_end_length = len(self.delimiter["end"])

		if self.caret._startOffset >= self.pointer['start'] + delimiter_start_length and self.caret._endOffset <= self.pointer['end'] - delimiter_end_length:
			return True
		else:
			return False

	@property
	def inMath(self):
		if self.pointer is None:
			return False

		if self.inSection and (self.pointer['type'] == 'latex' or self.pointer['type'] == 'asciimath' or self.pointer['type'] == 'nemeth' or self.pointer['type'] == 'mathml'):
			return True
		else:
			return False

	@property
	def inText(self):
		if self.pointer is None:
			return True

		if self.inSection and self.pointer['type'] == 'text':
			return True
		else:
			return False

	@property
	def inLaTeX(self):
		if self.pointer is None:
			return False

		if self.inSection and self.pointer['type'] == 'latex':
			return True
		else:
			return False

	@property
	def inAsciiMath(self):
		if self.pointer is None:
			return False

		if self.inSection and self.pointer['type'] == 'asciimath':
			return True
		else:
			return False

	@property
	def inNemeth(self):
		if self.pointer is None:
			return False

		if self.inSection and self.pointer['type'] == 'nemeth':
			return True
		else:
			return False

	@property
	def inMathML(self):
		if self.pointer is None:
			return False

		if self.inSection and self.pointer['type'] == 'mathml':
			return True
		else:
			return False

	@property
	def command(self):
		command = {
			"all": None,
			"front": None,
			"back": None,
		}
		if not self.inLaTeX:
			return command

		delimiter_start_length = len(self.delimiter["start"])
		data = self.pointer["data"]
		start = self.pointer['start'] + delimiter_start_length
		current_local = self.caret._startOffset - start
		front_str = data[:current_local]
		back_str = data[current_local:]

		front_result = re.match(r"[A-Za-z]*\\", front_str[::-1])
		if front_result:
			back_result = re.match(r"[A-Za-z]*", back_str)
			front_command = front_result.group(0)[::-1]
			back_command = back_result.group(0)
			command = {
				"all": f"{front_command}{back_command}",
				"front": front_command,
				"back": back_command,
			}

		return command

	def commandSelection(self):
		command = self.command
		if command["all"]:
			current = self.caret._startOffset
			self.caret._startOffset = current - len(command["front"])
			self.caret._endOffset = current + len(command["back"])
			self.caret.updateSelection()
