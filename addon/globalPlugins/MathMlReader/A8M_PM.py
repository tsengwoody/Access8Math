# coding: utf-8
# Copyright (C) 2017-2018 Tseng Woody <tsengwoody.tw@gmail.com>

import collections
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
		#raise RuntimeError('unknown tag : {}'.format(mp_tag))

	return node

def clean_allnode(node):
	for child in node.child:
		clean_allnode(child)

	if isinstance(node, BlockNode):
		if len(node.child)==1 or (isinstance(node.parent, AlterNode) and len(node.child)>0):

			#remove node
			parent_new_child = node.parent.child[0:node.index_in_parent()] +node.child
			if node.index_in_parent()+1 < len(node.parent.child):
				parent_new_child = parent_new_child +node.parent.child[node.index_in_parent()+1:]
			node.parent.child = parent_new_child
			for child in node.child:
				child.parent = node.parent

		elif isinstance(node.parent, AlterNode) and len(node.child)==0:
			index = node.index_in_parent()
			node.parent.child[index].child = []


	return  node

def set_mathrule_allnode(node, mathrule):
	for child in node.child:
		set_mathrule_allnode(child, mathrule)
	node.set_mathrule(mathrule)
	return  node

def clear_type_allnode(node):
	for child in node.child:
		clear_type_allnode(child)
	node.type = None
	return  node

def check_type_allnode(node):
	for child in node.child:
		check_type_allnode(child)
	node.check_type()
	return  node

class MathContent(object):
	def __init__(self, mathrule, et):
		self.root = self.pointer = create_node(et)
		clean_allnode(self.root)
		self.mathrule = {}
		self.set_mathrule(mathrule)

	def set_mathrule(self, mathrule):
		self.mathrule = mathrule
		set_mathrule_allnode(self.root, self.mathrule)
		check_type_allnode(self.root)

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
		else:
			return False

	def insert(self, node):
		if self.pointer.parent:
			self.pointer.parent.insert(self.pointer.index_in_parent(), node)
			self.pointer = node

			# node refresh
			clean_allnode(self.root)
			clear_type_allnode(self.root)
			set_mathrule_allnode(self.root, self.mathrule)
			check_type_allnode(self.root)

		else:
			self.pointer.insert(len(self.pointer.child), node)
			self.pointer = node

			# node refresh
			clean_allnode(self.root)
			clear_type_allnode(self.root)
			set_mathrule_allnode(self.root, self.mathrule)
			check_type_allnode(self.root)

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
	def __init__(self, child=[], attrib={}, data=u''):
		self._mathcontent = None
		self._parent = None
		self.child = list(child)
		for c in child:
			if isinstance(c, Node):
				c.parent = self
		self.attrib = attrib
		self.data = unicode(data.strip()) if data else u''
		self.mathrule = {}
		self.rule = []
		self.role = []
		self.type = None
		#self.set_mathrule(mathrule)
		#self.check_type()

	def check_type(self):
		for nodetype in nodetypes_check:
			if nodetype.check(self) and nodetype.name in self.mathrule:
				if not self.type:
					self.type = nodetype()
				elif self.type and issubclass(nodetype, self.type.__class__):
					self.type = nodetype()

		if self.type:
			self.type.set_mathrule(self.mathrule)

			self.type.set_rule()
			self.set_role()
			self.set_rule()

	def set_mathrule(self, mathrule):
		self.mathrule = mathrule
		self.set_role()
		self.set_rule()
		if self.type:
			self.type.set_mathrule(self.mathrule)

	def set_role(self):
		self.role = self.mathrule[self.name].role if mathrule.has_key(self.name) else [symbol_translate('item')]
		d = len(self.child) -len(self.role)
		if d > 0:
			append = self.role[-1]
			self.role = self.role[:-1]
			for i in range(d+1):
				self.role.append(u'{0}{1}'.format(append, i+1))
			self.role_level = AUTO_GENERATE
		else:
			self.role_level = DIC_GENERATE

	def set_rule(self):
		if self.type and self.type.rule:
			rule = self.type.rule
		else:
			rule = self.mathrule[self.name].serialized_order
		if len(rule)>=2 and isinstance(rule[1], tuple):
			result = []
			for i in range(len(self.child)):
				if not (rule[1][0].isspace() or rule[1][0]==u''):
					result.append(u'{0}{1}'.format(rule[1][0], i+1))
				result.append(i)

			rule = rule[0:1] +result +rule[-1:]
		self.rule = rule

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
			elif isinstance(r, unicode):
				serialized.append([r])
			else:
				raise TypeError('rule element type error : expect int or unicode (get {0})'.format(type(r)))
		if isinstance(self, TerminalNode):
			serialized.append(['@10@'])
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
	def mathcontent(self):
		return None if self._mathcontent is None else self._mathcontent()

	@mathcontent.setter
	def mathcontent(self, mathcontent):
		self._mathcontent = weakref.ref(mathcontent)

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
	def set_rule(self):
		try:
			super(NonTerminalNode, self).set_rule()
		except:
			self.rule = range(len(self.child))

	def set_role(self):
		try:
			super(NonTerminalNode, self).set_role()
		except:
			self.rule = range(len(self.child))

