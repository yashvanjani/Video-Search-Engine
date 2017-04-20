from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from pymongo import MongoClient
from py2neo import Graph, Node, Relationship


app = Flask(__name__)

client = MongoClient()
db = client.test_database
coll = db.test_collection

graph = Graph("http://neo4j:7527@localhost:7474")

@app.route('/graph')


@app.route('/koppar', methods=['POST'])
def app1():
	input1 = request.form['video']
	cursor = list(coll.find({'$text':{'$search': str(input1)}}).limit(5))
	
	res = []
	for doc in cursor:
		res.append([doc['videoInfo']['snippet']['thumbnails']['high']['url'],doc['videoInfo']['snippet']['localized']['title'],doc['videoInfo']['snippet']['localized']['description'],doc['videoInfo']['id']],)
	
	return render_template('2.html',data=res)	

@app.route('/<video_id>', methods=['POST'])
def details(video_id):
	cursor = list(coll.find({"videoInfo.id": video_id}))  
	res = []
	for doc in cursor:
		res.append([doc['videoInfo']['snippet']['thumbnails']['high']['url'],doc['videoInfo']['snippet']['localized']['title'],doc['videoInfo']['snippet']['localized']['description'],doc['videoInfo']['id'],doc['videoInfo']['statistics']['likeCount']],)
	results = graph.cypher.execute("MATCH (e) WHERE e.name = video_id RETURN e")

	return render_template('3.html',data=res)
	


@app.route('/')
def main():
	return render_template('1.html')


if __name__ == '__main__':
	app.run(debug=True)
