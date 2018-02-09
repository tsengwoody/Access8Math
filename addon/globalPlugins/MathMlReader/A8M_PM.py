# coding: utf-8
# Copyright (C) 2017-2018 Tseng Woody <tsengwoody.tw@gmail.com>

import copy
import io
import os
import re
import sys
import weakref

AUTO_GENERATE = 0
DIC_GENERATE = 1

def create_node(et):
	p_tag = re.compile(r'[\{].*[\}](?P<mp_type>.+)')
	r = p_tag.search(et.tag)
	try:
		mp_tag = r.group('mp_type')
	except:
		mp_tag = et.tag

	node_class = nodes[mp_tag.capitalize()] if mp_tag.capitalize() in nodes.keys() else object

	if issubclass(node_class, NonTerminalNode) or (issubclass(node_class, BlockNode) and len(et)!=1):
		child = []
		for c in et:
			node = create_node(c)
			child.append(node)
		node = node_class(child, et.attrib)
	elif issubclass(node_class, TerminalNode):
		node = node_class([], et.attrib, data=et.text)
	elif issubclass(node_class, BlockNode) and len(et) == 1:
		node = create_node(et[0])
	elif mp_tag == 'none':
		node = Nones()
	#elif mp_tag == 'semantics':
		#node = create_node(et[0])
	else:
		child = []
		for c in et:
			node = create_node(c)
			child.append(node)
		node = Node(child, et.attrib)
		#raise RuntimeError('unknown tag : {}'.format(mp_tag))

	return node

class Node(object):
	def __init__(self, child=[], attrib={}, data=u''):
		self._parent = None
		self.child = list(child)
		for c in child:
			if isinstance(c, Node):
				c.parent = self
		self.attrib = attrib
		self.data = unicode(data.strip()) if data else u''
		self.type = None
		for nodetype in nodetypes:
			if nodetype.check(self) and nodetype.name in math_rule:
				self.type = nodetype
				break

		self.role = math_role[self.name] if math_role.has_key(self.name) else [symbol_translate('item')]
		d = len(self.child) -len(self.role)
		if d > 0:
			append = self.role[-1]
			self.role = self.role[:-1]
			for i in range(d+1):
				self.role.append(u'{0}{1}'.format(append, i+1))
			self.role_level = AUTO_GENERATE
		else:
			self.role_level = DIC_GENERATE

	def rule(self):
		if self.type and self.type.rule and AMM:
			if issubclass(self.type, NonTerminalNodeType):
				rule = self.type.rule()
			elif issubclass(self.type, TerminalNodeType):
				rule = [unicode(self.type.data.sub(self.type.rule, self.data))]
		else:
			rule = math_rule[self.tag]
		if isinstance(rule[1], tuple):
			result = []
			for i in range(len(self.child)):
				if not rule[1][0] == u' ':
					result.append(u'{0}{1}'.format(rule[1][0], i+1))
				result.append(i)

			rule = rule[0:1] +result +rule[-1:]
		return rule

	def serialized(self):
		serialized = []
		if isinstance(self, TerminalNode):
			serialized = serialized +['@10@']
		for r in self.rule():
			if isinstance(r, int):
				serialized = serialized +self.child[r].serialized()
			elif r == '*':
				for c in self.child:
					serialized = serialized +c.serialized() if c else serialized
					serialized = serialized +['@10@']
			elif isinstance(r, unicode):
				serialized = serialized +[r]
			else:
				raise TypeError('rule element type error : expect int or unicode (get {0})'.format(type(r)))
		if isinstance(self, TerminalNode):
			serialized = serialized +['@10@']
		return serialized

	def get_mathml(self):
		mathml = u''
		for c in self.child:
			mathml = mathml +c.get_mathml()
		attrib = u''
		for k, v in self.attrib.items():
			attrib = attrib +u'{0}="{1}"'.format(k,v)

		return u'<{0} {1}>{2}</{0}>'.format(self.tag, attrib, mathml)

	@property
	def des(self):
		return self.parent.role[self.index_in_parent()] if self.parent else symbol_translate('math')

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
			index = self.index_in_parent() +1
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
			index = self.index_in_parent() -1
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
		next= current.next_sibling
		while not next:
			current = current.parent
			if not current:
				return None
			next= current.next_sibling
		return next

	@property
	def previous(self):
		current = self
		previous= current.previous_sibling
		while not previous:
			current = current.parent
			if not current:
				return None
			previous= current.previous_sibling
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
	pass

class TerminalNode(Node):
	def rule(self):
		try:
			return super(TerminalNode, self).rule()
		except:
			return [unicode(symbol_translate(self.data))]

	def get_mathml(self):
		mathml = u''
		mathml = mathml +self.data if self.data else mathml
		return u'<{0}>{1}</{0}>'.format(self.tag, mathml)

