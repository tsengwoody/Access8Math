import io
import json
import os
import re
import shutil
import uuid
from html.parser import HTMLParser
from zipfile import ZipFile

import addonHandler
import config

addonHandler.initTranslation()

PATH = os.path.dirname(os.path.dirname(__file__))
TEMPLATES_PATH = os.path.join(PATH, 'web', 'templates')
CONTENT_CONFIG_PLACEHOLDER = "__CONTEXT__"

import markdown2

from ..command.action import batch


class _ResourceHTMLParser(HTMLParser):
	def __init__(self):
		super().__init__()
		self.resources = []

	def handle_starttag(self, tag, attrs):
		attrs = dict(attrs)
		if tag == "a" and "href" in attrs:
			self.resources.append('\\'.join(attrs["href"].split('/')))
		elif tag == "img" and "src" in attrs:
			self.resources.append('\\'.join(attrs["src"].split('/')))


def _load_json(path):
	with open(path, encoding="utf8") as f:
		return json.load(f)


class Access8MathDocument:
	def __init__(self, path=None, exist=True):
		# path: folder/txt/zip
		self.temp = False
		if path and not os.path.exists(path):
			if not exist:
				raise OSError("path {} not exist".format(path))
			else:
				with open(path, 'w', encoding='utf8') as f:
					f.write("")
		if not path:
			path = os.path.join(PATH, 'web', 'workspace', str(uuid.uuid4()))
			self.temp = True
			os.makedirs(path)
			raw_entry = os.path.join(path, '{}.txt'.format(_("New document")))
			with open(raw_entry, 'w', encoding='utf8') as f:
				f.write("")
			metadata_file = os.path.join(path, 'Access8Math.json')
			metadata = {
				"entry": os.path.basename(raw_entry),
				"title": "Access8Math",
			}
			dst = os.path.join(path, 'Access8Math.json')
			with open(dst, 'w', encoding='utf8') as f:
				json.dump(metadata, f)

		if os.path.isdir(path):
			self._raw_folder = path
			metadata_file = os.path.join(path, 'Access8Math.json')
			metadata = _load_json(metadata_file)
		elif os.path.isfile(path):
			file = os.path.basename(path)
			ext = file.split('.')[-1]
			if ext == 'zip' or ext == 'a8m':
				self._raw_folder = os.path.join(PATH, 'web', 'workspace', str(uuid.uuid4()))
				self.temp = True
				if not os.path.exists(self.raw_folder):
					os.makedirs(self.raw_folder)
				with ZipFile(path, 'r') as file:
					file.extractall(self.raw_folder)
				metadata_file = os.path.join(self.raw_folder, 'Access8Math.json')
				metadata = _load_json(metadata_file)
			else:
				metadata_file = os.path.join(path, 'Access8Math.json')
				metadata = {
					"entry": os.path.basename(path),
					"title": "Access8Math",
				}
				dst = os.path.join(os.path.dirname(path), 'Access8Math.json')
				with open(dst, 'w', encoding='utf8') as f:
					json.dump(metadata, f)
				self._raw_folder = os.path.dirname(path)

		self.metadata = metadata
		self.raw_entry = metadata["entry"]
		self._title = metadata["title"]

		self.a8m_folder = os.path.join(PATH, 'web', 'workspace', 'a8m')
		self.review_folder = os.path.join(PATH, 'web', 'workspace', 'review')

	def __del__(self):
		if self.temp:
			try:
				shutil.rmtree(self.raw_folder)
			except BaseException:
				pass

	@property
	def raw_folder(self):
		return self._raw_folder

	@raw_folder.setter
	def raw_folder(self, path):
		if self.raw_folder == path:
			return
		rawIntoReview(self.raw_folder, path, self.resources)

		shutil.copyfile(
			os.path.join(self.raw_folder, self.raw_entry),
			os.path.join(path, self.raw_entry),
		)
		shutil.copyfile(
			os.path.join(self.raw_folder, 'Access8Math.json'),
			os.path.join(path, 'Access8Math.json'),
		)

		shutil.rmtree(self._raw_folder)

		self._raw_folder = path
		self.temp = False

	@property
	def review_entry(self):
		return os.path.join(self.review_folder, f"index.html")

	@property
	def resources(self):
		with io.open(os.path.join(self.raw_folder, self.raw_entry), 'r', encoding='utf8') as f:
			content = f.read()
		contentmd = markdown2.markdown(content)
		parser = _ResourceHTMLParser()
		try:
			parser.feed(contentmd)
			parser.close()
		except BaseException:
			return []
		return parser.resources

	@property
	def title(self):
		return self._title

	@title.setter
	def title(self, value):
		self._title = value
		# update metadata value
		path = self.raw_folder
		metadata_file = os.path.join(path, 'Access8Math.json')
		metadata = _load_json(metadata_file)
		metadata.update({
			"title": value,
		})
		with open(metadata_file, 'w', encoding='utf8') as f:
			json.dump(metadata, f)

	@property
	def document_color(self):
		return self.metadata.get(
			"documentColor",
			config.conf["Access8Math"]["settings"].get("HTML_color_scheme", "light"),
		)

	def rename(self, src, dst):
		_src = os.path.join(self.raw_folder, src)
		_dst = os.path.join(self.raw_folder, dst)
		if os.path.isfile(_src):
			os.rename(_src, _dst)
		else:
			raise OSError("src path is not file")
		if src == self.raw_entry:
			self.raw_entry = dst
			# update metadata value
			path = self.raw_folder
			raw_entry = self.raw_entry
			metadata_file = os.path.join(path, 'Access8Math.json')
			metadata = _load_json(metadata_file)
			metadata.update({
				"entry": raw_entry,
			})
			with open(metadata_file, 'w', encoding='utf8') as f:
				json.dump(metadata, f)

	def raw2a8m(self):
		try:
			shutil.rmtree(self.a8m_folder)
		except BaseException:
			pass

		shutil.copytree(self.raw_folder, self.a8m_folder)

		# update metadata value
		metadata_file = os.path.join(self.a8m_folder, 'Access8Math.json')
		metadata = _load_json(metadata_file)
		metadata.update({
			"title": self.title,
			"entry": self.raw_entry,
			"latexDelimiter": config.conf["Access8Math"]["settings"]["LaTeX_delimiter"],
			"documentColor": self.document_color,
		})
		with open(metadata_file, 'w', encoding='utf8') as f:
			json.dump(metadata, f)

	def raw2review(self):
		try:
			shutil.rmtree(self.review_folder)
		except BaseException:
			pass
		try:
			os.makedirs(self.review_folder)
		except BaseException:
			pass

		rawIntoReview(self.raw_folder, self.review_folder, self.resources)

		shutil.copyfile(
			os.path.join(self.raw_folder, self.raw_entry),
			os.path.join(self.review_folder, self.raw_entry),
		)

		template_folder = os.path.join(PATH, 'web', 'templates')

		for dirPath, dirNames, fileNames in os.walk(self.review_folder):
			for item in fileNames:
				item = os.path.join(dirPath, item)
				try:
					name = '.'.join(os.path.basename(item).split('.')[:-1])
					extend = os.path.basename(item).split('.')[-1]
				except BaseException:
					name = ''
					extend = ''
				if os.path.isfile(item) and (extend in ['txt', 'md'] or os.path.basename(item) == self.raw_entry):
					if os.path.basename(item) == self.raw_entry:
						text2template(
							src=item,
							dst=os.path.join(os.path.dirname(item), "content-config.js"),
							title=self.title,
							document_color=self.document_color,
						)
						os.remove(item)
					else:
						text2template(
							src=item,
							dst=os.path.join(os.path.dirname(item), f'{name}.js'),
							document_color=self.document_color,
						)
						os.remove(item)

		with ZipFile(os.path.join(template_folder, "Access8MathTemplate.zip"), "r") as zip_file:
			zip_file.extractall(self.review_folder)


