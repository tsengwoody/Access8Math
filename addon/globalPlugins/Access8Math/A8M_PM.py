# coding=utf-8
# Copyright (C) 2017-2021 Tseng Woody <tsengwoody.tw@gmail.com>

import xml
from xml.etree import ElementTree as ET

import collections
import html
import inspect
import io
import os
import re
import sys
import weakref

AUTO_GENERATE = 0
DIC_GENERATE = 1

def mathml2etree(mathml):
	"""
	Convert mathml to XML etree object
	@param mathml: source mathml
	@type mathml: str
	@rtype: XML etree
	"""

	gtlt_pattern = re.compile(r"([\>])(.*?)([\<])")
	mathml = gtlt_pattern.sub(
					lambda m: m.group(1) +html.escape(html.unescape(m.group(2))) +m.group(3),
					mathml
	)

	quote_pattern = re.compile(r"=([\"\'])(.*?)\1")
	mathml = quote_pattern.sub(lambda m: '=' +m.group(1) +html.escape(m.group(2)) +m.group(1), mathml)

	parser = ET.XMLParser()

	try:
		tree = ET.fromstring(mathml.encode('utf-8'), parser=parser)
	except BaseException as error:
		raise SystemError(error)
	return tree

def create_node(et):
	p_tag = re.compile(r"[\{].*[\}](?P<mp_type>.+)")
	r = p_tag.search(et.tag)
	try:
		mp_tag = r.group('mp_type')
	except:
		mp_tag = et.tag

	node_class = nodes[mp_tag.capitalize()] if mp_tag.capitalize() in nodes.keys() else object

	if issubclass(node_class, NonTerminalNode) or issubclass(node_class, BlockNode):
		child = []
		for c in et:
			node = create_node(c)
			child.append(node)
		node = node_class(child, et.attrib)
	elif issubclass(node_class, TerminalNode):
		node = node_class([], et.attrib, data=et.text)
	elif mp_tag == 'none':
		node = Nones()
	else:
		child = []
		for c in et:
			node = create_node(c)
			child.append(node)
		node = Mrow(child, et.attrib)
		# raise RuntimeError('unknown tag : {}'.format(mp_tag))

	return node


def clean_allnode(node):
	for child in node.child:
		clean_allnode(child)

	'''if len(node.child) > 1:
		clean_child = []
		clean_child.append(node.child[0])
		for index in range(1, len(node.child)):
			if isinstance(node, Mrow) and isinstance(node.child[index-1], Mn) and isinstance(node.child[index], Mn):
				clean_child[-1].data = clean_child[-1].data +node.child[index].data
			else:
				clean_child.append(node.child[index])
		node.child = clean_child'''

	if node.parent and isinstance(node, BlockNode):

		if len(node.child) == 1 or (isinstance(node.parent, AlterNode) and len(node.child) > 0):

			# remove node
			parent_new_child = node.parent.child[0:node.index_in_parent()] + node.child
			if node.index_in_parent() + 1 < len(node.parent.child):
				parent_new_child = parent_new_child + node.parent.child[node.index_in_parent() + 1:]
			node.parent.child = parent_new_child
			for child in node.child:
				child.parent = node.parent

		elif isinstance(node.parent, AlterNode) and len(node.child) == 0:
			index = node.index_in_parent()
			node.parent.child[index].child = []

	return node

def set_mathcontent_allnode(node, mathcontent):
	for child in node.child:
		set_mathcontent_allnode(child, mathcontent)
	node.mathcontent = mathcontent
	return node

def set_mathrule_allnode(node, mathrule):
	for child in node.child:
		set_mathrule_allnode(child, mathrule)
	node.set_mathrule(mathrule)
	return node


def set_braillemathrule_allnode(node, braillemathrule):
	for child in node.child:
		set_braillemathrule_allnode(child, braillemathrule)
	node.set_braillemathrule(braillemathrule)
	return node

def clear_type_allnode(node):
	for child in node.child:
		clear_type_allnode(child)
	node.type = None
	return node


def check_type_allnode(node):
	for child in node.child:
		check_type_allnode(child)
	node.check_type()
	return node


def check_in_allnode(node, check_node):
	if id(node) == id(check_node):
		return True

	for child in node.child:
		if check_in_allnode(child, check_node):
			return True

	return False


class MathContent(object):
	def __init__(self, language, mathMl):
		et = mathml2etree(mathMl)
		self.root = self.pointer = create_node(et)
		set_mathcontent_allnode(self.root, self)
		clean_allnode(self.root)
		clear_type_allnode(self.root)
		check_type_allnode(self.root)

		self.symbol = load_unicode_dic(language=language)
		mathrule = load_math_rule(language=language)
		self.set_mathrule(mathrule)

		self.braillesymbol = load_unicode_dic(language="braille")
		braillemathrule = load_math_rule(language="braille")
		self.set_braillemathrule(braillemathrule)

	def set_mathrule(self, mathrule):
		self.mathrule = mathrule
		set_mathrule_allnode(self.root, self.mathrule)
		clear_type_allnode(self.root)
		check_type_allnode(self.root)
		set_mathrule_allnode(self.root, self.mathrule)

	def set_braillemathrule(self, braillemathrule):
		self.braillemathrule = braillemathrule
		set_braillemathrule_allnode(self.root, self.braillemathrule)
		clear_type_allnode(self.root)
		check_type_allnode(self.root)
		set_braillemathrule_allnode(self.root, self.braillemathrule)

	def navigate(self, action):
		pointer = None
		if action == "downArrow":
			pointer = self.pointer.down()
		elif action == "upArrow":
			pointer = self.pointer.up()
		elif action == "leftArrow":
			pointer = self.pointer.previous_sibling
		elif action == "rightArrow":
			pointer = self.pointer.next_sibling
		elif action == "home":
			pointer = self.root

		if pointer is not None:
			self.pointer = pointer
			return True

		return False

	def insert(self, mathMl):
		et = mathml2etree(mathMl)
		node = create_node(et)
		if self.pointer.parent:
			self.pointer.parent.insert(self.pointer.index_in_parent(), node)
			self.pointer = node

		else:
			self.pointer.insert(len(self.pointer.child), node)
			self.pointer = node

		# node refresh
		clean_allnode(self.root)
		clear_type_allnode(self.root)
		set_mathrule_allnode(self.root, self.mathrule)
		check_type_allnode(self.root)
		self.pointer = self.root

		if check_in_allnode(self.root, node):
			del node

	def delete(self):
		if self.pointer.parent:
			parent = self.pointer.parent
			index = self.pointer.index_in_parent()
			self.pointer.parent.delete(self.pointer.index_in_parent())
			try:
				self.pointer = parent.child[index]
			except:
				self.pointer = parent

			# node refresh
			clean_allnode(self.root)
			clear_type_allnode(self.root)
			set_mathrule_allnode(self.root, self.mathrule)
			check_type_allnode(self.root)