class BlockNode(Node):
	def rule(self):
		try:
			return super(BlockNode, self).rule()
		except:
			return [u''] +range(len(self.child)) +[u'']

class Math(NonTerminalNode):
	pass

class Mrow(BlockNode):
	pass

class Mstyle(BlockNode):
	pass

class Mi(TerminalNode):
	def __init__(self, child=[], attrib={}, data=None):
		super(Mi, self).__init__(child, attrib, data)
		self.identifier = data

class Mn(TerminalNode):
	def __init__(self, child=[], attrib={}, data=None):
		super(Mn, self).__init__(child, attrib, data)
		self.number = data

class Mo(TerminalNode):
	def __init__(self, child=[], attrib={}, data=None):
		super(Mo, self).__init__(child, attrib, data)
		self.operator = data

class Mtext(TerminalNode):
	pass

class Mspace(TerminalNode):
	pass

class Ms(TerminalNode):
	pass

class Mfrac(NonTerminalNode):
	pass

class Mfenced(NonTerminalNode):
	def rule(self):
		rule = super(Mfenced, self).rule()
		if not self.type:
			if self.attrib.has_key('open'):
				rule = [unicode(self.attrib['open'])] +rule
			if self.attrib.has_key('close'):
				rule = rule[0:-1] +[unicode(self.attrib['close'])] +rule[-1:]
			if (not self.attrib.has_key('open')) and (not self.attrib.has_key('close')):
				rule = [u'('] +rule[0:-1] +[u')'] +rule[-1:]

		return rule

class Msqrt(NonTerminalNode):
	pass

class Mroot(NonTerminalNode):
	pass

class Msubsup(NonTerminalNode):
	pass

class Msub(NonTerminalNode):
	pass

class Msup(NonTerminalNode):
	pass

class Munderover(NonTerminalNode):
	pass

class Munder(NonTerminalNode):
	pass

class Mover(NonTerminalNode):
	pass

class Mtable(NonTerminalNode):
	def rule(self):
		rule = super(Mtable, self).rule()

		row_count = len(self.child)
		column_count_list = [len(i.child) for i in self.child]
		column_count = max(column_count_list)
		table_head = [rule[0] +u'{0}{1}{2}{3}{4}'.format(symbol_translate('has'), row_count, symbol['row'], column_count, symbol['column'])]
		cell = rule[1:-1]
		table_tail = rule[-1:]
		return table_head +cell +table_tail

class Mtr(NonTerminalNode):
	def rule(self):
		rule = super(Mtr, self).rule()
		cell = rule[1:-1]
		return rule[:1] +cell +rule[-1:]

class Mtd(NonTerminalNode):
	pass

class Mmultiscripts(NonTerminalNode):
	def __init__(self, *args, **kwargs):
		super(Mmultiscripts, self).__init__(*args, **kwargs)

		role = [symbol_translate('main')]

		index = range(1, self.mprescripts_index_in_child())
		for count in range(len(index)/2):
			temp = [
				u'{0}{1}{2}'.format(symbol_translate('order'), count, symbol_translate('rightdownmark')),
				u'{0}{1}{2}'.format(symbol_translate('order'), count, symbol_translate('rightupmark')),
			]
			role = role +temp

		role = role +[symbol_translate('mprescripts_index')]

		index = range(self.mprescripts_index_in_child() +1, len(self.child))
		for count in range(len(index)/2):
			temp = [
				u'{0}{1}{2}'.format(symbol_translate('order'), count, symbol_translate('leftdownmark')),
				u'{0}{1}{2}'.format(symbol_translate('order'), count, symbol_translate('leftupmark')),
			]
			role = role +temp

		self.role = role

	def rule(self):
		rule = super(Mmultiscripts, self).rule()

		index = range(1, self.mprescripts_index_in_child())
		index_odd = index[0::2]
		index_even = index[1::2]
		index_mix = zip(index_odd, index_even)
		for  count,item in enumerate(index_mix):
			temp = [
				u'{0}{1}{2}'.format(symbol_translate('order'), count, symbol_translate('rightdownmark')),
				item[0],
				u'{0}{1}{2}'.format(symbol_translate('order'), count, symbol_translate('rightupmark')),
				item[1],
			]
			rule = rule[:1] +temp +rule[-1:]

		index = range(self.mprescripts_index_in_child() +1, len(self.child))
		index_odd = index[0::2]
		index_even = index[1::2]
		index_mix = zip(index_odd, index_even)
		for  count,item in enumerate(index_mix):
			temp = [
				u'{0}{1}{2}'.format(symbol_translate('order'), count, symbol_translate('leftdownmark')),
				item[0],
				u'{0}{1}{2}'.format(symbol_translate('order'), count, symbol_translate('leftupmark')),
				item[1],
			]
			rule = rule[:1] +temp +rule[-1:]

		rule.insert(1,0)
		return rule

	def mprescripts_index_in_child(self):
		for c in self.child:
			if isinstance(c, Mprescripts):
				return self.child.index(c)

