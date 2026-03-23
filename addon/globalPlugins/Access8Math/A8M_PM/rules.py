import collections
import csv
from csv import DictReader
from dataclasses import dataclass
import os
import re
import shutil

from lib.dataProcess import joinObjectArray
LOCALE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "locale")


def NVDASymbolsFetch(language):
	from characterProcessing import _getSpeechSymbolsForLocale

	builtin_dict = {}
	user_dict = {}
	builtin, user = _getSpeechSymbolsForLocale(language)
	for value in builtin.symbols.values():
		if not value.identifier.isspace() and " " not in value.identifier:
			builtin_dict[value.identifier] = value.replacement
	for value in user.symbols.values():
		if not value.identifier.isspace() and " " not in value.identifier:
			user_dict[value.identifier] = value.replacement
	return builtin_dict, user_dict


@dataclass
class MathRule(object):
	name: str
	description: str
	category: str
	serialized_order: list
	role: list
	example: str


def exist_language(language):
	return os.path.exists(os.path.join(LOCALE_DIR, language))


def add_language(language):
	try:
		src_language = language.split("_")[0]
	except IndexError:
		src_language = "en"

	src = os.path.join(LOCALE_DIR, src_language)
	if not os.path.exists(src):
		src = os.path.join(LOCALE_DIR, "en")
	dst = os.path.join(LOCALE_DIR, language)
	try:
		shutil.copytree(src, dst, ignore=shutil.ignore_patterns("*_user.*"))
	except FileExistsError:
		pass


def remove_language(language):
	try:
		dst = os.path.join(LOCALE_DIR, language)
		shutil.rmtree(dst)
	except BaseException:
		return False
	return True


def export_language(language, dst):
	def ignore_patterns(patterns, filenames):
		return [filename for filename in filenames for pattern in patterns if pattern in filename]

	patterns = ["math.rule", "unicode.dic"]
	src = os.path.join(LOCALE_DIR, language)
	temp = os.path.join(LOCALE_DIR, "export")

	try:
		shutil.rmtree(temp)
	except BaseException:
		pass

	shutil.copytree(src, temp, ignore=lambda directory, contents: ignore_patterns(patterns, contents))
	for dirPath, dirNames, fileNames in os.walk(temp):
		for item in fileNames:
			item = os.path.join(dirPath, item)
			if "_user." in item:
				os.rename(item, item.replace("_user.", "."))

	try:
		shutil.make_archive(dst, "zip", temp)
	except BaseException:
		return False
	finally:
		shutil.rmtree(temp)

	return True


def available_languages():
	path = os.path.join(LOCALE_DIR)
	return [item for item in os.listdir(path) if os.path.isdir(os.path.join(path, item))]


def clean_user_data():
	for dirPath, dirNames, fileNames in os.walk(LOCALE_DIR):
		for item in fileNames:
			item = os.path.join(dirPath, item)
			try:
				if os.path.isfile(item) and ("_user.dic" in item or "_user.rule" in item):
					os.remove(item)
			except BaseException:
				pass


def load_unicode_dic(path=None, language="", category="speech", NVDASymbol=False):
	symbol = {}

	if not path and language:
		path = os.path.join(LOCALE_DIR, language, category)
		if not os.path.exists(path):
			raise OSError(f"{language} i18n file is not found")

		if category == "speech" and NVDASymbol:
			try:
				builtin, user = NVDASymbolsFetch(language)
			except BaseException:
				builtin, user = {}, {}
			symbol = {**builtin, **user}

		frp = os.path.join(path, "unicode.dic")
		frp_user = os.path.join(path, "unicode_user.dic")
		if not os.path.exists(frp_user):
			shutil.copyfile(frp, frp_user)

		path = frp_user

	with open(path, "r", encoding="utf-8") as fr:
		reader = csv.reader(fr, delimiter="\t")
		for row in reader:
			if len(row) >= 2:
				try:
					symbol[row[0]] = row[1].split(",")[0].strip()
				except BaseException:
					pass

	return symbol


def load_math_rule(path=None, language="", category="speech"):
	meta_path = os.path.join(LOCALE_DIR, "rule.csv")

	if not path and language:
		path = os.path.join(LOCALE_DIR, language, category)
		if not os.path.exists(path):
			raise OSError(f"{language} i18n file is not found")

		frp = os.path.join(path, "math.rule")
		frp_user = os.path.join(path, "math_user.rule")
		if not os.path.exists(frp_user):
			shutil.copyfile(frp, frp_user)
		path = frp_user

	mathrule = collections.OrderedDict({})

	with open(path, "r", encoding="utf-8") as rule_file, open(meta_path, "r", encoding="utf-8") as meta_file:
		meta_dict_csv = DictReader(meta_file, delimiter="\t")
		meta = []
		for item in meta_dict_csv:
			meta.append(item)

		rule_dict_csv = DictReader(rule_file, delimiter="\t")
		rule = []
		for item in rule_dict_csv:
			rule.append(item)

		rows = joinObjectArray(meta, rule, "name")
		rows = [{**item, **{"order": int(item["order"])}} for item in rows]
		rows = sorted(rows, key=lambda row: row["order"])

		for line in rows:
			try:
				if len(line) == 7:
					rule = []
					for item in line["rule"].split(","):
						item = item.strip()
						tuple_pattern = re.compile(r"\((.*)\.(.*)\)")
						match = tuple_pattern.search(item)
						if match:
							item = (match.group(1), match.group(2))

						try:
							rule.append(int(item))
						except BaseException:
							rule.append(item)

					role = []
					for item in line["role"].split(","):
						item = item.strip()
						role.append(item)

					mathrule[line["name"]] = MathRule(
						line["name"],
						line["description"].strip(),
						"",
						rule,
						role,
						line["mathml"],
					)
			except BaseException:
				pass

	return collections.OrderedDict({key: value for key, value in mathrule.items() if value})


def save_unicode_dic(symbol, path=None, language="", category="speech"):
	if not path and language:
		path = os.path.join(LOCALE_DIR, language, category)
		path = os.path.join(path, "unicode_user.dic")

	with open(path, "w", encoding="utf-8", newline="") as file:
		writer = csv.writer(file, delimiter="\t")
		for key in sorted(symbol.keys()):
			writer.writerow([key, symbol[key]])

	return True


def save_math_rule(mathrule, path=None, language="", category="speech"):
	if not path and language:
		path = os.path.join(LOCALE_DIR, language, category)
		path = os.path.join(path, "math_user.rule")

	mathrule_unicode = {}
	for key, value in mathrule.items():
		try:
			serialized_order = [
				str(item) if not isinstance(item, tuple) else "(" + ".".join(item) + ")"
				for item in value.serialized_order
			]
			mathrule_unicode[key] = [
				", ".join(serialized_order),
				", ".join(value.role),
				value.description,
			]
		except BaseException:
			pass

	with open(path, "w", encoding="utf-8", newline="") as file:
		writer = csv.writer(file, delimiter="\t")
		for key in sorted(mathrule.keys()):
			try:
				writer.writerow([key, *mathrule_unicode[key]])
			except BaseException:
				pass

	return True


__all__ = [
	"NVDASymbolsFetch",
	"MathRule",
	"LOCALE_DIR",
	"exist_language",
	"add_language",
	"remove_language",
	"export_language",
	"available_languages",
	"clean_user_data",
	"load_unicode_dic",
	"load_math_rule",
	"save_unicode_dic",
	"save_math_rule",
]
