from xml.etree import ElementTree as ET

import html
import re

from .nodes import (
	AlterNode,
	BlockNode,
	Mphantom,
	Mrow,
	Nones,
	NonTerminalNode,
	TerminalNode,
	nodes,
)


def includes_unicode_range(string, lower, high):
	for char in string:
		if ord(char) < high and ord(char) >= lower:
			return True
	return False


def mathml2etree(mathml):
	gtlt_pattern = re.compile(r"([\>])(.*?)([\<])")
	mathml = gtlt_pattern.sub(
		lambda match: match.group(1) + html.escape(html.unescape(match.group(2))) + match.group(3),
		mathml,
	)

	quote_pattern = re.compile(r"=([\"\'])(.*?)\1")
	mathml = quote_pattern.sub(
		lambda match: "=" + match.group(1) + html.escape(match.group(2)) + match.group(1),
		mathml,
	)

	parser = ET.XMLParser()

	try:
		return ET.fromstring(mathml.encode("utf-8"), parser=parser)
	except BaseException as error:
		raise SystemError(error)


def create_node(et):
	pattern = re.compile(r"[\{].*[\}](?P<mp_type>.+)")
	match = pattern.search(et.tag)
	try:
		mp_tag = match.group("mp_type")
	except BaseException:
		mp_tag = et.tag

	node_class = nodes[mp_tag.capitalize()] if mp_tag.capitalize() in nodes else object
	if mp_tag == "none":
		node_class = Nones

	if issubclass(node_class, (NonTerminalNode, BlockNode)):
		child = [create_node(child) for child in et]
		return node_class(child, et.attrib)
	if issubclass(node_class, TerminalNode):
		return node_class([], et.attrib, data=et.text)
	if mp_tag == "none":
		return Nones()

	child = [create_node(child) for child in et]
	return Mrow(child, et.attrib)


def clean_allnode(node):
	for child in node.child:
		clean_allnode(child)

	if isinstance(node, Mphantom):
		parent_new_child = node.parent.child[0:node.index_in_parent()]
		if node.index_in_parent() + 1 < len(node.parent.child):
			parent_new_child = parent_new_child + node.parent.child[node.index_in_parent() + 1:]
		node.parent.child = parent_new_child
		return node

	if node.parent and isinstance(node, BlockNode):
		if len(node.child) == 1 or (isinstance(node.parent, AlterNode) and len(node.child) > 0):
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

	return node


def set_mathcontent_allnode(node, mathcontent):
	for child in node.child:
		set_mathcontent_allnode(child, mathcontent)
	node.mathcontent = mathcontent
	if node.type:
		node.type.mathcontent = mathcontent
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


__all__ = [
	"includes_unicode_range",
	"mathml2etree",
	"create_node",
	"clean_allnode",
	"set_mathcontent_allnode",
	"set_mathrule_allnode",
	"set_braillemathrule_allnode",
	"clear_type_allnode",
	"check_type_allnode",
	"check_in_allnode",
]
