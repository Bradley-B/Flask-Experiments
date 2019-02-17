from flask import Flask, redirect, render_template, request
from .parser import GraciesHtmlParser
from .button import ButtonObject
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
	
	
@app.route("/")
def root():
	return redirect("http://bradsraspi.student.rit.edu/gracies", code=302)


@app.route("/gracies", methods=['POST', 'GET'])
def gracies():
	
	if request.method =='POST':
		values = {"menu_date": request.form['button']}
		html = post('https://www.rit.edu/fa/diningservices/gracies', values)
		date_displayed = request.form['button']
	else:
		html = get('https://www.rit.edu/fa/diningservices/gracies')
		date_displayed = datetime.datetime.now().strftime("%Y-%m-%d")
	
	parser = GraciesHtmlParser()
	parser.feed(html)
	
	buttons = []
	today = datetime.datetime.now()
	for i in range(7):
		target_day = today + datetime.timedelta(days = i)
		buttons.append(ButtonObject(target_day.strftime("%Y-%m-%d")))
	
	return render_template('gracies.html', content = parser.get_output(), buttons = buttons, date = date_displayed)
	
	
