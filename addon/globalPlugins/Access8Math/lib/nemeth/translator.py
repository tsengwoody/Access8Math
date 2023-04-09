from lark import Lark

from .grammar import grammar
from .transformer import Nemeth2TexTransformer


class Nemeth2LaTeXTranslator:
	def __init__(self, lexer="contextual", parser="lalr", **kwargs):
		self.transformer = Nemeth2TexTransformer()
		self.parser = Lark(grammar, start='start', lexer='basic')
		# self.parser = Lark(grammar, parser=parser, lexer=lexer)

	def translate(self, data):
		return self.transformer.transform(self.parser.parse(data))