class Node(object):
	def __init__(self, child=None, attrib=None, data=None):
		self._mathcontent = None
		self._parent = None

		self.child = list(child) if child else []
		for c in self.child:
			if isinstance(c, Node):
				c.parent = self

		self.attrib = attrib if attrib else {}
		self.data = str(data.strip()) if data else ''

		self.symbol = {}

		self.mathrule = {}
		self.rule = []
		self.role = []

		self.braillemathrule = {}
		self.braillerule = []
		self.braillerole = []

		self.type = None
		self.role_level = None

	def check_type(self):
		for nodetype in nodetypes_check:
			if nodetype.check(self) and nodetype.name in self.mathrule:
				if not self.type:
					self.type = nodetype()
				elif self.type and issubclass(nodetype, self.type.__class__):
					self.type = nodetype()

	def set_mathrule(self, mathrule):
		self.mathrule = mathrule
		self.set_role()
		self.set_rule()
		if self.type:
			self.type.set_mathrule(self.mathrule)

	def set_role(self):
		self.role = self.mathrule[self.name].role if self.name in self.mathrule else [self.symbol_translate('item')]
		d = len(self.child) - len(self.role)
		if d > 0:
			append = self.role[-1]
			self.role = self.role[:-1]
			for i in range(d + 1):
				self.role.append('{0}{1}'.format(append, i + 1))
			self.role_level = AUTO_GENERATE
		else:
			self.role_level = DIC_GENERATE

	def set_rule(self):
		if self.type and self.type.rule:
			rule = self.type.rule
		else:
			rule = self.mathrule[self.name].serialized_order
		if len(rule) >= 2 and isinstance(rule[1], tuple):
			result = []
			for i in range(len(self.child)):
				before_empty = (rule[1][0].isspace() or rule[1][0] == '')
				after_empty = (rule[1][1].isspace() or rule[1][1] == '')
				if not (before_empty and after_empty):
					result.append('{0}{1}{2}'.format(rule[1][0], i + 1, rule[1][1]))
				result.append(i)

			rule = rule[0:1] + result + rule[-1:]
		self.rule = rule

	def set_braillemathrule(self, braillemathrule):
		self.braillemathrule = braillemathrule
		self.set_braillerole()
		self.set_braillerule()
		if self.type:
			self.type.set_braillemathrule(self.braillemathrule)

	def set_braillerole(self):
		self.braillerole = self.braillemathrule[self.name].role if self.name in self.braillemathrule else [self.symbol_translate('item')]
		d = len(self.child) - len(self.braillerole)
		if d > 0:
			append = self.braillerole[-1]
			self.braillerole = self.braillerole[:-1]
			for i in range(d + 1):
				self.braillerole.append('{0}{1}'.format(append, i + 1))
			self.braillerole_level = AUTO_GENERATE
		else:
			self.braillerole_level = DIC_GENERATE

	def set_braillerule(self):
		if self.type and self.type.braillerule:
			braillerule = self.type.braillerule
		else:
			braillerule = self.braillemathrule[self.name].serialized_order

		if len(braillerule) >= 2 and isinstance(braillerule[1], tuple):
			result = []
			for i in range(len(self.child)):
				before_empty = (braillerule[1][0].isspace() or braillerule[1][0] == '')
				after_empty = (braillerule[1][1].isspace() or braillerule[1][1] == '')
				if not (before_empty and after_empty):
					result.append('{0}{1}{2}'.format(braillerule[1][0], i + 1, braillerule[1][1]))
				result.append(i)

			braillerule = braillerule[0:1] + result + braillerule[-1:]
		self.braillerule = braillerule

	def serialized(self):
		serialized = []
		if isinstance(self, TerminalNode):
			serialized.append(['@10@'])
		for r in self.rule:
			if isinstance(r, int):
				serialized.append(self.child[r].serialized())
			elif r == '*':
				for c in self.child:
					if c:
						serialized.append(c.serialized())
						serialized.append(['@10@'])
			elif isinstance(r, str):
				serialized.append([r])
			else:
				raise TypeError('rule element type error : expect int or str (get {0})'.format(type(r)))
		if isinstance(self, TerminalNode):
			serialized.append(['@10@'])
		return serialized

	def brailleserialized(self):
		serialized = []
		for r in self.braillerule:
			if isinstance(r, int):
				serialized.append(self.child[r].brailleserialized())
			elif r == '*':
				for c in self.child:
					if c:
						serialized.append(c.brailleserialized())
			elif isinstance(r, str):
				serialized.append([r])
			else:
				raise TypeError('rule element type error : expect int or str (get {0})'.format(type(r)))
		return serialized

	def symbol_translate(self, string):
		symbol_order = sorted(list(self.mathcontent.symbol.items()), key=lambda i: -len(i[0]))
		for key, value in symbol_order:
			string = string.replace(key, value)
		return string

	def braillesymbol_translate(self, string):
		symbol_order = sorted(list(self.mathcontent.braillesymbol.items()), key=lambda i: -len(i[0]))
		for key, value in symbol_order:
			string = string.replace(key, value)
		return string

	def get_mathml(self):
		mathml = ''
		for c in self.child:
			mathml = mathml + c.get_mathml()
		attrib = ''
		for k, v in self.attrib.items():
			attrib = attrib + ' {0}="{1}"'.format(k, v)

		if len(self.attrib) > 0:
			result = '<{0}{1}>{2}</{0}>'.format(self.tag, attrib, mathml)
		else:
			result = '<{0}>{1}</{0}>'.format(self.tag, mathml)

		return result

	@property
	def mathcontent(self):
		return None if self._mathcontent is None else self._mathcontent()

	@mathcontent.setter
	def mathcontent(self, mathcontent):
		# self._mathcontent = mathcontent
		self._mathcontent = weakref.ref(mathcontent)

	@property
	def des(self):
		return self.parent.role[self.index_in_parent()] if self.parent else self.symbol_translate('math')

	@property
	def name(self):
		return self.type.name if self.type else self.tag

	@property
	def tag(self):
		return self.__class__.__name__.lower()

	@property
	def parent(self):
		return None if self._parent is None else self._parent()

	@parent.setter
	def parent(self, node):
		self._parent = weakref.ref(node)

	def index_in_parent(self):
		try:
			return self.parent.child.index(self)
		except:
			return None

	@property
	def next_sibling(self):
		try:
			index = self.index_in_parent() + 1
			if index < 0:
				raise IndexError('index out of range')
		except:
			index = None

		try:
			return self.parent.child[index]
		except:
			return None

	@property
	def previous_sibling(self):
		try:
			index = self.index_in_parent() - 1
			if index < 0:
				raise IndexError('index out of range')
		except:
			index = None

		try:
			return self.parent.child[index]
		except:
			return None

	@property
	def next(self):
		current = self
		_next = current.next_sibling
		while not _next:
			current = current.parent
			if not current:
				return None
			_next = current.next_sibling
		return _next

	@property
	def previous(self):
		current = self
		previous = current.previous_sibling
		while not previous:
			current = current.parent
			if not current:
				return None
			previous = current.previous_sibling
		return previous

	def down(self):
		try:
			return self.child[0]
		except:
			return None

	def up(self):
		try:
			return self.parent
		except:
			return None