class TerminalNode(Node):
	def set_rule(self):
		try:
			super(TerminalNode, self).set_rule()
		except BaseException as e:
			self.rule = [unicode(symbol_translate(self.data))]

	def get_mathml(self):
		mathml = u''
		mathml = mathml +self.data if self.data else mathml
		return u'<{0}>{1}</{0}>'.format(self.tag, mathml)

class AlterNode(NonTerminalNode):
	def insert(self, index, node):
		if index > len(self.child):
			return None
		if index == len(self.child):
			self.child.insert(index+1, node)
			node.parent = self
		elif isinstance(self.child[index], BlockNode) and len(self.child[index].child) == 0:
			self.child[index].child.insert(0, node)
			node.parent = self.child[index]
		else:
			self.child.insert(index+1, node)
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
			super(BlockNode, self).set_rule()
		except:
			self.rule = range(len(self.child))

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
		super(Mfenced, self).set_rule()
		rule = self.rule
		if not self.type:
			if self.attrib.has_key('open'):
				rule = [unicode(self.attrib['open'])] +rule
			if self.attrib.has_key('close'):
				rule = rule[0:-1] +[unicode(self.attrib['close'])] +rule[-1:]
			if (not self.attrib.has_key('open')) and (not self.attrib.has_key('close')):
				rule = [u'('] +rule[0:-1] +[u')'] +rule[-1:]

		self.rule = rule

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
		super(Mtable, self).set_rule()
		rule = self.rule

		row_count = len(self.child)
		column_count_list = [len(i.child) for i in self.child]
		column_count = max(column_count_list)
		table_head = [rule[0] +u'{0}{1}{2}{3}{4}'.format(symbol_translate('has'), row_count, symbol_translate('row'), column_count, symbol_translate('column'))]
		cell = rule[1:-1]
		table_tail = rule[-1:]
		self.rule = table_head +cell +table_tail

class Mlabeledtr(AlterNode):
	pass

class Mtr(AlterNode):
	def set_rule(self):
		super(Mtr, self).set_rule()
		rule = self.rule
		cell = rule[1:-1]
		self.rule = rule[:1] +cell +rule[-1:]

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
	pass

class Ms(TerminalNode):
	pass

class Mmultiscripts(AlterNode):
	'''def __init__(self, *args, **kwargs):
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

		self.role = role'''

	def set_rule(self):
		super(Mmultiscripts, self).set_rule()
		rule = self.rule

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
		self.rule = rule

	def mprescripts_index_in_child(self):
		for c in self.child:
			if isinstance(c, Mprescripts):
				return self.child.index(c)

class Mprescripts(TerminalNode):
	pass

class Nones(Node):
	pass

class NodeType(object):
	tag = object
	child = [u'object', '*']
	attrib = {}
	data = re.compile(r".*")
	name = 'nodetype'

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

