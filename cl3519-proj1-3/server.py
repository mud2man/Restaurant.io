#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@104.196.18.7/w4111
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.18.7/w4111"
#
DATABASEURI = "postgresql://cl3519:89060@104.196.18.7/w4111"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#

#engine.execute("""CREATE TABLE IF NOT EXISTS test (
#  id serial,
#  name text
#);""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
@app.route('/index')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print request.args


  #
  # example of a database query
  #
  
  #cursor = g.conn.execute("SELECT name FROM test")
  #names = []
  #for result in cursor:
  #  names.append(result['name'])  # can also be accessed using result[0]
  #cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  #context = dict(data = names)

  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  #return render_template("index.html", **context)
  return render_template("index.html")

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#

####### SQL#1: List all the address of the restaurant ######
@app.route('/listAddressRestaurant')
def listAdressRestaurant():
  names = []
  context = dict(data = names)
  return render_template("listAddressRestaurant.html", **context)

@app.route('/doListAddressRestaurant', methods=['POST'])
def doListAddressRestaurant():
  restaurant = request.form['restaurant']

  # SQL command
  command = "select address "
  command += "FROM restaurant R "
  command += "WHERE R.rname='" + restaurant + "'"

  cursor = g.conn.execute(command)
  addrs = []
  for result in cursor:
    addrs.append(result['address'])  # can also be accessed using result[0]
  cursor.close()
  context = dict(data = addrs)
  return render_template("listAddressRestaurant.html", **context)

###### SQL#2: List the restaurants with the specific number of stars (rating) around me ######
@app.route('/listRestaurantStarAroundMe')
def listRestaurantStarAroundMe():
  names = []
  context = dict(data = names)
  return render_template("listRestaurantStarAroundMe.html", **context)

@app.route('/doListRestaurantStarAroundMe', methods=['POST'])
def doListRestaurantStarAroundMe():
  uid = request.form['uid']
  rating = request.form['rating']

  # SQL command
  command = "SELECT R.rname "
  command += "FROM restaurant R, restaurant_user U "
  command += "WHERE U.uid='" + uid + "' AND "
  command += "R.rating>'" + rating + "' AND "
  command += "ABS(R.rlat - U.ulat) < 0.005 AND "
  command += "ABS(R.rlng - U.ulng) < 0.005"

  cursor = g.conn.execute(command)
  restaurants = []
  for result in cursor:
    restaurants.append(result['rname'])
  cursor.close()
  context = dict(data = restaurants)
  return render_template("listRestaurantStarAroundMe.html", **context)

###### SQL#3: How many and what restaurants around me opened now  ######
@app.route('/listRestaurantAroundMeAndOpen')
def listRestaurantAroundMeAndOpen():
  names = []
  context = dict(data = names)
  return render_template("listRestaurantAroundMeAndOpen.html", **context)

@app.route('/doListRestaurantAroundMeAndOpen', methods=['POST'])
def doListRestaurantAroundMeAndOpen():
  uid = request.form['uid']
  day = request.form['day']
  time = request.form['time']
  tid = 2*int(day) + int(time) - 1

  # SQL command
  command = "SELECT R.rname "
  command += "FROM restaurant R, restaurant_user U, is_open_during I "
  command += "WHERE U.uid='" + uid + "' AND "
  command += "ABS(R.rlat - U.ulat) < 0.005 AND "
  command += "ABS(R.rlng - U.ulng) < 0.005 AND "
  command += "R.rid = I.rid AND "
  command += "I.tid = '" + str(tid) + "'"

  cursor = g.conn.execute(command)
  restaurants = []
  for result in cursor:
    restaurants.append(result['rname'])
  cursor.close()
  context = dict(data = restaurants)
  return render_template("listRestaurantAroundMeAndOpen.html", **context)

###### SQL#4: List restaurants with cost under $10 around me ######
@app.route('/listRestaurantCostAroundMe')
def listRestaurantCostAroundMe():
  names = []
  context = dict(data = names)
  return render_template("listRestaurantCostAroundMe.html", **context)

@app.route('/doListRestaurantCostAroundMe', methods=['POST'])
def doListRestaurantCostAroundMe():
  uid = request.form['uid']
  cost = request.form['cost']

  # SQL command
  command = "SELECT R.rname "
  command += "FROM restaurant R, restaurant_user U "
  command += "WHERE U.uid='" + uid + "' AND "
  command += "R.cost<'" + cost + "' AND "
  command += "ABS(R.rlat - U.ulat) < 0.005 AND "
  command += "ABS(R.rlng - U.ulng) < 0.005"

  cursor = g.conn.execute(command)
  restaurants = []
  for result in cursor:
    restaurants.append(result['rname'])
  cursor.close()
  context = dict(data = restaurants)
  return render_template("listRestaurantCostAroundMe.html", **context)

####### SQL#5: List the restaurants nearby the subway station ######
@app.route('/listRestaurantAroundSubway')
def listRestaurantAroundSubway():
  names = []
  context = dict(data = names)
  return render_template("listRestaurantAroundSubway.html", **context)

@app.route('/doListRestaurantAroundSubway', methods=['POST'])
def doListRestaurantAroundSubway():
  sid = request.form['sid']

  # SQL command
  command = "SELECT R.rname "
  command += "FROM restaurant R, subway_station S "
  command += "WHERE S.sid='" + sid + "' AND "
  command += "ABS(R.rlat - S.slat) < 0.005 AND "
  command += "ABS(R.rlng - S.slng) < 0.005"

  cursor = g.conn.execute(command)
  restaurants = []
  for result in cursor:
    restaurants.append(result['rname'])
  cursor.close()
  context = dict(data = restaurants)
  return render_template("listRestaurantAroundSubway.html", **context)

####### SQL#6: List my favorite restaurants around me ######
@app.route('/listFavoriteRestaurantAroundMe')
def listFavoriteRestaurantAroundMe():
  names = []
  context = dict(data = names)
  return render_template("listFavoriteRestaurantAroundMe.html", **context)

@app.route('/doListFavoriteRestaurantAroundMe', methods=['POST'])
def doListFavoriteRestaurantAroundMe():
  uid = request.form['uid']

  # SQL command
  command = "SELECT R.rname "
  command += "FROM restaurant R, restaurant_user U, is_favorite S, have H "
  command += "WHERE U.uid='" + uid + "' AND "
  command += "S.uid=U.uid AND "
  command += "S.hid=H.hid AND "
  command += "H.rid=R.rid AND "
  command += "ABS(R.rlat - U.ulat) < 0.005 AND "
  command += "ABS(R.rlng - U.ulng) < 0.005"

  cursor = g.conn.execute(command)
  restaurants = []
  for result in cursor:
    restaurants.append(result['rname'])
  cursor.close()
  context = dict(data = restaurants)
  return render_template("listFavoriteRestaurantAroundMe.html", **context)

@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