class NonTerminalNode(Node):
	def set_rule(self):
		try:
			super().set_rule()
		except:
			self.rule = range(len(self.child))

	def set_role(self):
		try:
			super().set_role()
		except:
			self.rule = range(len(self.child))

	def set_braillerule(self):
		try:
			super().set_braillerule()
		except:
			self.braillerule = range(len(self.child))

	def set_braillerole(self):
		try:
			super().set_braillerole()
		except:
			self.braillerule = range(len(self.child))


class TerminalNode(Node):
	def set_rule(self):
		try:
			super().set_rule()
		except BaseException as e:
			self.rule = [str(self.symbol_translate(self.data))]

	def set_braillerule(self):
		try:
			super().set_braillerule()
		except BaseException as e:
			self.braillerule = [str(self.braillesymbol_translate(self.data))]

	def get_mathml(self):
		mathml = ''
		mathml = mathml + self.data if self.data else mathml
		return '<{0}>{1}</{0}>'.format(self.tag, mathml)


class AlterNode(NonTerminalNode):
	def insert(self, index, node):
		if index > len(self.child):
			return None
		if index == len(self.child):
			self.child.insert(index + 1, node)
			node.parent = self
		elif isinstance(self.child[index], BlockNode) and len(self.child[index].child) == 0:
			self.child[index].child.insert(0, node)
			node.parent = self.child[index]
		else:
			self.child.insert(index + 1, node)
			node.parent = self
		return node

	def delete(self, index):
		if index >= len(self.child):
			return None
		node = self.child[index]
		del self.child[index]
		if len(self.child) <= 0:
			mrow_node = Mrow([], {})
			self.child.insert(0, mrow_node)
			mrow_node.parent = self
		return node


class FixNode(NonTerminalNode):
	def insert(self, index, node):
		if index >= len(self.child):
			return None
		if isinstance(self.child[index], BlockNode):
			self.child[index].child.append(node)
			node.parent = self.child[index]
		else:
			mrow_child = [self.child[index], node]
			mrow_node = Mrow(mrow_child, {})
			mrow_node.parent = self
			for child in mrow_node.child:
				child.parent = mrow_node
			self.child[index] = mrow_node

		return node

	def delete(self, index):
		if index >= len(self.child):
			return None
		node = self.child[index]
		self.child[index] = Mrow([], {})
		self.child[index].parent = self
		return node


class BlockNode(AlterNode):
	def set_rule(self):
		try:
			super().set_rule()
		except:
			self.rule = range(len(self.child))

	def set_braillerule(self):
		try:
			super().set_braillerule()
		except:
			self.braillerule = range(len(self.child))


class Mrow(BlockNode):
	pass


class Mfrac(FixNode):
	pass


class Msqrt(AlterNode):
	pass


class Mroot(FixNode):
	pass


class Mstyle(BlockNode):
	pass


class Merror(AlterNode):
	pass


class Mpadded(AlterNode):
	pass


class Mphantom(AlterNode):
	pass


