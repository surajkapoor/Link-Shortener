from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://surajkapoor:wilshere10@localhost/link_shortener'
db = SQLAlchemy(app)

class Links(db.Model):

	__tablename__ = "link_shortener"
	entry_number = db.Column(db.Integer, primary_key= True)
	long_url = db.Column(db.String, unique=True)
	short_url = db.Column(db.String, unique=True)
	metrics = db.Column(db.String)

	def __init__(self, long_url, short_url, metrics):
		self.long_url = long_url
		self.short_url = short_url
		self.metrics = metrics
