import re

class SplitterConst(object):
	CHAPTER = '\\chapter'
	SECTION = '\\section'
	SUBSECTION = '\\subsection'
	SUBSUBSECTION = '\\subsubsection'

class RegPatternConst(object):
	TITLE = r'\\title{.*}'
	SECTION = r'\\section{.*}'

class Splitter(object):
	def split_chapters(text):
		return text.split(SplitterConst.CHAPTER)[1:]

	def split_sections(chapter):
		return chapter.split(SplitterConst.SECTION)[1:]

	def split_subsections(section):
		return section.split(SplitterConst.SUBSECTION)[1:]

	def split_subsubsections(section):
		return section.split(SplitterConst.SUBSUBSECTION)[1:]

class Extracter(object):
	def extract_title(text):
		"""{title} at the first line"""
		title = re.findall(r'^{(.*)}', text)
		return title[0] if len(title) > 0 else None

class Thesis(dict):
	def __init__(self, title='', subtitle='', abstraction='', conclusion='', date=''):
		self['title'] = title
		self['subtitle'] = subtitle
		self['chapters'] = []
		self['author'] = []
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







