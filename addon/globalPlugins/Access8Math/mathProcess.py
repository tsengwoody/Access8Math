import html
import re
import sys

from latex2mathml import converter

def latex2mathml(latex):
	mathml = converter.convert(latex)
	mathml = html.unescape(mathml)
	return mathml

def textmath2laObj(input):
	reTexMath = re.compile(r"\\\(.*?\\\)")
	text = reTexMath.split(input)
	math = reTexMath.findall(input)
	length = len(math)
	datas = []

	for i in range(length):
		raw = text[i].replace('\r\n', '\n').replace('\\', '\\\\').strip('\n')
		if raw != '':
			datas.append({
				'type': 'text-content',
				'data': raw,
			})
		raw = math[i][2: len(math[i])-2].replace('\\', '\\\\')
		datas.append({
			'type': 'latex-content',
			'data': raw,
		})

	raw = text[length].replace('\n', '').replace('\\', '\\\\').strip('\n')
	if raw != '':
		datas.append({
			'type': 'text-content',
				'data': raw,
		})

	return datas

def laObj2mathObj(input):
	result = []
	for item in input:
		if item['type'] == 'latex-content':
			result.append({
				'type': 'math-content',
				'data': latex2mathml(item['data']),
			})
		else:
			result.append({
				'type': item['type'],
				'data': item['data'],
			})

	return result

def obj2html(data):
	content = ''
	result = ''
	htmls = []
	for item in data:
		result = ''
		if item['type'] == 'text-content':
			temp = ''
			for index, line in enumerate(item['data'].split("\n")):
				if index != 0:
					temp += '<br />'
				temp += '{}'.format(line)
			result = '{}'.format(temp)
			content += result
			htmls.append(result)
		elif item['type'] == 'math-content':
			result = '<div>{}</div>'.format(item['data'])
			content += result
			htmls.append(result)

	return {
		"content": content,
		"htmls": htmls,
	}

if __name__ == '__main__':
	i = '一元二次方程式\(ax^2+bx+c=0\)的解為'
	result = textmath2laObj(i)
	print(result)