class TerminalNodeType(NodeType):
	@classmethod
	def check(cls, obj):
		if not issubclass(obj.__class__, cls.tag):
			return False

		#check attrib
		for key, value in cls.attrib.items():
			if not obj.attrib.has_key(key):
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
		if cls.child[-1]=='*' and len(cls.child)>1:
			d = len(obj.child) - (len(cls.child) -1)
			type_list = cls.child[:-1] +[cls.child[-2]]*d
		else:
			type_list = cls.child
		if not len(type_list) == len(obj.child):
			return False

		# change type
		type_list_str = [t if isinstance(t, unicode) else t.__name__ for t in type_list]
		type_list = [all_nodetypes_dict[t] for t in type_list_str]

		# check child type
		for mt, o in zip(type_list, obj.child):
			if not mt==object and not mt.check(o):
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
		if not self_index is None:
			start_index = self_index -cpsl
			if cpsl>0 and cls_previous_siblings[0] == None:
				cls_previous_siblings = cls_previous_siblings[1:]
				if not start_index==-1:
					return False
			elif start_index < 0:
				return False

			end_index = self_index +cnsl
			if cnsl>0 and cls_next_siblings[-1] == None:
				cls_next_siblings = cls_next_siblings[:-1]
				if not end_index==len(obj.parent.child):
					return False
			elif end_index > len(obj.parent.child):
				return False
		else:
			return False

		if not cls.self_.check(obj):
			return False

		# change type
		type_list = cls_previous_siblings
		type_list_str = [t if isinstance(t, unicode) else t.__name__ for t in type_list]
		type_list = [all_nodetypes_dict[t] for t in type_list_str]
		obj_previous_siblings = obj.parent.child[start_index:self_index]
		for mt, o in zip(type_list, obj_previous_siblings):
			if not mt==object and not mt.check(o):
				return False

		type_list = cls_next_siblings
		type_list_str = [t if isinstance(t, unicode) else t.__name__ for t in type_list]
		type_list = [all_nodetypes_dict[t] for t in type_list_str]
		obj_next_siblings = obj.parent.child[self_index+1:end_index+1]
		for mt, o in zip(type_list, obj_next_siblings):
			if not mt==object and not mt.check(o):
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
	compound = [MiOperandType, MnOperandType, FractionType,]

class OperatorType(TerminalNodeType):
	tag = Mo
	data = re.compile(ur"^[u'\u2200'-u'\u22FF']$")

class FromToOperatorType(TerminalNodeType):
	tag = Mo
	data = re.compile(ur"^[∑∫]$")

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
	data = re.compile(ur"^[2]$")

class ThreeMnType(TerminalNodeType):
	tag = Mn
	data = re.compile(ur"^[3]$")

class TwoMiOperandItemType(NonTerminalNodeType):
	tag = Mrow
	child = [MiOperandType, MiOperandType]

class MoLineType(TerminalNodeType):
	tag = Mo
	data = re.compile(ur"^[↔]$")

class LineType(NonTerminalNodeType):
	tag = Mover
	child = [TwoMiOperandItemType, MoLineType]
	name = 'LineType'

class MoLineSegmentType(TerminalNodeType):
	tag = Mo
	data = re.compile(ur"^[¯]$")

class LineSegmentType(NonTerminalNodeType):
	tag = Mover
	child = [TwoMiOperandItemType, MoLineSegmentType]
	name = 'LineSegmentType'

class MoRayType(TerminalNodeType):
	tag = Mo
	data = re.compile(ur"^[→]$")

class RayType(NonTerminalNodeType):
	tag = Mover
	child = [TwoMiOperandItemType, MoRayType]
	name = 'RayType'

class MoVectorType(TerminalNodeType):
	tag = Mo
	data = re.compile(ur"^[⇀]$")

class VectorSingleType(NonTerminalNodeType):
	tag = Mover
	child = [MiOperandType, MoVectorType]
	name = 'VectorSingleType'

class VectorDoubleType(NonTerminalNodeType):
	tag = Mover
	child = [TwoMiOperandItemType, MoVectorType]
	name = 'VectorDoubleType'

class MoFrownType(TerminalNodeType):
	tag = Mo
	data = re.compile(ur"^[⌢]$")

class FrownType(NonTerminalNodeType):
	tag = Mover
	child = [TwoMiOperandItemType, MoFrownType]
	name = 'FrownType'

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
	child = [OperandType, OperandType,]
	name = 'single_fraction'

class SingleSqrtType(NonTerminalNodeType):
	tag = Msqrt
	child = [OperandType]
	name = 'single_square_root'

class PowerType(SingleMsupType):
	tag = Msup
	child = [OperandType, OperandType,]
	name = 'power'

class SquarePowerType(PowerType):
	tag = Msup
	child = [OperandType, TwoMnType,]
	name = 'SquarePowerType'

class CubePowerType(PowerType):
	tag = Msup
	child = [OperandType, ThreeMnType,]
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

class DeterminantType(AbsoluteType):
	tag = Mfenced
	attrib = {
		'open': re.compile(ur"^[|]$"),
		'close': re.compile(ur"^[|]$"),
	}
	child = [MtableType]
	name = 'determinant'

# SiblingNodeType

class SingleNumberFractionType(SingleFractionType):
	child = [MnOperandType, MnOperandType,]
	name = ''

class AddIntegerFractionType(SiblingNodeType):
	previous_siblings = [MnOperandType]
	self_ = SingleNumberFractionType
	name = 'AddIntegerFractionType'

class SignPreviousMoType(TerminalNodeType):
	tag = Mo
	data = re.compile(ur"^[(*+-\./:<=>±·×÷−∔]$")

