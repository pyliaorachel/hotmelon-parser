import sys
from parser import Parser
import db
import json

def walk_sections(sections, key):
	for section in sections:
		figures = section['figures']
		
		# change image url
		section['figures'] = list(map(lambda f: db.get_image_url(f, key), figures))

		if len(section['subsections']) > 0:
			walk_sections(section['subsections'], key)

def update_image_urls(thesis, key):
	for chapter in thesis['chapters']:
		walk_sections(chapter['sections'], key)

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("Usage: python3 parser.py <path-to-latex-file>")

	else:
		parser = Parser(sys.argv[1])
		thesis = parser.parse_thesis()

		db.put_all_figures(parser.historical_graphic_paths, parser.base_path, parser.key)
		update_image_urls(thesis, parser.key)

		db.put_data(parser.key, thesis)
