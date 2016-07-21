import flask
from flask import Flask, render_template, flash, redirect, url_for, request
import json
import re

app = Flask(__name__)

"""
:Assumptions to note  
	:Multi line data 
	:Only 1 phone number per line (script will ignore the second number, if any)
	:Only 1 date string per line 
	:US format 10 digits or 11 digit (including country code)

"""

@app.route("/")
def index():
	return render_template('index.html')


@app.route('/submit', methods=['GET', 'POST'])
def form_submit():
	text = request.form['phone_field']
	numbers =[]
	def get_num(txt):
		out = re.sub("\D", "", txt)
		if not out or (len(out) >11 or len(out) <10):return 
		if(len(out) == 11): 
			if out[0] == '1':
				out = out[1:]
			else: return 

		#print 'outnow' + out
		return '('+out[:3]+')'+out[3:6]+ '-'+ out[6:10]

	if text:
		i_text = text.split('\n') 
		numbers =[]
		for line in i_text:
			number = get_num(line)
			if number:
				numbers.append(number)
			

	if numbers: 
		result = {"numbers" : numbers }
		response =flask.Response(json.dumps(result))
		return response

	return json.dumps({"error" : "bad inputs"})



if __name__ == "main__":
    #app.run(host="0.0.0.0", port=5000, threaded=True)
    app.run(debug = True)