from flask import Flask, render_template, request, redirect, flash
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Links, db
import time 
import requests
import os
import pdb

app = Flask(__name__)

engine = create_engine('postgresql+psycopg2://surajkapoor:wilshere10@localhost/link_shortener')
app.config['SQLALCHEMY_DATABASE_URI'] = engine
app.secret_key = "secret!"

Session = sessionmaker(bind=engine)
session = Session()

alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

cached_entry = {}

def numb_to_string(num):
	output = []
	while num:
		rem = num % len(alpha)
		num = num / len(alpha)
		print rem, num
		output.append(alpha[rem])
	return str(''.join(output))

@app.route('/', methods = ["GET", "POST"])
def main():
	if request.method == "GET":
		return render_template("link.html")
	else:
		url = request.form.get('url')
		long_url = url.strip('/')
		try:
			response = str(requests.get(url))
		except requests.exceptions.MissingSchema:
			return render_template("link.html", response = "This doesn't look like a proper URL")
		if response == "<Response [200]>":
			find_long_url = Links.query.filter_by(long_url = long_url).first()
			if find_long_url:
				short_url = find_long_url.short_url
				return render_template("link.html", short_url = short_url)
			elif "last_entry_number" in cached_entry:	
				last_entry_number = cached_entry["last_entry_number"]
			else:	
				last_entry_number = session.query(Links).order_by(Links.entry_number.desc()).first()
				last_entry_number = last_entry_number.entry_number	
			new_entry_number = last_entry_number + 1
			short_url = request.url_root + numb_to_string(int(new_entry_number))
			cached_entry["last_entry_number"] = new_entry_number
			link = Links(long_url = long_url, short_url = short_url, metrics = "None")
			db.session.add(link)
			db.session.commit()
			return render_template("link.html", short_url = short_url)
		else:
			return render_template("link.html", response = "This is a bad URL")		


@app.route('/<path:path>')
def catch_url(path):
	short_url = request.url_root + str(path)
	find_short_url = Links.query.filter_by(short_url = short_url).first()
	if find_short_url:
		return redirect(find_short_url.long_url)		
	return "URL NOT FOUND"		

if __name__ == "__main__":
	app.run(debug = True, host = "0.0.0.0")