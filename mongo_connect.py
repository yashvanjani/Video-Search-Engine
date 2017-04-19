from flask import Flask, render_template
from flask import request
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)


@app.route('/koppar', methods=['POST'])
def app1():
	input1 = request.form['video']
	client = MongoClient()
	db = client.test_database
	coll = db.test_collection
	
	cursor = list(coll.find({'$text':{'$search': str(input1)}}).limit(5))
	#print cursor
	res = []
	for doc in cursor:
		res.append([doc['videoInfo']['snippet']['thumbnails']['high']['url'],doc['videoInfo']['snippet']['localized']['title'],doc['videoInfo']['snippet']['localized']['description']],)
	#print res	
	return render_template('2.html',data=res)	



@app.route('/')
def main():
	return render_template('1.html')


if __name__ == '__main__':
	app.run(debug=True)
