import os
import pickle

files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
	print f

record = {}
def loadData():
	record = pickle.load( open( "save.plk", "rb" ))
	return record

def saveData(record):


	pickle.dump( record, open( "save.plk", "wb" ))


