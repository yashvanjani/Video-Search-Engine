from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask_mysqldb import MySQL
from py2neo import Graph, Node, Relationship


mysql = MySQL()
app = Flask(__name__)
# mysql config and connection
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'Youtube'
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
	cursor = list(coll.find({'$text':{'$search': str(input1)}}))
	
	res = []
	for doc in cursor:
		res.append([doc['videoInfo']['snippet']['thumbnails']['high']['url'],doc['videoInfo']['snippet']['localized']['title'],doc['videoInfo']['snippet']['localized']['description'],doc['videoInfo']['id'],doc['videoInfo']['statistics']['viewCount'],doc['videoInfo']['statistics']['likeCount'],doc['videoInfo']['statistics']['dislikeCount']],)
	
	conn = mysql.connection
	cursor1 = conn.cursor()
	
	query_string = "SELECT * FROM Video_info;"
	cursor1.execute(query_string)

	data=cursor1.fetchall()
	# conn.close()
	# print data

	for doc in res:
		# if the video does not exist in mysql database, then add it
		found=0
		for info in data:
			if doc[3]==info[0]:
				found=1
				
		if found==0:
			# print"adding to mysql db"
			conn = mysql.connection
			cursor1 = conn.cursor()
			query_string = "INSERT INTO Video_info (video_id, viewCount, likeCount, dislikeCount) VALUES ('{}', {}, {}, {});".format(doc[3],doc[4],doc[5],doc[6])
			cursor1.execute(query_string)
			# cursor1.close()
			conn.commit()
			# conn.close()
			# print "added"
			# print query_string

	# now our video shurely exists in the mysql database, now getting the sorted order according to viewcount
	sorted_data=sorted(data,key=lambda x:-x[1])
	# print sorted_data

	# showing only top 5 results
	res_final=[]
	sorted_data=sorted_data[0:5]
	for sort_doc in sorted_data:
		for doc in res:
			if (sort_doc[0] == doc[3]):
				res_final.append(doc)
				print sort_doc[0],sort_doc[1]
				print doc[3],doc[4]
	# print res_final
	return render_template('2.html',data=res_final)	

@app.route('/<video_id>', methods=['GET','POST'])
def details(video_id):
	cursor = list(coll.find({"videoInfo.id": video_id})) 
	# if method=='GET':
	# 	url1 = "www.youtube.com/watch?v="+str(video_id) 
	# 	print url1
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


	return render_template('list.html',data=res)
	
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

