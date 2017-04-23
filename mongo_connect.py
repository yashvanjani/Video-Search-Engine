from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask_mysqldb import MySQL
from py2neo import Graph, Node, Relationship
import urllib



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

@app.route('/koppar', methods=['POST'])
def app1():
	input1 = request.form['video']
	db = client.test_database
	coll = db.test_collection
	cursor = list(coll.find({'$text':{'$search': str(input1)}}))
	
	res = []
	for doc in cursor:
		res.append([doc['videoInfo']['snippet']['thumbnails']['high']['url'],doc['videoInfo']['snippet']['localized']['title'],doc['videoInfo']['snippet']['localized']['description'],doc['videoInfo']['id'],doc['videoInfo']['statistics']['viewCount'],doc['videoInfo']['statistics']['likeCount'],doc['videoInfo']['statistics']['dislikeCount']],)
	# print len(res)
	
	# conn.close()
	# print data

	for doc in res:
		# if the video does not exist in mysql database, then add it
		conn = mysql.connection
		cursor1 = conn.cursor()
		
		query_string = "SELECT * FROM Video_info;"
		cursor1.execute(query_string)

		data=cursor1.fetchall()

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
	# print sorted_data
	# sorted_data=sorted_data[0:10]
	for sort_doc in sorted_data:
		for doc in res:
			if (sort_doc[0] == doc[3]):
				res_final.append(doc)
				# print sort_doc[0],sort_doc[1]
				# print doc[3],doc[4]
	# print res_final
	# print len(res_final)

	# removing mysql algo
	# res_final=res
	print "koppar"
	return render_template('2.html',data=res_final)	

@app.route('/<video_id>', methods=['POST'])
def details(video_id):
	db = client.test_database
	coll = db.test_collection
	cursor = list(coll.find({"videoInfo.id": video_id})) 
	
	url1 = "www.youtube.com/embed/"+str(video_id) 
	# url1 = encodeURIComponent(url1)
	url1 = urllib.quote(url1.encode("utf-8"))
	# print url1

	res = []
	for doc in cursor:
		res.append([doc['videoInfo']['snippet']['thumbnails']['high']['url'],doc['videoInfo']['snippet']['localized']['title'],doc['videoInfo']['snippet']['localized']['description'],doc['videoInfo']['id'],doc['videoInfo']['statistics']['likeCount']],)
	# print cursor
	#results = graph.run("MATCH (e) WHERE e.name = {video_id} RETURN e")

	cursor2 = list(graph.run("MATCH (n {name: {a}})-[r]->(m) RETURN m.name ORDER BY r.weightage DESC limit 5", a = str(video_id)))
	a="hello "
	# print a
	# print cursor
	# print cursor2

	res2=[]
	for doc in cursor2:
	  	res2.append([doc['m.name']],)
	# print res2
	# print cursor2

	# cursor3=list()
	# for doc in res2:
	#print "cursor2 leng"
	#print len(cursor2)
	db = client.test_database
	coll = db.test_collection
	reco1= list(coll.find({"videoInfo.id": res2[0][0]})) 
	reco2= list(coll.find({"videoInfo.id": res2[1][0]})) 
	reco3= list(coll.find({"videoInfo.id": res2[2][0]})) 
	reco4= list(coll.find({"videoInfo.id": res2[3][0]})) 
	reco5= list(coll.find({"videoInfo.id": res2[4][0]}))

	conn = mysql.connection
	cursor1 = conn.cursor()
	query_string = "UPDATE Video_info SET viewCount = viewCount + 1 WHERE video_id = '{}'".format(video_id)
	cursor1.execute(query_string)
	# cursor1.close()
	conn.commit()

	# adding to click_history table in mysql
	conn = mysql.connection
	cursor1 = conn.cursor()
	query_string = "INSERT INTO click_history (video_id) VALUES ('{}');".format(video_id)
	cursor1.execute(query_string)
	# cursor1.close()
	conn.commit()

	# get new view count from mysql
	conn = mysql.connection
	cursor1 = conn.cursor()
	query_string = "SELECT * FROM Video_info WHERE video_id = '{}'".format(video_id)
	cursor1.execute(query_string)
	newView=cursor1.fetchall()
	# cursor1.close()
	conn.commit()


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

	print "video_id"
	return render_template('list.html',data=res, url=url1, view=newView[0][1], like=newView[0][2], dislike=newView[0][3])
	
