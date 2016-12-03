import json
from watson_developer_cloud import AlchemyLanguageV1

def getAlchemyLanguageV1(text):
	alchemy_language = AlchemyLanguageV1(api_key='a28509b72075355ab9daa10adcab355f6dd9dc7a')
	return json.dumps(
		alchemy_language.combined(
			text=text, 
			extract='entities,keywords,concepts,doc-emotion',
			sentiment=1,
			max_items=5),
		indent=2)