class Mprescripts(TerminalNode):
	pass

class Nones(Node):
	def rule(self):
		return []

class NodeType(object):
	tag = object
	child = []
	attrib = {}
	data = re.compile(r".*")
	name = ''
	rule = None

	@classmethod
	def check(cls, obj):
		result = []
		if not issubclass(obj.__class__, cls.tag):
			return False

		#check attrib
		for key, value in cls.attrib.items():
			if not obj.attrib.has_key(key):
				return False
			elif not value.search(obj.attrib[key]) is not None:
				return False

		#check child
		d = len(obj.child) - (len(cls.child) -1)
		if d > 0 and len(cls.child) > 0 and cls.child[-1]=='*':
			type_list = cls.child[:-1] +[cls.child[-2]]*d
		else:
			type_list = cls.child
		for mt, o in zip(type_list, obj.child):
			if not mt.check(o):
				return False
		if not obj.data == '':
			try:
				if not cls.data.search(obj.data) is not None:
					return False
			except:
				return False
		return True
		#return False if False in result else True

class TerminalNodeType(NodeType):

	@classmethod
	def rule(cls, m):
		temp = ''
		if not math_rule.has_key(cls.name):
			return None
		for i in math_rule[cls.name]:
			if isinstance(i, int):
				temp = temp +m.group(int(i))
			else:
				temp = temp +i
		return temp

class NonTerminalNodeType(NodeType):

	@classmethod
	def rule(cls):
		return math_rule[cls.name]

class CompoundNodeType(NodeType):
	compound = []

	@classmethod
	def check(cls, obj):
		for mt in cls.compound:
			if mt.check(obj):
				return True
		return False

class MiOperandType(TerminalNodeType):
	tag = Mi
	data = re.compile(r"^[\d\w]+$")

class MnOperandType(TerminalNodeType):
	tag = Mn
	data = re.compile(r"^[\d\w]+$")

class OperandType(CompoundNodeType):
	compound = [MiOperandType, MnOperandType]

class OperatorType(TerminalNodeType):
	tag = Mo
	data = re.compile(ur"^[u'\u2200'-u'\u22FF']$")

class FromToOperatorType(TerminalNodeType):
	tag = Mo
	data = re.compile(ur"^[∑∫]$")

class MtableType(NonTerminalNodeType):
	tag = Mtable

class PowerType(NonTerminalNodeType):
	tag = Msup
	child = [OperandType, OperandType,]
	name = 'power'

class MsubsupFromToType(NonTerminalNodeType):
	tag = Msubsup
	child = [FromToOperatorType]
	name = 'from_to'

class MunderoverFromToType(NonTerminalNodeType):
	tag = Munderover
	child = [FromToOperatorType]
	name = 'from_to'

class SetType(NonTerminalNodeType):
	tag = Mfenced
	attrib = {
		'open': re.compile(ur"^[\{]$"),
		'close': re.compile(ur"^[\}]$"),
	}
	name = 'set'

class AbsoluteType(NonTerminalNodeType):
	tag = Mfenced
	attrib = {
		'open': re.compile(ur"^[|]$"),
		'close': re.compile(ur"^[|]$"),
	}
	name = 'absolute_value'

class MatrixType(NonTerminalNodeType):
	tag = Mfenced
	attrib = {
		'open': re.compile(ur"^[\[]$"),
		'close': re.compile(ur"^[\]]$"),
	}
	child = [MtableType]
	name = 'matrix'

class DeterminantType(NonTerminalNodeType):
	tag = Mfenced
	attrib = {
		'open': re.compile(ur"^[|]$"),
		'close': re.compile(ur"^[|]$"),
	}
	child = [MtableType]
	name = 'determinant'

class SingleFractionType(NonTerminalNodeType):
	tag = Mfrac
	child = [OperandType, OperandType,]
	name = 'single_fraction'

class SingleSqrtType(NonTerminalNodeType):
	tag = Msqrt
	child = [OperandType]
	name = 'single_square_root'

class MiType(TerminalNodeType):
	tag = Mi

class MnType(TerminalNodeType):
	tag = Mn

class MoType(TerminalNodeType):
	tag = Mo

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

class LimitOperatorType(TerminalNodeType):
	tag = Mi
	data = re.compile(ur"^[Ll][Ii][Mm]$")

class LimitApproacheType(TerminalNodeType):
	tag = TerminalNode
	data = re.compile(ur"^([→])$")
	name = 'limit_approache'

class LimitType(NonTerminalNodeType):
	tag = Munder
	child = [LimitOperatorType, ]
	name = 'limit'