@app.route('/')
def main():
	print "main"
	return render_template('1.html')

@app.route('/like_increment', methods=['POST'])
def like():
	print "like increment"
	video_id = request.form['video_id']
	conn = mysql.connection
	cursor1 = conn.cursor()
	query_string = "UPDATE Video_info SET likeCount = likeCount + 1 WHERE video_id = '{}'".format(video_id)
	cursor1.execute(query_string)
	# cursor1.close()
	conn.commit()

	# link="http://127.0.0.1:5000/{}".format(id)
	# return redirect(link, code=307)

	db = client.test_database
	coll = db.test_collection
	cursor = list(coll.find({"videoInfo.id": video_id})) 
	
	url1 = "www.youtube.com/embed/"+str(video_id) 
	# url1 = encodeURIComponent(url1)
	url1 = urllib.quote(url1.encode("utf-8"))
	# print url1

	res = []
	for doc in cursor:
		res.append([doc['videoInfo']['snippet']['thumbnails']['high']['url'],doc['videoInfo']['snippet']['localized']['title'],doc['videoInfo']['snippet']['localized']['description'],doc['videoInfo']['id'],doc['videoInfo']['statistics']['likeCount']],)
	# print cursor
	#results = graph.run("MATCH (e) WHERE e.name = {video_id} RETURN e")

	cursor2 = list(graph.run("MATCH (n {name: {a}})-[r]->(m) RETURN m.name ORDER BY r.weightage DESC limit 5", a = str(video_id)))
	a="hello "
	# print a
	# print cursor
	# print cursor2

	res2=[]
	for doc in cursor2:
	  	res2.append([doc['m.name']],)
	# print res2
	# print cursor2

	# cursor3=list()
	# for doc in res2:
	#print "cursor2 leng"
	#print len(cursor2)
	db = client.test_database
	coll = db.test_collection
	reco1= list(coll.find({"videoInfo.id": res2[0][0]})) 
	reco2= list(coll.find({"videoInfo.id": res2[1][0]})) 
	reco3= list(coll.find({"videoInfo.id": res2[2][0]})) 
	reco4= list(coll.find({"videoInfo.id": res2[3][0]})) 
	reco5= list(coll.find({"videoInfo.id": res2[4][0]}))

	# conn = mysql.connection
	# cursor1 = conn.cursor()
	# query_string = "UPDATE Video_info SET viewCount = viewCount + 1 WHERE video_id = '{}'".format(video_id)
	# cursor1.execute(query_string)
	# # cursor1.close()
	# conn.commit()

	conn = mysql.connection
	cursor1 = conn.cursor()
	query_string = "SELECT * FROM Video_info WHERE video_id = '{}'".format(video_id)
	cursor1.execute(query_string)
	newView=cursor1.fetchall()
	# cursor1.close()
	conn.commit()

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


	return render_template('list.html',data=res, url=url1, view=newView[0][1], like=newView[0][2], dislike=newView[0][3])

