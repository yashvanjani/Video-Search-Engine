from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask_mysqldb import MySQL
from py2neo import Graph, Node, Relationship


mysql = MySQL()
app = Flask(__name__)
# mysql config and connection
app.config['MYSQL_USER'] = 'yash'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'TUTORIALS'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)

# mongodb connection
client = MongoClient()
db = client.test_database
coll = db.test_collection

# neo4j connection
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
	cursor = list(coll.find({"videoInfo.id": (video_id)}))  
	res = []
	for doc in cursor:
		res.append([doc['videoInfo']['snippet']['thumbnails']['high']['url'],doc['videoInfo']['snippet']['localized']['title'],doc['videoInfo']['snippet']['localized']['description'],doc['videoInfo']['id'],doc['videoInfo']['statistics']['likeCount']],)
	# print cursor
	#results = graph.run("MATCH (e) WHERE e.name = {video_id} RETURN e")

	cursor2 = list(graph.run("MATCH (n {name: {a}})-[r:`Matching Tags`]->(m) RETURN m.name ORDER BY r.weightage DESC limit 5", a = str(video_id)))
	a="hello "
	print a
	# print cursor2

	res2=[]
	for doc in cursor2:
	  	res2.append([doc['m.name']],)
	# print res2

	# cursor3=list()
	# for doc in res2:
	reco1= list(coll.find({"videoInfo.id": res2[0][0]})) 
	reco2= list(coll.find({"videoInfo.id": res2[1][0]})) 
	reco3= list(coll.find({"videoInfo.id": res2[2][0]})) 
	reco4= list(coll.find({"videoInfo.id": res2[3][0]})) 
	reco5= list(coll.find({"videoInfo.id": res2[4][0]}))

	# print cursor3

	# for doc in cursor3:
	# 	res.append([doc['videoInfo']['snippet']['thumbnails']['high']['url'],doc['videoInfo']['snippet']['localized']['title'],doc['videoInfo']['snippet']['localized']['description'],doc['videoInfo']['id'],doc['videoInfo']['statistics']['likeCount']],)
	for doc in reco1:
		res.append([doc['videoInfo']['snippet']['thumbnails']['high']['url'],doc['videoInfo']['snippet']['localized']['title'],doc['videoInfo']['snippet']['localized']['description'],doc['videoInfo']['id'],doc['videoInfo']['statistics']['likeCount']],)
	for doc in reco2:
		res.append([doc['videoInfo']['snippet']['thumbnails']['high']['url'],doc['videoInfo']['snippet']['localized']['title'],doc['videoInfo']['snippet']['localized']['description'],doc['videoInfo']['id'],doc['videoInfo']['statistics']['likeCount']],)
	for doc in reco3:
		res.append([doc['videoInfo']['snippet']['thumbnails']['high']['url'],doc['videoInfo']['snippet']['localized']['title'],doc['videoInfo']['snippet']['localized']['description'],doc['videoInfo']['id'],doc['videoInfo']['statistics']['likeCount']],)
	for doc in reco4:
		res.append([doc['videoInfo']['snippet']['thumbnails']['high']['url'],doc['videoInfo']['snippet']['localized']['title'],doc['videoInfo']['snippet']['localized']['description'],doc['videoInfo']['id'],doc['videoInfo']['statistics']['likeCount']],)
	for doc in reco5:
		res.append([doc['videoInfo']['snippet']['thumbnails']['high']['url'],doc['videoInfo']['snippet']['localized']['title'],doc['videoInfo']['snippet']['localized']['description'],doc['videoInfo']['id'],doc['videoInfo']['statistics']['likeCount']],)


	return render_template('3.html',data=res)
	
@app.route('/')
def main():
	 return render_template('1.html')



@app.route('/yash')
def app2():
	# input1 = request.form['video']
	# client = MongoClient()
	# db = client.test_database
	# coll = db.test_collection
	
	# cursor = list(coll.find({'$text':{'$search': str(input1)}}).limit(5))
	# #print cursor
	# res = []
	# for doc in cursor:
	# 	res.append([doc['videoInfo']['snippet']['thumbnails']['high']['url'],doc['videoInfo']['snippet']['localized']['title'],doc['videoInfo']['snippet']['localized']['description']],)

	# video_id = cursor['videoInfo']['id']

	cursor = mysql.connection.cursor()
	
	query_string = "SELECT * FROM student;"
	cursor.execute(query_string)

	data=cursor.fetchall()

	# mysql.close()

	return render_template('select.html',data=data)
	
if __name__ == '__main__':
	app.run(debug=True)