class Mfenced(AlterNode):
	def set_rule(self):
		super().set_rule()
		rule = self.rule
		if not self.type:
			if 'open' in self.attrib:
				rule = [str(self.attrib['open'])] + rule
			if 'close' in self.attrib:
				rule = rule[0:-1] + [str(self.attrib['close'])] + rule[-1:]
			if ('open' not in self.attrib) and ('close' not in self.attrib):
				rule = ['('] + rule[0:-1] + [')'] + rule[-1:]

		self.rule = rule

	def set_braillerule(self):
		pass


class Menclose(AlterNode):
	pass


class Msub(FixNode):
	pass


class Msup(FixNode):
	pass


class Msubsup(FixNode):
	pass


class Munder(FixNode):
	pass


class Mover(FixNode):
	pass


class Munderover(FixNode):
	pass


class Mtable(AlterNode):
	def set_rule(self):
		super().set_rule()
		rule = self.rule

		row_count = len(self.child)
		column_count_list = [len(i.child) for i in self.child]
		column_count = max(column_count_list)
		table_head = [rule[0] + '{0}{1}{2}{3}{4}'.format(self.symbol_translate('has'), row_count, self.symbol_translate('row'), column_count, self.symbol_translate('column'))]
		cell = rule[1:-1]
		table_tail = rule[-1:]
		self.rule = table_head + cell + table_tail

	def set_braillerule(self):
		pass


class Mlabeledtr(AlterNode):
	pass


class Mtr(AlterNode):
	def set_rule(self):
		super().set_rule()
		rule = self.rule
		cell = rule[1:-1]
		self.rule = rule[:1] + cell + rule[-1:]

class Mlabeledtr(AlterNode):
	pass


class Mtd(AlterNode):
	pass


class Mstack(AlterNode):
	pass


class Mlongdiv(AlterNode):
	pass


class Msgroup(AlterNode):
	pass


class Msrow(AlterNode):
	pass


class Mscarries(AlterNode):
	pass


class Mscarry(AlterNode):
	pass


class Maction(AlterNode):
	pass


class Math(AlterNode):
	pass


class Mi(TerminalNode):
	pass


class Mn(TerminalNode):
	pass


class Mo(TerminalNode):
	pass


class Mtext(TerminalNode):
	pass


class Mspace(TerminalNode):
	def set_rule(self):
		self.rule = [str(self.symbol_translate(self.data)) if not self.data == '' else str(self.symbol_translate("empty"))]

class Mlabeledtr(AlterNode):
	pass


class Ms(TerminalNode):
	pass


class Mmultiscripts(AlterNode):
	'''def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		role = [self.symbol_translate('main')]

		index = range(1, self.mprescripts_index_in_child())
		for count in range(len(index)/2):
			temp = [
				'{0}{1}{2}'.format(self.symbol_translate('order'), count, self.symbol_translate('rightdownmark')),
				'{0}{1}{2}'.format(self.symbol_translate('order'), count, self.symbol_translate('rightupmark')),
			]
			role = role + temp

		role = role + [self.symbol_translate('mprescripts_index')]

		index = range(self.mprescripts_index_in_child() + 1, len(self.child))
		for count in range(len(index)/2):
			temp = [
				'{0}{1}{2}'.format(self.symbol_translate('order'), count, self.symbol_translate('leftdownmark')),
				'{0}{1}{2}'.format(self.symbol_translate('order'), count, self.symbol_translate('leftupmark')),
			]
			role = role + temp

		self.role = role'''

	def set_rule(self):
		super().set_rule()
		rule = self.rule

		index = range(1, self.mprescripts_index_in_child())
		index_odd = index[0::2]
		index_even = index[1::2]
		index_mix = zip(index_odd, index_even)
		for count, item in enumerate(index_mix):
			temp = [
				'{0}{1}{2}'.format(self.symbol_translate('order'), count, self.symbol_translate('rightdownmark')),
				item[0],
				'{0}{1}{2}'.format(self.symbol_translate('order'), count, self.symbol_translate('rightupmark')),
				item[1],
			]
			rule = rule[:1] + temp + rule[-1:]

		index = range(self.mprescripts_index_in_child() + 1, len(self.child))
		index_odd = index[0::2]
		index_even = index[1::2]
		index_mix = zip(index_odd, index_even)
		for count, item in enumerate(index_mix):
			temp = [
				'{0}{1}{2}'.format(self.symbol_translate('order'), count, self.symbol_translate('leftdownmark')),
				item[0],
				'{0}{1}{2}'.format(self.symbol_translate('order'), count, self.symbol_translate('leftupmark')),
				item[1],
			]
			rule = rule[:1] + temp + rule[-1:]

		rule.insert(1, 0)
		self.rule = rule

	def set_braillerule(self):
		pass

	def mprescripts_index_in_child(self):
		for c in self.child:
			if isinstance(c, Mprescripts):
				return self.child.index(c)
		return None


class Mprescripts(TerminalNode):
	pass


class Nones(Node):
	pass


class NodeType(object):
	tag = object
	child = ['object', '*']
	attrib = {}
	data = re.compile(r".*")
	name = 'nodetype'
	priority = 0

	def __init__(self):
		self.mathrule = {}
		self.rule = []
		self.role = []

	@classmethod
	def check(cls, obj):
		if not issubclass(obj.__class__, cls.tag):
			return False

		return True

	def set_mathrule(self, mathrule):
		self.mathrule = mathrule
		self.set_rule()

	def set_rule(self):
		try:
			self.rule = self.mathrule[self.name].serialized_order
		except:
			self.rule = None

	def set_braillemathrule(self, braillemathrule):
		self.braillemathrule = braillemathrule
		self.set_braillerule()

	def set_braillerule(self):
		try:
			self.braillerule = self.braillemathrule[self.name].serialized_order
		except:
			self.braillerule = None