@app.route('/dislike_increment', methods=['POST'])
def dislike():
	print "dislike increment"
	video_id = request.form['video_id']
	conn = mysql.connection
	cursor1 = conn.cursor()
	query_string = "UPDATE Video_info SET dislikeCount = dislikeCount + 1 WHERE video_id = '{}'".format(video_id)
	cursor1.execute(query_string)
	# cursor1.close()
	conn.commit()

	# link="http://127.0.0.1:5000/{}".format(id)
	# return redirect(link, code=307)

	db = client.test_database
	coll = db.test_collection
	cursor = list(coll.find({"videoInfo.id": video_id})) 
	
	url1 = "www.youtube.com/embed/"+str(video_id) 
	# url1 = encodeURIComponent(url1)
	url1 = urllib.quote(url1.encode("utf-8"))
	# print url1

	res = []
	for doc in cursor:
		res.append([doc['videoInfo']['snippet']['thumbnails']['high']['url'],doc['videoInfo']['snippet']['localized']['title'],doc['videoInfo']['snippet']['localized']['description'],doc['videoInfo']['id'],doc['videoInfo']['statistics']['likeCount']],)
	# print cursor
	#results = graph.run("MATCH (e) WHERE e.name = {video_id} RETURN e")

	cursor2 = list(graph.run("MATCH (n {name: {a}})-[r]->(m) RETURN m.name ORDER BY r.weightage DESC limit 5", a = str(video_id)))
	a="hello "
	# print a
	# print cursor
	# print cursor2

	res2=[]
	for doc in cursor2:
	  	res2.append([doc['m.name']],)
	# print res2
	# print cursor2

	# cursor3=list()
	# for doc in res2:
	#print "cursor2 leng"
	#print len(cursor2)
	db = client.test_database
	coll = db.test_collection
	reco1= list(coll.find({"videoInfo.id": res2[0][0]})) 
	reco2= list(coll.find({"videoInfo.id": res2[1][0]})) 
	reco3= list(coll.find({"videoInfo.id": res2[2][0]})) 
	reco4= list(coll.find({"videoInfo.id": res2[3][0]})) 
	reco5= list(coll.find({"videoInfo.id": res2[4][0]}))

	# conn = mysql.connection
	# cursor1 = conn.cursor()
	# query_string = "UPDATE Video_info SET viewCount = viewCount + 1 WHERE video_id = '{}'".format(video_id)
	# cursor1.execute(query_string)
	# # cursor1.close()
	# conn.commit()

	conn = mysql.connection
	cursor1 = conn.cursor()
	query_string = "SELECT * FROM Video_info WHERE video_id = '{}'".format(video_id)
	cursor1.execute(query_string)
	newView=cursor1.fetchall()
	# cursor1.close()
	conn.commit()

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


	return render_template('list.html',data=res, url=url1, view=newView[0][1], like=newView[0][2], dislike=newView[0][3])
	
@app.route('/trending', methods=['POST'])
def trending():
	
	conn = mysql.connection
	cursor1 = conn.cursor()
	
	query_string = "SELECT DISTINCT video_id FROM Video_info ORDER BY viewCount DESC LIMIT 10;"
	cursor1.execute(query_string)

	data=cursor1.fetchall()
	# print data
	res = []
	for row in data:
		db = client.test_database
		coll = db.test_collection
		print row[0]
		cursor = list(coll.find({'videoInfo.id':str(row[0])}))
		print cursor
		for doc in cursor:
			res.append([doc['videoInfo']['snippet']['thumbnails']['high']['url'],doc['videoInfo']['snippet']['localized']['title'],doc['videoInfo']['snippet']['localized']['description'],doc['videoInfo']['id'],doc['videoInfo']['statistics']['viewCount'],doc['videoInfo']['statistics']['likeCount'],doc['videoInfo']['statistics']['dislikeCount']],)

	
	print "trending"
	return render_template('2.html',data=res)

@app.route('/history', methods=['POST'])
def history():
	
	conn = mysql.connection
	cursor1 = conn.cursor()
	
	query_string = "SELECT DISTINCT video_id FROM click_history;"
	cursor1.execute(query_string)

	data=cursor1.fetchall()
	data=data[::-1] #reversed data 
	# print data
	res = []
	for row in data:
		db = client.test_database
		coll = db.test_collection
		print row[0]
		cursor = list(coll.find({'videoInfo.id':str(row[0])}))

		print str(row[0])
		print cursor
		for doc in cursor:
			res.append([doc['videoInfo']['snippet']['thumbnails']['high']['url'],doc['videoInfo']['snippet']['localized']['title'],doc['videoInfo']['snippet']['localized']['description'],doc['videoInfo']['id'],doc['videoInfo']['statistics']['viewCount'],doc['videoInfo']['statistics']['likeCount'],doc['videoInfo']['statistics']['dislikeCount']],)

	
	print "history"
	return render_template('2.html',data=res)

if __name__ == '__main__':
	# app.run(host='172.16.68.34')
	app.run(debug=True)

