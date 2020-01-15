from flask import Flask, redirect, render_template, request
from .parser import DiningHtmlParser
from .button import ButtonObject
from typing import List
import json
import urllib.parse
import urllib.request
import datetime
import pickle
import os

app = Flask(__name__)

class MenuCache():
	cache_name = None
	cache = None
	def __init__(self, cache, cache_name):
		self.cache_name = cache_name
		self.cache = cache

		
def get(url: str) -> str:
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')

	
def post(url: str, values) -> str:
	data = urllib.parse.urlencode(values)
	data = data.encode('utf-8')
	req = urllib.request.Request(url, data)
	return urllib.request.urlopen(req).read().decode('utf-8')
	

def setup_buttons() -> List[ButtonObject]:
	buttons = []
	today = datetime.datetime.now()
	for i in range(7):
		target_day = today + datetime.timedelta(days = i)
		buttons.append(ButtonObject(target_day.strftime("%Y-%m-%d")))
	return buttons


def save_obj(obj, name):
	with open('/remote/testapi/Main/obj/' + name + '.pkl', 'wb') as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

	
def load_obj(name):
	with open('/remote/testapi/Main/obj/' + name + '.pkl', 'rb') as f:
		return pickle.load(f)
	

def get_menu_content(date, cache, backup_url):
	if date in cache.cache:
		return cache.cache[date]
	else:
		values = {'menu_date': date}
		html = post(backup_url, values)
		parser = DiningHtmlParser()
		parser.feed(html)
		cache.cache[date] = parser.get_output()
		save_obj(cache.cache, cache.cache_name)
		return parser.get_output()


def get_date_displayed(request):
	if request.method =='POST':
		return request.form['button']
	else:
		return datetime.datetime.now().strftime("%Y-%m-%d")

	
@app.route("/")
def root():
	return render_template('home.html')

@app.route("/ritz", methods=['POST', 'GET'])
def ritz():
	date_displayed = get_date_displayed(request)
	menu_content = get_menu_content(date_displayed, MenuCache(ritz_cache, 'ritz_menu_cache'), 'https://www.rit.edu/fa/diningservices/ritz-sports-zone')
	return render_template('menu.html', content = menu_content, buttons = setup_buttons(), date = date_displayed, location = "Ritz")


@app.route("/brickcity", methods=['POST', 'GET'])
def brickcity():
	date_displayed = get_date_displayed(request)
	menu_content = get_menu_content(date_displayed, MenuCache(brickcity_cache, 'brickcity_menu_cache'), 'https://www.rit.edu/fa/diningservices/brick-city-cafe')
	return render_template('menu.html', content = menu_content, buttons = setup_buttons(), date = date_displayed, location = "Brick City")
	
	
@app.route("/gracies", methods=['POST', 'GET'])
def gracies():
	date_displayed = get_date_displayed(request)
	menu_content = get_menu_content(date_displayed, MenuCache(gracies_cache, 'gracies_menu_cache'), 'https://www.rit.edu/fa/diningservices/gracies')
	return render_template('menu.html', content = menu_content, buttons = setup_buttons(), date = date_displayed, location = "Gracie's")


@app.route("/crossroads", methods=['POST', 'GET'])
def crossroads():
        date_displayed = get_date_displayed(request)
        menu_content = get_menu_content(date_displayed, MenuCache(crossroads_cache, 'crossroads_menu_cache'), 'https://www.rit.edu/fa/diningservices/cafe-market-crossroads')
        return render_template('menu.html', content = menu_content, buttons = setup_buttons(), date = date_displayed, location = 'Crossroads')


@app.route("/sh", methods=['GET'])
def sh():
	return render_template('sh.html')

@app.route("/chefs", methods=['GET'])
def chefs():
	with open('/remote/testapi/Main/data.json') as json_file:
		data = json.load(json_file)
	return render_template('chefs.html', chefs = data)

	
gracies_cache = load_obj('gracies_menu_cache')
ritz_cache = load_obj('ritz_menu_cache')
brickcity_cache = load_obj('brickcity_menu_cache')
crossroads_cache = load_obj('crossroads_cache')