class TerminalNodeType(NodeType):
	@classmethod
	def check(cls, obj):
		if not issubclass(obj.__class__, cls.tag):
			return False

		# check attrib
		for key, value in cls.attrib.items():
			if key not in obj.attrib:
				return False
			elif not value.search(obj.attrib[key]) is not None:
				return False

		# check data
		if not obj.data == '':
			try:
				if not cls.data.search(obj.data) is not None:
					return False
			except:
				return False
		return True


class NonTerminalNodeType(NodeType):
	@classmethod
	def check(cls, obj):
		if not issubclass(obj.__class__, cls.tag):
			return False

		# check attrib
		for key, value in cls.attrib.items():
			if key not in obj.attrib:
				return False
			elif not value.search(obj.attrib[key]) is not None:
				return False

		# check child
		if cls.child[-1] == '*' and len(cls.child) > 1:
			d = len(obj.child) - (len(cls.child) - 1)
			type_list = cls.child[:-1] + [cls.child[-2]] * d
		else:
			type_list = cls.child
		if not len(type_list) == len(obj.child):
			return False

		# change type
		type_list_str = [t if isinstance(t, str) else t.__name__ for t in type_list]
		type_list = [all_nodetypes_dict[t] for t in type_list_str]

		# check child type
		for mt, o in zip(type_list, obj.child):
			if not mt == object and not mt.check(o):
				return False

		return True


class SiblingNodeType(NodeType):
	previous_siblings = []
	next_siblings = []
	self_ = NodeType

	@classmethod
	def check(cls, obj):
		self_index = obj.index_in_parent()
		cls_previous_siblings = cls.previous_siblings
		cls_next_siblings = cls.next_siblings
		cpsl = len(cls_previous_siblings)
		cnsl = len(cls_next_siblings)
		if self_index is not None:
			start_index = self_index - cpsl
			if cpsl > 0 and cls_previous_siblings[0] is None:
				cls_previous_siblings = cls_previous_siblings[1:]
				if not start_index == -1:
					return False
			elif start_index < 0:
				return False

			end_index = self_index + cnsl
			if cnsl > 0 and cls_next_siblings[-1] is None:
				cls_next_siblings = cls_next_siblings[:-1]
				if not end_index == len(obj.parent.child):
					return False
			elif end_index > len(obj.parent.child):
				return False
		else:
			return False

		if not cls.self_.check(obj):
			return False

		# change type
		type_list = cls_previous_siblings
		type_list_str = [t if isinstance(t, str) else t.__name__ for t in type_list]
		type_list = [all_nodetypes_dict[t] for t in type_list_str]
		obj_previous_siblings = obj.parent.child[start_index:self_index]
		for mt, o in zip(type_list, obj_previous_siblings):
			if not mt == object and not mt.check(o):
				return False

		type_list = cls_next_siblings
		type_list_str = [t if isinstance(t, str) else t.__name__ for t in type_list]
		type_list = [all_nodetypes_dict[t] for t in type_list_str]
		obj_next_siblings = obj.parent.child[self_index + 1:end_index + 1]
		for mt, o in zip(type_list, obj_next_siblings):
			if not mt == object and not mt.check(o):
				return False

		return True


class CompoundNodeType(NodeType):
	compound = []

	@classmethod
	def check(cls, obj):
		for mt in cls.compound:
			if mt.check(obj):
				return True
		return False


class FractionType(NonTerminalNodeType):
	tag = Mfrac


class MiOperandType(TerminalNodeType):
	tag = Mi
	data = re.compile(r"^[\d\w]+$")


class MnOperandType(TerminalNodeType):
	tag = Mn
	data = re.compile(r"^[\d\w]+$")


class OperandType(CompoundNodeType):
	compound = [MiOperandType, MnOperandType, FractionType, ]


class OperatorType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^[u'\u2200'-u'\u22FF']$")


class FromToOperatorType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^[∑∫]$")


class LogOperatorType(TerminalNodeType):
	tag = Mi
	data = re.compile(r"^log$")


class MiType(TerminalNodeType):
	tag = Mi


class MnType(TerminalNodeType):
	tag = Mn


class MoType(TerminalNodeType):
	tag = Mo


class MtableType(NonTerminalNodeType):
	tag = Mtable


class TwoMnType(TerminalNodeType):
	tag = Mn
	data = re.compile(r"^[2]$")


class ThreeMnType(TerminalNodeType):
	tag = Mn
	data = re.compile(r"^[3]$")


class TwoMiOperandItemType(NonTerminalNodeType):
	tag = Mrow
	child = [MiOperandType, MiOperandType]


class MoLineType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^[↔]$")


class LineType(NonTerminalNodeType):
	tag = Mover
	child = [TwoMiOperandItemType, MoLineType]
	name = 'LineType'


class MoLineSegmentType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^[¯―]$")


class LineSegmentType(NonTerminalNodeType):
	tag = Mover
	child = [TwoMiOperandItemType, MoLineSegmentType]
	name = 'LineSegmentType'


# Arrow above 2 symbols denotes Ray in English notation and vector in French notation
# (equivalent of VectorDoubleType).
# Arrow above 1 symbol denotes also vector in French notation.
class MoRayType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^[→]$")


# Arrow above 2 symbols denotes Ray in English notation and vector in French notation
# (equivalent of VectorDoubleType).
class RayType(NonTerminalNodeType):
	tag = Mover
	child = [TwoMiOperandItemType, MoRayType]
	name = 'RayType'


class MoVectorType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^[⇀]$")


class VectorSingleType(NonTerminalNodeType):
	tag = Mover
	child = [MiOperandType, MoVectorType]
	name = 'VectorSingleType'


class VectorDoubleType(NonTerminalNodeType):
	tag = Mover
	child = [TwoMiOperandItemType, MoVectorType]
	name = 'VectorDoubleType'


