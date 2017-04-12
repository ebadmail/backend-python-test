from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy

from config import *


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE


def connect_db():
    db = SQLAlchemy(app)
    return db


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


import alayatodo.views
