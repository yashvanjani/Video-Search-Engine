from flask import Flask, render_template
from flask import request
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask_mysqldb import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_USER'] = 'yash'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'TUTORIALS'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)




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



@app.route('/yash')
def app2():
	input1 = request.form['video']
	client = MongoClient()
	db = client.test_database
	coll = db.test_collection
	
	cursor = list(coll.find({'$text':{'$search': str(input1)}}).limit(5))
	#print cursor
	res = []
	for doc in cursor:
		res.append([doc['videoInfo']['snippet']['thumbnails']['high']['url'],doc['videoInfo']['snippet']['localized']['title'],doc['videoInfo']['snippet']['localized']['description']],)

	video_id = cursor['videoInfo']['id']

	conn=mysql.connection
	cursor = mysql.connection.cursor()
	
	query_string = "SELECT * FROM student;"
	cursor.execute(query_string)

	data=cursor.fetchall()

	# mysql.close()

	return render_template('select.html',data=data)
	
if __name__ == '__main__':
	app.run(debug=True)

