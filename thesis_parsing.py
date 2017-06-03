import re

class SplitterConst:
	CHAPTER = '\\chapter'
	SECTION = '\\_section'

class RegPatternConst:
	THESIS_TITLE = r'\\title(\[.*\])?{(?P<title>.*)}'
	FIRST_PAREN = r'^(\[.*\])?{(?P<content>.*)}'
	AUTHOR = r'\\author(\[.*\])?{(?P<author>.*)}'
	ABSTRACT = r'\\begin{abstract}\n*(?P<abstract>.*)\n*\\end{abstract}'
	DATE = r'\\degreedate(\[.*\])?{(?P<date>.*)}'
	SUBTITLE = r'\\subtitle(\[.*\])?{(?P<subtitle>.*)}'
	INNER_COMMANDS = r'\\[^{}]+(\[.*\])?{[^{}]*}{(?P<content>[^{}]*)}'

class Splitter:
	def split_chapters(text):
		return text.split(SplitterConst.CHAPTER)[1:]

	def split_sections(text, level=0):
		split_txt = SplitterConst.SECTION.replace('_', 'sub' * level)
		return text.split(split_txt)[1:]

class Extracter:
	def remove_inner_commands(text):
		inner_cmd = re.search(RegPatternConst.INNER_COMMANDS, text)
		while inner_cmd:
			txt = inner_cmd.group(0)
			content = inner_cmd.group('content')
			text = text.replace(txt, content, 1)

			inner_cmd = re.search(RegPatternConst.INNER_COMMANDS, text)

		return text

	def extract_title(text):
		"""{title} at the first line"""
		match = re.search(RegPatternConst.FIRST_PAREN, text)
		return Extracter.remove_inner_commands(match.group('content')) if match else ''

	def extract_thesis_title(text):
		"""\title{title} anywhere in text"""
		match = re.search(RegPatternConst.THESIS_TITLE, text)
		return Extracter.remove_inner_commands(match.group('title')) if match else ''

	def extract_authors(text):
		"""\author[*]{author}"""
		match = re.finditer(RegPatternConst.AUTHOR, text)
		authors = list(map(lambda m: m.group('author'), match))
		return authors

	def extract_abstract(text):
		"""\begin{abstract}...\end{abstract}"""
		match = re.search(RegPatternConst.ABSTRACT, text)
		return Extracter.remove_inner_commands(match.group('abstract')) if match else ''

	def extract_date(text):
		"""\degreedate{date}"""
		match = re.search(RegPatternConst.DATE, text)
		return Extracter.remove_inner_commands(match.group('date')) if match else ''

	def extract_subtitle(text):
		"""\subtitle{subtitle}"""
		match = re.search(RegPatternConst.SUBTITLE, text)
		return Extracter.remove_inner_commands(match.group('subtitle')) if match else ''

class Thesis(dict):
	def __init__(self, title='', subtitle='', abstraction='', conclusion='', date=''):
		self['title'] = title
		self['subtitle'] = subtitle
		self['chapters'] = []
		self['authors'] = []
		self['abstraction'] = abstraction
		self['conclusion'] = conclusion
		self['date'] = date
		self['reference'] = None

class Chapter(dict):
	def __init__(self, title=''):
		self['title'] = title
		self['sections'] = []

class Section(dict):
	def __init__(self, title=''):
		self['title'] = title
		self['keywords'] = []
		self['subsections'] = []
		self['figures'] = []
		self['tables'] = []







