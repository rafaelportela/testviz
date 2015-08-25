from flask import Flask, redirect, render_template, json, Response, abort
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

from database import init_db
from models import Run, Test

@app.route('/')
def index():
  return redirect('/runs', code=302)

@app.route('/runs')
def runs():
  runs = Run.query.all()
  data = [run.serialize() for run in runs]

  return Response(json.dumps(data), status=200, mimetype="application/json")

@app.route('/runs/<run_id>')
def run(run_id):
  run = Run.query.get(run_id)
  if run is None:
      abort(404)

  return Response(json.dumps(run.serialize()), status=200, mimetype="application/json")

@app.route('/tests')
def tests():
    tests = Test.query.all()
    data = [test.serialize() for test in tests]

    return Response(json.dumps(data), status=200, mimetype="application/json")

if __name__ == '__main__':
  database_url = os.getenv('DATABASE_URL', 'mysql://dashboard:password@192.168.33.42/sandbox_test')
  init_db(database_url)
  from database import db_session
  app.run(debug=True, host=os.getenv('HOST', 'localhost'))
