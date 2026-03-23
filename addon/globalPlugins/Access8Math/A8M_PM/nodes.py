from . import _core_impl as _core
from .metadata import AUTO_GENERATE, DIC_GENERATE


_NODE_CLASS_PARENT_NAMES = {
	"Node": None,
	"NonTerminalNode": "Node",
	"TerminalNode": "Node",
	"AlterNode": "NonTerminalNode",
	"FixNode": "NonTerminalNode",
	"BlockNode": "AlterNode",
	"Mrow": "BlockNode",
	"Mfrac": "FixNode",
	"Msqrt": "AlterNode",
	"Mroot": "FixNode",
	"Mstyle": "BlockNode",
	"Merror": "AlterNode",
	"Mpadded": "AlterNode",
	"Mphantom": "AlterNode",
	"Mfenced": "AlterNode",
	"Menclose": "AlterNode",
	"Msub": "FixNode",
	"Msup": "FixNode",
	"Msubsup": "FixNode",
	"Munder": "FixNode",
	"Mover": "FixNode",
	"Munderover": "FixNode",
	"Mtable": "AlterNode",
	"Mlabeledtr": "AlterNode",
	"Mtr": "AlterNode",
	"Mtd": "AlterNode",
	"Mstack": "AlterNode",
	"Mlongdiv": "AlterNode",
	"Msgroup": "AlterNode",
	"Msrow": "AlterNode",
	"Mscarries": "AlterNode",
	"Mscarry": "AlterNode",
	"Maction": "AlterNode",
	"Math": "AlterNode",
	"Mi": "TerminalNode",
	"Mn": "TerminalNode",
	"Mo": "TerminalNode",
	"Mtext": "TerminalNode",
	"Mspace": "TerminalNode",
	"Ms": "TerminalNode",
	"Mmultiscripts": "AlterNode",
	"Mprescripts": "TerminalNode",
	"Nones": "TerminalNode",
}


for _name, _parent_name in _NODE_CLASS_PARENT_NAMES.items():
	legacy_class = getattr(_core, _name)
	if _parent_name is None:
		bases = (legacy_class,)
	else:
		bases = (globals()[_parent_name], legacy_class)
	globals()[_name] = type(_name, bases, {})

nodes = {name: globals()[name] for name in _NODE_CLASS_PARENT_NAMES}

def _check_type(self):
	from .semantics import nodetypes_check

	for nodetype in nodetypes_check:
		if nodetype.check(self) and nodetype.name in self.mathrule:
			if not self.type:
				self.type = nodetype()
				self.type.mathcontent = self.mathcontent
				self.type.set_mathrule(self.mathrule)
			elif self.type and issubclass(nodetype, self.type.__class__):
				self.type = nodetype()
				self.type.mathcontent = self.mathcontent
				self.type.set_mathrule(self.mathrule)


Node.check_type = _check_type


__all__ = ["AUTO_GENERATE", "DIC_GENERATE", "nodes", *_NODE_CLASS_PARENT_NAMES.keys()]
