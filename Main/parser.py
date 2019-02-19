from html.parser import HTMLParser

dining_stations = ["Breakfast Standards", "Breakfast Meat", "Breakfast Potato", "Hot Breakfast Choices", "Breakfast Patries",
					"Simply Eats Pasta and Sauces", "Simply Eats Vegetables, Salads and Starches", "Mongolian Grill", "Pizza Special",
					"Simply Eats Meat Dishes", "Bakery", "East Bar", "West Bar", "Quick Serve Items", "Visiting Chef - Lunch",
					"Visiting Chef - Dinner", "Soup", "Grill", "Pizza", "Panini", "Deli", "Breakfast Salad Bar", "Breakfast Sandwiches",
					"Breakfast Grill", "Omelet Bar", "Main Entree", "Lunch Salad Bar", "Pot Luck", "Choices", "Wraps", "Soups",
					"Deli Special", "Brick City Cafe Bar", "Visiting Chefs", "Vegetarian Entree"]

important_stations = ["Mongolian Grill", "West Bar", "East Bar", "Visiting Chef - Lunch", "Visiting Chef - Dinner", "Visiting Chefs", "Main Entree"]
					
class DiningHtmlParser(HTMLParser):
	record_output = False
	output = ""

	def add_line(self, data):
		self.output+=data
		#self.output+="<br/>"
	
	def get_output(self):
		return self.output
	
	def handle_starttag(self, tag, attrs):
		if len(attrs) >0 and (attrs[0][1] == '107' or attrs[0][1] == '103' or attrs[0][1] == '108'):
			self.record_output = True
		
	def handle_endtag(self, tag):
		pass
			
	def handle_data(self, data):
		if self.record_output and not data.isspace():
			if data == "BREAKFAST MENU" or data == "LUNCH MENU" or data == "DINNER MENU":
				self.add_line("<h3>"+data+"</h3>")
			elif data in dining_stations:
				if data in important_stations:
					self.add_line("<strong style='color: red'>"+data+"</strong><br/>")
				else:
					self.add_line("<strong>"+data+"</strong><br/>")
			else:
				self.add_line(data+"<br/>") 

	def handle_comment(self, data):
		if data == " END DAILY SPECIALS SECTION ":
			self.record_output = False
