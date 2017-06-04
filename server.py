from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os
from hot_melon import parse_thesis

PORT = int(os.getenv('PORT', 8000))
DEFAULT_ZIP_FILE_PATH = 'thesis.zip'
DEFAULT_OUTPUT_FOLDER_PATH = './thesis'

def get_file_ext(filename):
	return filename.split('.')[-1]

def process_new_thesis(filepath):
	import zipfile
	zip_ref = zipfile.ZipFile(filepath, 'r')
	zip_ref.extractall(DEFAULT_OUTPUT_FOLDER_PATH)
	zip_ref.close()

	# walk folder to find .tex file
	current_base_path = os.path.dirname(os.path.realpath(__file__))
	thesis_file = ''
	for root, dirs, files in os.walk(os.path.join(current_base_path, DEFAULT_OUTPUT_FOLDER_PATH)):
		for filename in files:
			if get_file_ext(filename) == 'tex' and not filename.startswith('.'):
				thesis_file = os.path.join(root, filename)
				break

		if thesis_file != '':
			break

	thesis_file = os.path.relpath(thesis_file)
	
	# parse thesis
	key = parse_thesis(thesis_file)
	return key


class HTTPServer_RequestHandler(BaseHTTPRequestHandler):

	def do_POST(self):
		path = urllib.parse.urlparse(self.path).path

		if path == '/thesis':
			data = self.rfile.read(int(self.headers['Content-Length']))

			with open(DEFAULT_ZIP_FILE_PATH, 'wb') as outfile:
				outfile.write(data)

			key = process_new_thesis(DEFAULT_ZIP_FILE_PATH)

			self.send_response(200)

			self.send_header('Content-type','text/plain')
			self.send_header('Access-Control-Allow-Origin', '*')
			self.end_headers()

			self.wfile.write(bytes(key, 'utf8'))

	def do_GET(self):
		self.send_response(200)

		self.send_header('Content-type','text/plain')
		self.end_headers()

		message = 'Hello world!'
		self.wfile.write(bytes(message, 'utf8'))

	def do_OPTIONS(self):
		self.send_response(200)

		self.send_header('Access-Control-Allow-Origin', self.headers['Origin'])
		self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
		self.end_headers()
 
def run():
	print('starting server...')

	server_address = ('', PORT)
	httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
	print('running server...')
	httpd.serve_forever()

if __name__ == '__main__':
	run()