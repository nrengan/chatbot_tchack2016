import pickle

record = {}
def loadData():
	record = pickle.load( open( "save.plk", "rb" ))
	return record

def saveData(record):
	pickle.dump( record, open( "save.plk", "wb" ))