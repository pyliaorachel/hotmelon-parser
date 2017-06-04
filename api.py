import config
import os
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as features

natural_language_understanding = NaturalLanguageUnderstandingV1(
	version='2017-06-03',
	username=os.getenv('WATSON_KEYWORD_EXTRACTOR_USERNAME', config.WATSON_KEYWORD_EXTRACTOR_USERNAME),
	password=os.getenv('WATSON_KEYWORD_EXTRACTOR_PASSWORD', config.WATSON_KEYWORD_EXTRACTOR_PASSWORD),
)

def get_keywords(text):
	try:
		response = natural_language_understanding.analyze(
			text=text,
			features=[features.Keywords()]
		)

		l = list(map(lambda k: k['text'], response['keywords']))

	except Exception as e:
		print(e)
		return []

	return l