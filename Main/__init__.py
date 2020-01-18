from flask import Flask, redirect, render_template, request
import json
import os

app = Flask(__name__)

@app.route("/")
def root():
	return render_template('home.html')

@app.route("/index.html")
def index():
	return render_template('index.html')

@app.route("/elements.html")
def elements():
	return render_template('elements.html')

@app.route("/generic.html")
def generic():
	return render_template('generic.html')

@app.route("/sh", methods=['GET'])
def sh():
	return render_template('sh.html')

@app.route("/chefs", methods=['GET'])
def chefs():
	filename = 'data.json' if os.stat("/remote/testapi/Main/data.json").st_size != 0 else 'empty.json'

	with open('/remote/testapi/Main/' + filename) as json_file:
		data = json.load(json_file)
	return render_template('chefs.html', chefs = data)
