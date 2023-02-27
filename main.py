#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, request, jsonify
import uuid
import sqlite3 as sl
import os
import time

app = Flask(__name__)


base_wait = 0.1
api_fail_every = 0
slowing_over_time = 0.005

threads = 0
api_request_count = 0


@app.route('/getkey', methods=['GET'])
def getUserKey():
	global threads, base_wait
	base_wait = base_wait + slowing_over_time
	threads = threads + 1
	username = request.args.get('username')
	password = request.args.get('password')
	print (username)
	if username == 'jesper' and password == 'andersen':
		id_string = str(uuid.uuid4())
		sql = 'INSERT INTO USER (id) values("%s")'%id_string
		print (sql)
		dbcon2 = sl.connect('my-test.db',check_same_thread=False)
		with dbcon2:
			dbcon2.execute(sql)
			w = threads * base_wait
		dbcon2.close()
		print ("Wait: %i"%w)
		time.sleep(threads * base_wait)
		threads = threads - 1
		return jsonify ({'token':id_string})
	threads = threads - 1
	return jsonify({'error': 'You must specify username and password'}),400

@app.route('/api1', methods=['GET'])
def api1():
	global threads, api_request_count, base_wait
	base_wait = base_wait + slowing_over_time
	api_request_count = api_request_count + 1
	
	if api_fail_every > 0 and api_request_count % api_fail_every == 0:
		response = jsonify({'message':'Server error'})
		return response, 500
	threads = threads + 1
	token = request.headers.get('accesstoken')
	if token == None:
		time.sleep(threads * base_wait)
		threads = threads - 1
		response = jsonify({'message':'invalid token'})
		return response, 401
	dbcon = sl.connect('my-test.db',check_same_thread=False)
	with dbcon:
		sql = 'SELECT * FROM USER WHERE id = "%s";'%token
		key = dbcon.execute(sql)
	dbcon.close()
	time.sleep(threads * base_wait)
	threads = threads - 1
	
	return jsonify({'random':'json'})
	
@app.route('/api2', methods=['GET'])
def api2():
	token = request.headers.get('accesstoken')
	if token == None:
		response = jsonify({'message':'invalid token'})
		return response, 401
	return jsonify({'random':'json'})
	

	
def setupDB():
	with con:
		con.execute("""
			CREATE TABLE USER (
				id UUID NOT NULL PRIMARY KEY
			);
		""")
	
	
os.remove("my-test.db")
con = sl.connect('my-test.db',check_same_thread=False)
setupDB()
con.close()
app.run(debug=True,threaded=True,host="0.0.0.0", port=7777)

