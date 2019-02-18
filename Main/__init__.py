from flask import Flask, redirect, render_template, request
from .parser import GraciesHtmlParser
from .button import ButtonObject
from typing import List
import urllib.parse
import urllib.request
import datetime
import pickle

app = Flask(__name__)

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


def save_cache(obj):
	with open('/remote/testapi/Main/obj/' + 'gracies_menu_cache' + '.pkl', 'wb') as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

	
def load_cache():
	with open('/remote/testapi/Main/obj/' + 'gracies_menu_cache' + '.pkl', 'rb') as f:
		return pickle.load(f)
	

def get_menu_content(date):
	if date in cache:
		return cache[date]
	else:
		values = {'menu_date': date}
		html = post('https://www.rit.edu/fa/diningservices/gracies', values)
		parser = GraciesHtmlParser()
		parser.feed(html)
		cache[date] = parser.get_output()
		save_cache(cache)
		return parser.get_output()


@app.route("/")
def root():
	return redirect("http://bradsraspi.student.rit.edu/gracies", code=302)


@app.route("/gracies", methods=['POST', 'GET'])
def gracies():
	if request.method =='POST':
		date_displayed = request.form['button']
	else:
		date_displayed = datetime.datetime.now().strftime("%Y-%m-%d")
	
	return render_template('gracies.html', content = get_menu_content(date_displayed), buttons = setup_buttons(), date = date_displayed)

	
cache = load_cache()