def rawIntoReview(raw_folder, review_folder, resources):
	for resource in resources:
		try:
			dir = os.path.dirname(os.path.join(review_folder, resource))
			if not os.path.exists(dir):
				os.makedirs(dir)
			shutil.copyfile(
				os.path.join(raw_folder, resource),
				os.path.join(review_folder, resource),
			)
		except BaseException:
			pass


def text2template(src, dst, title=None, document_color="light"):
	with open(src, "r", encoding="utf8") as f:
		value = f.read()
		value = batch("nemeth2latex")(value)

	decimal_pattern = re.compile(r"&#([\d]+);")
	value = decimal_pattern.sub(lambda m: chr(int(m.group(1))), value)

	hexadecimal_pattern = re.compile(r"&#x([\dABCDEFabcdef]+);")
	value = hexadecimal_pattern.sub(lambda m: chr(int(m.group(1), 16)), value)

	if not title:
		try:
			name = os.path.basename(src).split('.')
			if len(name) > 1:
				name = name[:-1]
			title = '.'.join(name)
		except BaseException:
			title = 'Access8Math'

	content_config = {
		"title": title,
		"sourceText": value,
		"latexDelimiter": config.conf["Access8Math"]["settings"]["LaTeX_delimiter"],
		"documentColor": document_color,
	}
	with open(os.path.join(TEMPLATES_PATH, "index.template"), "r", encoding="utf8") as f:
		template = f.read()
	content = template.replace(
		CONTENT_CONFIG_PLACEHOLDER,
		json.dumps(content_config, ensure_ascii=False),
	)
	with open(dst, "w", encoding="utf8", newline="") as f:
		f.write(content)
	return dst
