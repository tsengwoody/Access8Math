import csv
import os

from lark import Transformer, Tree

from .utils import nemeth2symbol_with_priority


class Nemeth2TexTransformer(Transformer):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		BASE_DIR = os.path.dirname(__file__)
		data_folder = os.path.join(BASE_DIR, "data")

		data_path = "number.csv"
		map = nemeth2symbol_with_priority(os.path.join(data_folder, data_path))
		self.number = sorted(list(map.items()), key=lambda i: -len(i[0]))

		data_path = "letter.csv"
		map = nemeth2symbol_with_priority(os.path.join(data_folder, data_path))
		self.letter = sorted(list(map.items()), key=lambda i: -len(i[0]))

		data_path = "symbol.csv"
		map = nemeth2symbol_with_priority(os.path.join(data_folder, data_path))
		self.symbol = sorted(list(map.items()), key=lambda i: -len(i[0]))

	def translate(self, string, map):
		for key, value in map:
			string = string.replace(key, value)
		return string

	def exp(self, items):
		join = ""
		for item in items:
			if isinstance(item, str):
				join += item
			else:
				print("not string:", item)
		return join

	def exp_sup(self, items):
		main = items[0]
		if not len(main) == 1:
			main = r"{" + main + r"}"

		comp = items[1]
		if not len(comp) == 1:
			comp = r"{" + comp + r"}"

		return main + r"^" + comp

	def exp_sub(self, items):
		main = items[0]
		if not len(main) == 1:
			main = r"{" + main + r"}"

		comp = items[1]
		if not len(comp) == 1:
			comp = r"{" + comp + r"}"

		return main + r"_" + comp

	def exp_sup_simple(self, items):
		main = items[0]
		if not len(main) == 1:
			main = r"{" + main + r"}"

		comp = items[1]
		if not len(comp) == 1:
			comp = r"{" + comp + r"}"

		return main + r"^" + comp

	def exp_sub_simple(self, items):
		main = items[0]
		if not len(main) == 1:
			main = r"{" + main + r"}"

		comp = items[1]
		if not len(comp) == 1:
			comp = r"{" + comp + r"}"

		return main + r"_" + comp

	def exp_over(self, items):
		return r"\overset{" + items[1] + r"}{" + items[0] + r"}"

	def exp_under(self, items):
		return r"\underset{" + items[1] + r"}{" + items[0] + r"}"

	def exp_frac(self, items):
		return r"\frac{" + items[0] + r"}{" + items[1] + r"}"

	def exp_sqrt(self, items):
		return r"\sqrt{" + items[0] + r"}"

	def exp_root(self, items):
		return r"\sqrt[" + items[0] + r"]{" + items[1] + r"}"

	def exp_interm(self, items):
		return items[0]

	def exp_par(self, items):
		return "".join(items)

	def const(self, items):
		return "".join(items)

	def EN_UPPERCASE(self, items):
		result = self.translate(items.replace("⠠", ""), self.letter).upper()
		return result

	def EN_LOWERCASE(self, items):
		result = self.translate(items, self.letter)
		return result

	def EN_UPPERCASE_CONTINUE(self, items):
		try:
			uppercases, lowercases = items.split("⠠⠄")
		except ValueError:
			uppercases = items
			lowercases = ""
		uppercases = uppercases.strip("⠠")
		result = self.translate(uppercases, self.letter).upper() + self.translate(lowercases, self.letter)
		return result

	def NUMBER(self, items):
		result = self.translate(items.replace("⠼", ""), self.number)
		return result

	def operand(self, items):
		return "".join(items)

	def other(self, items):
		return "".join(items)

	def OPERAND(self, items):
		result = self.translate(items, self.symbol)
		return result

	def OTHER(self, items):
		result = self.translate(items, self.symbol)
		return result