# Arrow above single symbol denotes vector in French notation.
class ArrowOverSingleSymbolType(NonTerminalNodeType):
	tag = Mover
	child = [MiOperandType, MoRayType]
	name = 'ArrowOverSingleSymbolType'


class MoFrownType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^[⌢]$")


class FrownType(NonTerminalNodeType):
	tag = Mover
	child = [TwoMiOperandItemType, MoFrownType]
	name = 'FrownType'


class MoDegreeType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^[°∘]$")


class DegreeType(NonTerminalNodeType):
	tag = Msup
	child = [MnOperandType, MoDegreeType, ]
	name = 'DegreeType'


class SingleType(CompoundNodeType):
	compound = [MiType, MnType, MoType]


class SingleMsubsupType(NonTerminalNodeType):
	tag = Msubsup
	child = [SingleType, SingleType, SingleType]
	name = 'SingleMsubsup'


class SingleMsubType(NonTerminalNodeType):
	tag = Msub
	child = [SingleType, SingleType]
	name = 'SingleMsub'


class SingleMsupType(NonTerminalNodeType):
	tag = Msup
	child = [SingleType, SingleType]
	name = 'SingleMsup'


class SingleMunderoverType(NonTerminalNodeType):
	tag = Munderover
	child = [SingleType, SingleType, SingleType]
	name = 'SingleMunderover'


class SingleMunderType(NonTerminalNodeType):
	tag = Munder
	child = [SingleType, SingleType]
	name = 'SingleMunder'


class SingleMoverType(NonTerminalNodeType):
	tag = Mover
	child = [SingleType, SingleType]
	name = 'SingleMover'


class SingleFractionType(FractionType):
	tag = Mfrac
	child = [OperandType, OperandType, ]
	name = 'single_fraction'


class SingleSqrtType(NonTerminalNodeType):
	tag = Msqrt
	child = [OperandType]
	name = 'single_square_root'


class PowerType(SingleMsupType):
	tag = Msup
	child = [OperandType, OperandType, ]
	name = 'power'


class SquarePowerType(PowerType):
	tag = Msup
	child = [OperandType, TwoMnType, ]
	name = 'SquarePowerType'


class CubePowerType(PowerType):
	tag = Msup
	child = [OperandType, ThreeMnType]
	name = 'CubePowerType'


class MsubsupFromToType(SingleMsubsupType):
	tag = Msubsup
	child = [FromToOperatorType, NodeType, NodeType]
	name = 'from_to'


class MunderoverFromToType(SingleMunderoverType):
	tag = Munderover
	child = [FromToOperatorType, NodeType, NodeType]
	name = 'from_to'


class MsubFromType(SingleMsubType):
	tag = Msub
	child = [FromToOperatorType, NodeType]
	name = 'from'


class MunderFromType(SingleMunderType):
	tag = Munder
	child = [FromToOperatorType, NodeType]
	name = 'from'


class MsupToType(SingleMsupType):
	tag = Msup
	child = [FromToOperatorType, NodeType]
	name = 'to'


class MoverToType(SingleMoverType):
	tag = Mover
	child = [FromToOperatorType, NodeType]
	name = 'to'


class MsubLogType(SingleMsubType):
	tag = Msub
	child = [LogOperatorType, OperandType]
	name = 'LogType'


class VerticalBarType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^\|$")


class AbsoluteType(SiblingNodeType):
	previous_siblings = [VerticalBarType]
	self_ = MnOperandType
	next_siblings = [VerticalBarType]
	name = 'absolute'


class OpenMatrixType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^\[$")


class CloseMatrixType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^\]$")


class MatrixType(SiblingNodeType):
	previous_siblings = [OpenMatrixType]
	self_ = MtableType
	next_siblings = [CloseMatrixType]
	name = 'matrix'


class DeterminantType(SiblingNodeType):
	tag = Mtable
	previous_siblings = [VerticalBarType]
	self_ = MtableType
	next_siblings = [VerticalBarType]
	name = 'determinant'


class BinomialType(FractionType):
	tag = Mfrac
	attrib = {
		'linethickness': re.compile(r"^[0]$"),
	}
	name = 'BinomialType'
	priority = 1


# SiblingNodeType
class SingleNumberFractionType(SingleFractionType):
	child = [MnOperandType, MnOperandType]
	name = ''


class AddIntegerFractionType(SiblingNodeType):
	previous_siblings = [MnOperandType]
	self_ = SingleNumberFractionType
	name = 'AddIntegerFractionType'
	priority = 1


