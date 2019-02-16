from flask import Flask, redirect, render_template, request
from html.parser import HTMLParser
import urllib.parse
import urllib.request
import datetime

app = Flask(__name__)

gracies_stations = ["Breakfast Standards", "Breakfast Meat", "Breakfast Potato", "Hot Breakfast Choices", "Breakfast Patries",
					"Simply Eats Pasta and Sauces", "Simply Eats Vegetables, Salads and Starches", "Mongolian Grill", "Pizza Special",
					"Simply Eats Meat Dishes", "Bakery", "East Bar", "West Bar", "Quick Serve Items"]
important_stations = ["Mongolian Grill", "West Bar", "East Bar"]
					
class GraciesHtmlParser(HTMLParser):
	record_output = False
	output = ""

	def add_line(self, data):
		self.output+=data
		#self.output+="<br/>"
	
	def get_output(self):
		return self.output
	
	def handle_starttag(self, tag, attrs):
		if len(attrs) >0 and attrs[0][1] == '107':
			self.record_output = True
		
	def handle_endtag(self, tag):
		pass
			
	def handle_data(self, data):
		if self.record_output and not data.isspace():
			if data == "BREAKFAST MENU" or data == "LUNCH MENU" or data == "DINNER MENU":
				self.add_line("<h3>"+data+"</h3>")
			elif data in gracies_stations:
				if data in important_stations:
					self.add_line("<strong style='color: red'>"+data+"</strong><br/>")
				else:
					self.add_line("<strong>"+data+"</strong><br/>")
			else:
				self.add_line(data+"<br/>") 

	def handle_comment(self, data):
		if data == " END DAILY SPECIALS SECTION ":
			self.record_output = False
			

class ButtonObject:
	text = "Error" 
	def __init__(self, text: str):
		self.text = text


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
	
	
