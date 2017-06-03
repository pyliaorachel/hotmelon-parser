import sys
import os
from thesis_parsing import Splitter, Extracter, Thesis, Chapter, Section

class Parser(object):
	def __init__(self, filename):
		self.filename = filename
		self.base_path = os.path.dirname(os.path.realpath(filename))
		self.graphic_paths = [self.base_path]

	def parse_sections(self, raw_text, level=0, max_level=2):
		if level > max_level:
			return

		section_list = []

		content, sections = Splitter.split_sections(raw_text, level=level)
		graphic_paths = Extracter.extract_graphic_paths(content)
		self.graphic_paths = graphic_paths if graphic_paths else self.graphic_paths # update current graphic paths

		for section in sections:
			section_title = Extracter.extract_title(section)
			section_data = Section(title=section_title)
			if level + 1 <= max_level:
				section_data['content'], section_data['figures'], section_data['subsections'] = self.parse_sections(section, level=level+1, max_level=max_level)		

			section_list.append(section_data)

		return (Extracter.clean_content(content), Extracter.extract_figures(content, self.graphic_paths, self.base_path), section_list)

	def parse_chapters(self, raw_text):
		chapter_list = []

		chapters = Splitter.split_chapters(raw_text)
		for chapter in chapters:
			chapter_title = Extracter.extract_title(chapter)
			chapter_data = Chapter(title=chapter_title)
			chapter_data['content'], chapter_data['figures'], chapter_data['sections'] = self.parse_sections(chapter)

			chapter_list.append(chapter_data)

		return chapter_list

	def parse_thesis(self):
		with open(self.filename, 'r') as f:
			thesis_raw = f.read()

		thesis_title = Extracter.extract_thesis_title(thesis_raw)
		thesis = Thesis(title=thesis_title)
		
		thesis['chapters'] = self.parse_chapters(thesis_raw)
		thesis['authors'] = Extracter.extract_authors(thesis_raw)
		thesis['abstract'] = Extracter.extract_abstract(thesis_raw)
		thesis['date'] = Extracter.extract_date(thesis_raw)
		thesis['subtitle'] = Extracter.extract_subtitle(thesis_raw)

		return thesis





