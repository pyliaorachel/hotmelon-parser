import config
import pyrebase
import os

db_config = {
  'apiKey': os.getenv('FIREBASE_API_KEY', config.FIREBASE_API_KEY),
  'authDomain': '{}.firebaseapp.com'.format(os.getenv('FIREBASE_PROJECT_ID', config.FIREBASE_PROJECT_ID)),
  'databaseURL': 'https://{}.firebaseio.com'.format(os.getenv('FIREBASE_PROJECT_ID', config.FIREBASE_PROJECT_ID)),
  'storageBucket': '{}.appspot.com'.format(os.getenv('FIREBASE_PROJECT_ID', config.FIREBASE_PROJECT_ID)),
}

image_ext = {'jpg', 'jpeg', 'png', 'eps', 'bmp'}

firebase = pyrebase.initialize_app(db_config)
db = firebase.database()
storage = firebase.storage()

def get_file_ext(filename):
	return filename.split('.')[-1]

def put_data(data, key):
	try:
		db.child(key).set(data)

	except Exception as e:
		print(e)

def put_all_figures(dir_paths, base_path, key):
	walked_path = set()

	for dir_path in dir_paths:
		for root, dirs, files in os.walk(os.path.join(base_path, dir_path)):
			for filename in files:
				filepath = os.path.join(root, filename)
				if get_file_ext(filename) in image_ext and filepath not in walked_path:
					# upload image
					prefix = root.split(base_path)[-1]
					upload_path = '{}{}'.format(key, os.path.join(prefix, filename))

					try:
						storage.child(upload_path).put(filepath)

					except Exception as e:
						print(e)
						continue

					walked_path |= {filepath}

def get_image_url(filepath, key):
	image_path = '{}/{}'.format(key, filepath)
	return storage.child(image_path).get_url(token=None)