class SignPreviousMoType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^[(*+-\./:<=>±·×÷−∔]$")


class MinusType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^[-−]$")


class NegativeSignType(SiblingNodeType):
	previous_siblings = [SignPreviousMoType]
	self_ = MinusType
	name = 'NegativeSignType'


class FirstNegativeSignType(SiblingNodeType):
	previous_siblings = [None]
	self_ = MinusType
	name = 'NegativeSignType'


class PlusType(TerminalNodeType):
	tag = Mo
	data = re.compile(r"^[+∔]$")


class PositiveSignType(SiblingNodeType):
	previous_siblings = [SignPreviousMoType]
	self_ = PlusType
	name = 'PositiveSignType'


class FirstPositiveSignType(SiblingNodeType):
	previous_siblings = [None]
	self_ = PlusType
	name = 'PositiveSignType'


class MathRule(object):
	def __init__(self, name, description, category, serialized_order, role, example=''):
		self.name = name
		self.description = description
		self.category = category
		self.serialized_order = serialized_order
		self.role = role
		self.example = example


def load_unicode_dic(path=None, language=''):
	if not path and language:
		path = os.path.dirname(os.path.abspath(__file__))
		if language != 'Windows' and language != 'braille':
			path = path + '/locale/{0}'.format(language)
		elif language == 'braille':
			path = path + '/locale/braille'
		else:
			path = path + '/locale/default'

	frp = os.path.join(path, 'unicode.dic')
	frp_user = os.path.join(path, 'unicode_user.dic')
	if not os.path.exists(frp_user):
		with io.open(frp, 'r', encoding='utf-8') as fr, io.open(frp_user, 'w', encoding='utf-8') as fr_user:
			fr_user.write(fr.read())
	path = frp_user

	symbol = {}
	try:
		with io.open(path, 'r', encoding='utf-8') as fr:
			for line in fr:
				line = line.split('\t')
				if len(line) >= 2:
					symbol[line[0]] = line[1].split(',')[0].strip()
	except:
		pass
	return symbol


def load_math_rule(path=None, language=''):
	math_example_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'math.example')
	if not path and language:
		path = os.path.dirname(os.path.abspath(__file__))
		if language != 'Windows' and language != 'braille':
			path = path + '/locale/{0}'.format(language)
		elif language == 'braille':
			path = path + '/locale/braille'
		else:
			path = path + '/locale/default'

	frp = os.path.join(path, 'math.rule')
	frp_user = os.path.join(path, 'math_user.rule')
	if not os.path.exists(frp_user):
		with io.open(frp, 'r', encoding='utf-8') as fr, io.open(frp_user, 'w', encoding='utf-8') as fr_user:
			fr_user.write(fr.read())
	path = frp_user

	mathrule = collections.OrderedDict({})
	for category_key in mathrule_category_order:
		category = mathrule_order[category_key]
		for item in category:
			mathrule[item] = None

	with io.open(path, 'r', encoding='utf-8') as fr, io.open(math_example_path, 'r', encoding='utf-8') as math_example:
		for line in fr:
			try:
				line = line.split('\t')
				if len(line) == 4:
					rule = []
					for i in line[1].split(','):
						i = i.strip()
						tuple_pattern = re.compile(r"\((.*)\.(.*)\)")
						s = tuple_pattern.search(i)
						if s:
							i = (s.group(1), s.group(2))

						try:
							rule.append(int(i))
						except:
							rule.append(i)

					role = []
					for i in line[2].split(','):
						i = i.strip()
						role.append(i)

					mathrule[line[0]] = MathRule(line[0], line[3].strip(), '', rule, role)
			except:
				pass

		for line in math_example:
			try:
				line = line.split('\t')
				if len(line) == 2:
					mathrule[line[0]].example = line[1].strip()
			except:
				pass

	return mathrule


def save_unicode_dic(symbol, path=None, language=''):
	if not path and language:
		path = os.path.dirname(os.path.abspath(__file__))
		if language != 'Windows':
			path = path + '/locale/{0}'.format(language)
		else:
			path = path + '/locale/default'
		path = os.path.join(path, 'unicode_user.dic')

	with io.open(path, 'w', encoding='utf-8') as f:
		f.write('symbols:\r\n')
		key = list(symbol.keys())
		key.sort()
		for k in key:
			line = '\t'.join([k, symbol[k], 'none']) + '\r\n'
			f.write(line)

	return True


def save_math_rule(mathrule, path=None, language=''):
	if not path and language:
		path = os.path.dirname(os.path.abspath(__file__))
		if language != 'Windows':
			path = path + '/locale/{0}'.format(language)
		else:
			path = path + '/locale/default'
		path = os.path.join(path, 'math_user.rule')

	mathrule_unicode = {}
	for k, v in mathrule.items():
		so_line = [str(i) if not isinstance(i, tuple) else '(' + '.'.join(i) + ')' for i in v.serialized_order]
		so_line = ', '.join(so_line)
		role_line = ', '.join(v.role)
		mathrule_unicode[k] = '\t'.join([so_line, role_line, v.description])

	with io.open(path, 'w', encoding='utf-8') as f:
		key = list(mathrule.keys())
		key.sort()
		for k in key:
			line = '\t'.join([k, mathrule_unicode[k]]) + '\r\n'
			f.write(line)

	return True


def symbol_translate(u):
	symbol_order = sorted(list(symbol.items()), key=lambda i: -len(i[0]))
	for key, value in symbol_order:
		u = u.replace(key, value)
	return u


def initialize(Access8MathConfig):
	global nodetypes_check
	nodetypes_check = []
	if Access8MathConfig:
		for i in nodetypes:
			if i.__name__ in Access8MathConfig["rules"]:
				if Access8MathConfig["rules"][i.__name__]:
					nodetypes_check.append(globals()[i.__name__])
			else:
				nodetypes_check.append(globals()[i.__name__])

		if not Access8MathConfig["settings"]["analyze_math_meaning"]:
			nodetypes_check = []

		# SNT_check = []
		# for i in SNT:
			# if i.__name__ in Access8MathConfig["rules"]:
				# if Access8MathConfig["rules"][i.__name__]:
					# SNT_check.append(globals()[i.__name__])
			# else:
				# SNT_check.append(globals()[i.__name__])

def ComplementMethod(method):
	def decorator(cls, obj):
		return not method(obj)
	return decorator

# get class which is Node subclass
nodes = {i.__name__: i for i in locals().values() if inspect.isclass(i) and issubclass(i, Node)}

# get class which is NodeType subclass
nodetypes = [i for i in locals().values() if inspect.isclass(i) and issubclass(i, NodeType)]
nodetypes = sorted(nodetypes, key=lambda c: -c.priority)
nodetypes_dict = {k: v for k, v in locals().items() if inspect.isclass(v) and issubclass(v, NodeType)}
SNT = [i for i in locals().values() if inspect.isclass(i) and issubclass(i, SiblingNodeType)]