class MinusType(TerminalNodeType):
	tag = Mo
	data = re.compile(ur"^[-−]$")

class NegativeSignType(SiblingNodeType):
	previous_siblings = [SignPreviousMoType]
	self_ = MinusType
	name = 'NegativeSignType'

class FirstNegativeSignType(SiblingNodeType):
	previous_siblings = [None,]
	self_ = MinusType
	name = 'NegativeSignType'

class PlusType(TerminalNodeType):
	tag = Mo
	data = re.compile(ur"^[+∔]$")

class PositiveSignType(SiblingNodeType):
	previous_siblings = [SignPreviousMoType]
	self_ = PlusType
	name = 'PositiveSignType'

class FirstPositiveSignType(SiblingNodeType):
	previous_siblings = [None,]
	self_ = PlusType
	name = 'PositiveSignType'

class MathRule(object):
	def __init__(self, name, description, category, serialized_order, role, example=''):
		self.name = name
		self.description = description
		self.category= category
		self.serialized_order = serialized_order
		self.role = role
		self.example = example

def load_unicode_dic(path=None, language=''):
	if not path and language:
		path = os.path.dirname(os.path.abspath(__file__))
		if not language == 'Windows':
			path = path +'/locale/{0}'.format(language)
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
		if not language == 'Windows':
			path = path +'/locale/{0}'.format(language)
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

					role = []
					for i in line[2].split(','):
						i = i.strip()
						role.append(i)

					mathrule[line[0]] = MathRule(line[0], '', '', rule, role)
			except BaseException as e:
				pass

		for line in math_example:
			try:
				line = line.split('\t')
				if len(line) == 2:
					mathrule[line[0]].example = line[1].strip()
			except BaseException as e:
				pass

	return mathrule

def save_unicode_dic(symbol,path=None, language=''):
	if not path and language:
		path = os.path.dirname(os.path.abspath(__file__))
		if not language == 'Windows':
			path = path +'/locale/{0}'.format(language)
		path = os.path.join(path, 'unicode_user.dic')

	with io.open(path, 'w', encoding='utf-8') as f:
		f.write(u'symbols:\r\n')
		key = symbol.keys()
		#key.sort()
		for k in key:
			line = '\t'.join([k, symbol[k], 'none']) +'\r\n'
			f.write(line)

	return True

def save_math_rule(mathrule, path=None, language=''):
	if not path and language:
		path = os.path.dirname(os.path.abspath(__file__))
		if not language == 'Windows':
			path = path +'/locale/{0}'.format(language)
		path = os.path.join(path, 'math_user.rule')

	mathrule_unicode = {}
	for k,v in mathrule.items():
		so_line = [unicode(i) if not isinstance(i, tuple) else '(' +'.'.join(i) +')' for i in v.serialized_order]
		so_line = ', '.join(so_line)
		role_line = ', '.join(v.role)
		mathrule_unicode[k] ='\t'.join([so_line, role_line])

	with io.open(path, 'w', encoding='utf-8') as f:
		key = mathrule.keys()
		key.sort()
		for k in key:
			line = '\t'.join([k, mathrule_unicode[k]]) +'\r\n'
			f.write(line)

	return True

def symbol_translate(u):
	return symbol[u] if symbol.has_key(u) else u

def config_from_environ():
	global language, AMM
	global symbol, mathrule
	language = os.environ.get('LANGUAGE', 'Windows')
	symbol = load_unicode_dic(language=language)
	mathrule = load_math_rule(language=language)
	AMM = True if os.environ.get('AMM', 'True') in [u'True', u'true'] else False

	global nodetypes_check, SNT_check
	nodetypes_check = SNT_check = []
	for i in nodetypes:
		if os.environ.get(i.__name__, 'True') in [u'True', u'true']:
			nodetypes_check.append(globals()[i.__name__])
	for i in SNT:
		if os.environ.get(i.__name__, 'True') in [u'True', u'true']:
			SNT_check.append(globals()[i.__name__])
	if not AMM:
		nodetypes_check = SNT_check = []

import inspect
# get class which is Node subclass
nodes = { i.__name__: i for i in locals().values() if inspect.isclass(i) and issubclass(i, Node) }

# get class which is NodeType subclass
nodetypes = [ i for i in locals().values() if inspect.isclass(i) and issubclass(i, NodeType) ]
nodetypes_dict = { k:v for k,v in locals().items() if inspect.isclass(v) and issubclass(v, NodeType) }
SNT = [ i for i in locals().values() if inspect.isclass(i) and issubclass(i, SiblingNodeType) ]