def load_unicode_dic(language):
	path = os.path.dirname(os.path.abspath(__file__))
	if not language == 'Windows':
		path = path +'/locale/{0}'.format(language)
	symbol = {}

	frp = os.path.join(path, 'unicode.dic')
	frp_user = os.path.join(path, 'unicode_user.dic')
	if not os.path.exists(frp_user):
		with io.open(frp, 'r', encoding='utf-8') as fr, io.open(frp_user, 'w', encoding='utf-8') as fr_user:
			fr_user.write(fr.read())

	try:
		with io.open(frp, 'r', encoding='utf-8') as fr:
			for line in fr:
				line = line.split('\t')
				if len(line) >= 2:
					symbol[line[0]] = line[1].split(',')[0].strip()
	except:
		pass
	return symbol

def load_math_rule(language):
	path = os.path.dirname(os.path.abspath(__file__))
	if not language == 'Windows':
		path = path +'/locale/{0}'.format(language)
	math_role = {}
	math_rule = {}

	frp = os.path.join(path, 'math.rule')
	frp_user = os.path.join(path, 'math_user.rule')
	if not os.path.exists(frp_user):
		with io.open(frp, 'r', encoding='utf-8') as fr, io.open(frp_user, 'w', encoding='utf-8') as fr_user:
			fr_user.write(fr.read())

	try:
		with io.open(frp_user, 'r', encoding='utf-8') as fr:
			for line in fr:
				line = line.split('\t')
				if len(line) == 3:
					rule = []
					for i in line[1].split(','):
						i = i.strip()
						tuple_pattern = re.compile(ur'\((.*)\.(.*)\)')
						s = tuple_pattern.search(i)
						if s:
							i= (s.group(1), s.group(2))

						try:
							rule.append(int(i))
						except:
							rule.append(i)
					math_rule[line[0]] = rule

					role = []
					for i in line[2].split(','):
						i = i.strip()
						role.append(i)
					math_role[line[0]] = role
	except:
		pass

	return [math_role, math_rule]

def save_unicode_dic(language, symbol):
	path = os.path.dirname(os.path.abspath(__file__))
	if not language == 'Windows':
		path = path +'/locale/{0}'.format(language)

def save_math_rule(language, math_role, math_rule):
	path = os.path.dirname(os.path.abspath(__file__))
	if not language == 'Windows':
		path = path +'/locale/{0}'.format(language)

	math_rule_unicode = {}
	for k,v in math_rule.items():
		line = [unicode(i) if not isinstance(i, tuple) else '(' +'.'.join(i) +')' for i in v]
		line = ', '.join(line)
		math_rule_unicode[k] = line

	math_role_unicode = {}
	for k,v in math_role.items():
		line = ', '.join(v)
		math_role_unicode[k] = line

	fwp = os.path.join(path, 'math_user.rule')
	with io.open(fwp, 'w', encoding='utf-8') as f:
		key = math_rule.keys()
		key.sort()
		for k in key:
			line = '\t'.join([k, math_rule_unicode[k], math_role_unicode[k]]) +'\r\n'
			f.write(line)

	return True

def symbol_translate(u):
	return symbol[u] if symbol.has_key(u) else u

import inspect
# get class which is Node subclass
nodes = { i.__name__: i for i in locals().values() if inspect.isclass(i) and issubclass(i, Node) }

# get class which is NodeType subclass
nodetypes = [ i for i in locals().values() if inspect.isclass(i) and issubclass(i, NodeType) ]

language = os.environ.get('LANGUAGE', 'Windows')
symbol = load_unicode_dic(language)
math_role, math_rule = load_math_rule(language)
AMM = True if os.environ.get('AMM', 'True') in [u'True', u'true'] else False



import os
import re
import sys
path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path)
Base_Dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, Base_Dir)
import cgi
import HTMLParser
import xml
from xml.etree import ElementTree as ET
if __name__ == '__main__':
	mathMl = u'<math><mfenced><mrow><mo>-</mo><mn>2</mn></mrow></mfenced><mo>&times;</mo><mfenced close="|" open="|"><mrow><mo>-</mo><mn>5</mn></mrow></mfenced><mo>-</mo><mfenced close="|" open="|"><mrow><mo>-</mo><mn>3</mn></mrow></mfenced></math>'
	gtlt_pattern = re.compile(ur"([\>])(.*?)([\<])")
	mathMl = gtlt_pattern.sub(lambda m: m.group(1) +cgi.escape(HTMLParser.HTMLParser().unescape(m.group(2))) +m.group(3), mathMl)
	quote_pattern = re.compile(ur"([\"\'])(.*?)\1")
	mathMl = quote_pattern.sub(lambda m: m.group(1) +cgi.escape(m.group(2)) +m.group(1), mathMl)
	parser = ET.XMLParser()

	tree = ET.fromstring(mathMl.encode('utf-8'), parser=parser)
	node = create_node(tree)