notnodetypes = []
notnodetypes_dict = {}
for nodetype in nodetypes:
	dic = dict(nodetype.__dict__)
	dic.update({
		'check': classmethod(ComplementMethod(nodetype.check)),
		'name': '',
	})
	notnodetype = type('Not' + nodetype.__name__, nodetype.__bases__, dic)
	notnodetypes.append(notnodetype)
	notnodetypes_dict.update({
		'Not' + nodetype.__name__: notnodetype,
	})
	locals()['Not' + nodetype.__name__] = notnodetype

nodetypes_dict.update({'object': object})
all_nodetypes = [i for i in locals().values() if inspect.isclass(i) and issubclass(i, NodeType)]
all_nodetypes_dict = {k: v for k, v in locals().items() if inspect.isclass(v) and issubclass(v, NodeType)}
all_nodetypes_dict.update({'object': object})

mathrule_info = {
	"generics": {
		"node": [3, 1, "*"],
		"math": [3, 1, "*", ],
	},
	"fraction": {
		"mfrac": [5, 2, ".", ],
		"single_fraction": [5, 2, ".", ],
		"AddIntegerFractionType": [5, 2, ".", ],
		"BinomialType": [5, 2, ".", ],
	},
	"fenced": {
		"mfenced": [3, 1, "*", ],
		"absolute_value": [3, 1, "*", ],
		"determinant": [3, 1, "*", ],
		"matrix": [3, 1, "*", ],
	},
	"root": {
		"msqrt": [3, 1, "*", ],
		"mroot": [5, 2, ".", ],
		"single_square_root": [3, 1, ".", ],
	},
	"position": {
		"msubsup": [7, 3, ".", ],
		"msup": [5, 2, ".", ],
		"msub": [5, 2, ".", ],
		"munderover": [7, 3, ".", ],
		"munder": [5, 2, ".", ],
		"mover": [5, 2, ".", ],
		"SingleMsubsup": [7, 3, ".", ],
		"SingleMsub": [5, 2, ".", ],
		"SingleMsup": [5, 2, ".", ],
		"SingleMunderover": [7, 3, ".", ],
		"SingleMunder": [5, 2, ".", ],
		"SingleMover": [5, 2, ".", ],
	},
	"power": {
		"power": [5, 2, ".", ],
		"SquarePowerType": [3, 2, ".", ],
		"CubePowerType": [3, 2, ".", ],
	},
	"from to": {
		"from_to": [7, 3, ".", ],
		"from": [5, 2, ".", ],
		"to": [5, 2, ".", ],
		"LogType": [3, 2, ".", ],
	},
	"table": {
		"mtable": [3, 1, "*", ],
		"mtr": [3, 1, "*", ],
		"mtd": [3, 1, "*", ],
	},
	"line": {
		"LineType": [3, 2, ".", ],
		"RayType": [3, 2, ".", ],
		"LineSegmentType": [3, 2, ".", ],
		"VectorSingleType": [3, 2, ".", ],
		"VectorDoubleType": [3, 2, ".", ],
		"ArrowOverSingleSymbolType": [3, 2, ".", ],
		"FrownType": [3, 2, ".", ],
		"DegreeType": [3, 2, ".", ],
	},
	"other": {
		"NegativeSignType": [1, 1, ".", ],
		"PositiveSignType": [1, 1, ".", ],
		"mmultiscripts": [0, 0, ".", ],
		"mprescripts": [0, 0, ".", ],
		"none": [0, 0, ".", ],
	},
}

mathrule_category_order = [
	"generics",
	"fraction",
	"fenced",
	"root",
	"position",
	"power",
	"from to",
	"table",
	"line",
	"other",
]

mathrule_order = {
	"generics": [
		"node",
		"math",
	],
	"fraction": [
		"mfrac",
		"single_fraction",
		"AddIntegerFractionType",
		"BinomialType",
	],
	"fenced": [
		"mfenced",
		"absolute_value",
		"determinant",
		"matrix",
	],
	"root": [
		"msqrt",
		"mroot",
		"single_square_root",
	],
	"position": [
		"msubsup",
		"msup",
		"msub",
		"munderover",
		"munder",
		"mover",
		"SingleMsubsup",
		"SingleMsub",
		"SingleMsup",
		"SingleMunderover",
		"SingleMunder",
		"SingleMover",
	],
	"power": [
		"power",
		"SquarePowerType",
		"CubePowerType",
	],
	"from to": [
		"from_to",
		"from",
		"to",
	],
	"table": [
		"mtable",
		"mtr",
		"mtd",
	],
	"line": [
		"LineType",
		"RayType",
		"LineSegmentType",
		"VectorSingleType",
		"VectorDoubleType",
		"ArrowOverSingleSymbolType",
		"FrownType",
		"DegreeType",
	],
	"other": [
		"NegativeSignType",
		"PositiveSignType",
		"mmultiscripts",
		"mprescripts",
		"none",
	],
}

def mathrule_validate(mathrule, validator):
	result = True
	if not len(mathrule.serialized_order) == validator[0]:
		result = False
	if not len(mathrule.role) == validator[1]:
		result = False
	if validator[2] == ".":
		for index in range(len(mathrule.serialized_order)):
			if index % 2 == 0:
				if not isinstance(mathrule.serialized_order[index], str):
					result = False
			else:
				if not isinstance(mathrule.serialized_order[index], int):
					result = False
	elif validator[2] == "*":
		if not isinstance(mathrule.serialized_order[0], str):
			result = False
		elif not isinstance(mathrule.serialized_order[1], tuple):
			result = False
		elif not isinstance(mathrule.serialized_order[2], str):
			result = False
	else:
		pass
	return result

initialize(None)

"""for category_key in mathrule_category_order:
	category = mathrule_order[category_key]
	for item in category:
		if not mathrule_validate(mathrule[item], mathrule_info[category_key][item]):
			pass
"""