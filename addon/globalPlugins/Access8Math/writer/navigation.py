# coding=utf-8


class WriterNavigationMixin:
	def move(self, step=0, type_="any", all_index=None):
		MATH_TYPE = ["latex", "asciimath", "nemeth", "mathml"]
		if all_index is not None:
			pointer = self.points[all_index]
		else:
			if step >= 0:
				filte_points = self.points[self.section_index:]
				if self.pointer["type"] != type_ and type_ in MATH_TYPE + ["text"]:
					step -= 1
				if self.pointer["type"] not in MATH_TYPE and type_ == "interactivable":
					step -= 1
			elif step < 0:
				filte_points = self.points[:self.section_index]
			if type_ in MATH_TYPE + ["text"]:
				filte_points = list(filter(lambda i: i['type'] == type_, filte_points))
			elif type_ == 'interactivable':
				filte_points = list(filter(lambda i: i['type'] in MATH_TYPE, filte_points))
			try:
				pointer = filte_points[step]
			except BaseException:
				pointer = None

		if not pointer:
			return None

		if type_ == 'notacrossline' and all_index is not None:
			if self.pointer['line'] != pointer['line']:
				return None

		self.section_index = self.points.index(pointer)
		delimiter_start_length = len(self.delimiter["start"])
		self.caret._startOffset = self.caret._endOffset = pointer['start'] + delimiter_start_length
		self.caret.updateCaret()
		self.caret._startOffset = pointer['start']
		self.caret._endOffset = pointer['end']

		return pointer

	def moveLine(self, step, type=None):
		line = -1
		if self.pointer and self.pointer["line"] + step >= 0 and self.pointer["line"] + step <= self.points[-1]["line"]:
			line = self.pointer["line"] + step
		pointers = []
		for all_index, point in enumerate(self.points):
			if point['line'] == line:
				self.section_index = all_index
				pointers.append(point)

		if len(pointers) > 0:
			if type:
				if type == "home":
					pointers = [pointers[0]]
				elif type == "end":
					pointers = [pointers[-1]]
				self.caret._startOffset = self.caret._endOffset = pointers[0]['start']
				self.caret.updateCaret()
				self.caret._startOffset = pointers[0]['start']
				self.caret._endOffset = pointers[0]['end']
			else:
				self.caret._startOffset = self.caret._endOffset = pointers[0]['start']
				self.caret.updateCaret()
				self.caret._startOffset = pointers[0]['start']
				self.caret._endOffset = pointers[-1]['end']

		return pointers

	def start(self):
		delimiter_start_length = len(self.delimiter["start"])
		if self.pointer:
			self.caret._startOffset = self.caret._endOffset = self.pointer['start'] + delimiter_start_length
			self.caret.updateCaret()
			return self.pointer
		return None

	def end(self):
		delimiter_end_length = len(self.delimiter["end"])
		if self.pointer:
			self.caret._startOffset = self.caret._endOffset = self.pointer['end'] - delimiter_end_length - 1
			self.caret.updateCaret()
			return self.pointer
		return None

	def startMargin(self):
		if self.pointer:
			self.caret._startOffset = self.caret._endOffset = self.pointer['start']
			self.caret.updateCaret()
			return self.pointer
		return None

	def endMargin(self):
		if self.pointer:
			self.caret._startOffset = self.caret._endOffset = self.pointer['end']
			self.caret.updateCaret()
			return self.pointer
		return None