def ComplementMethod(method):
	def decorator(cls, obj):
		return not method(obj)
	return decorator

notnodetypes = []
notnodetypes_dict = {}
for nodetype in nodetypes:
	dic = dict(nodetype.__dict__)
	dic.update({
		'check': classmethod(ComplementMethod(nodetype.check)),
		'name': '',
	})
	notnodetype = type('Not'+nodetype.__name__, nodetype.__bases__, dic)
	notnodetypes.append(notnodetype)
	notnodetypes_dict.update({
		'Not'+nodetype.__name__: notnodetype,
	})
	locals()['Not'+nodetype.__name__]= notnodetype

nodetypes_dict.update({'object': object})
all_nodetypes = [ i for i in locals().values() if inspect.isclass(i) and issubclass(i, NodeType) ]
all_nodetypes_dict = { k:v for k,v in locals().items() if inspect.isclass(v) and issubclass(v, NodeType) }
all_nodetypes_dict.update({'object': object})

mathrule_info = {
	"generics": {
		"node": [3, 1, "*",],
		"math": [3, 1, "*",],
	},
	"fraction": {
		"mfrac": [5, 2, ".",],
		"single_fraction": [5, 2, ".",],
		"AddIntegerFractionType": [5, 2, ".",],
	},
	"fenced": {
		"mfenced": [3, 1, "*",],
		"set": [3, 1, "*",],
		"absolute_value": [3, 1, "*",],
		"determinant": [3, 1, "*",],
		"matrix": [3, 1, "*",],
	},
	"root": {
		"msqrt": [3, 1, "*",],
		"mroot": [5, 2, ".",],
		"single_square_root": [3, 1, ".",],
	},
	"position": {
		"msubsup": [7, 3, ".",],
		"msup": [5, 2, ".",],
		"msub": [5, 2, ".",],
		"munderover": [7, 3, ".",],
		"munder": [5, 2, ".",],
		"mover": [5, 2, ".",],
		"SingleMsubsup": [7, 3, ".",],
		"SingleMsub": [5, 2, ".",],
		"SingleMsup": [5, 2, ".",],
		"SingleMunderover": [7, 3, ".",],
		"SingleMunder": [5, 2, ".",],
		"SingleMover": [5, 2, ".",],
	},
	"power": {
		"power": [5, 2, ".",],
		"SquarePowerType": [3, 2, ".",],
		"CubePowerType": [3, 2, ".",],
	},
	"from to": {
		"from_to": [7, 3, ".",],
		"from": [5, 2, ".",],
		"to": [5, 2, ".",],
	},
	"table": {
		"mtable": [3, 1, "*",],
		"mtr": [3, 1, "*",],
		"mtd": [3, 1, "*",],
	},
	"line": {
		"LineType": [3, 2, ".",],
		"RayType": [3, 2, ".",],
		"LineSegmentType": [3, 2, ".",],
		"VectorSingleType": [3, 2, ".",],
		"VectorDoubleType": [3, 2, ".",],
		"FrownType": [3, 2, ".",],
	},
	"other": {
		"NegativeSignType": [1, 1, ".",],
		"PositiveSignType": [1, 1, ".",],
		"mmultiscripts": [0, 0, ".",],
		"mprescripts": [0, 0, ".",],
		"none": [0, 0, ".",],
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
	],
	"fenced": [
		"mfenced",
		"set",
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
		"FrownType",
	],
	"other": [
		"NegativeSignType",
		"PositiveSignType",
		"mmultiscripts",
		"mprescripts",
		"none",
	],
}

config_from_environ()

def mathrule_validate(mathrule, validator):
	if not len(mathrule.serialized_order) == validator[0]:
		return False
	if not len(mathrule.role) == validator[1]:
		return False
	if validator[2] == ".":
		for index in range(len(mathrule.serialized_order)):
			if index%2 == 0:
				if not isinstance(mathrule.serialized_order[index], unicode):
					return False
			else:
				if not isinstance(mathrule.serialized_order[index], int):
					return False
	elif validator[2] == "*":
		if not isinstance(mathrule.serialized_order[0], unicode):
			return False
		elif not isinstance(mathrule.serialized_order[1], tuple):
			return False
		elif not isinstance(mathrule.serialized_order[2], unicode):
			return False
	else:
		pass
	return True

for category_key in mathrule_category_order:
	category = mathrule_order[category_key]
	for item in category:
		if not mathrule_validate(mathrule[item], mathrule_info[category_key][item]):
			pass
