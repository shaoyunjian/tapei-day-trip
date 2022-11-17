from flask import *
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"]=False

# Pages
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")

@app.route("/booking")
def booking():
	return render_template("booking.html")

@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

# -----------------------------------------------------

from dotenv import load_dotenv
import os
load_dotenv() 
USER=os.getenv("USER")
PASSWORD=os.getenv("PASSWORD")

from mysql.connector.pooling import MySQLConnectionPool
cnxpool = MySQLConnectionPool(
  pool_name = "mypool",
  pool_size=32,
  host="localhost",
  port="3306", 
  user=USER, 
  password=PASSWORD, 
  database="taipei_day_trip_db"
)

# -----------------------------------------------------
# API

@app.route("/api/attractions")
def api_attractions():
	try:
		cnx = cnxpool.get_connection()
		cursor = cnx.cursor()
		keyword = request.args.get("keyword")
		page = request.args.get("page", type=int)
		page_size = 12
		if keyword: 
			sql = "SELECT * FROM `attraction_info` WHERE `category` = %s or `name` LIKE %s LIMIT %s OFFSET %s;"
			values = (keyword, "%"+keyword+"%", page_size, page * page_size)
			cursor.execute(sql, values)
			database = cursor.fetchall()
			print(database)
			values_next_page = (keyword, "%"+keyword+"%", page_size, (page + 1) * page_size)
			cursor.execute(sql, values_next_page)
			database_next_page = cursor.fetchall()
		else:
			sql = "SELECT * FROM `attraction_info` LIMIT %s OFFSET %s;"
			values = (page_size, page * page_size)
			cursor.execute(sql, values)
			database = cursor.fetchall()
			values_next_page = (page_size, (page + 1) * page_size)
			cursor.execute(sql, values_next_page)
			database_next_page = cursor.fetchall()

		attractions_info = []
		for data in database:
			attraction_info = {
				"id": data[0],
				"name": data[1],
				"category": data[2],
				"description": data[3],
				"address": data[4],
				"transport": data[5],
				"mrt": data[6],
				"lat": data[7],
				"lng": data[8],
				"images": data[9].split(",")
			}
			attractions_info.append(attraction_info)

		if len(database_next_page) == 0:
			next_page = None
		else:
			next_page = page + 1

		return {"nextPage": next_page ,"data": attractions_info}, 200
	except:
		return {
			"error": True,
			"message": "Error"}, 500
	finally:
		cursor.close()
		cnx.close()

# -----------------------------------------------------

@app.route("/api/attraction/<attractionId>") 
def api_attraction_id(attractionId):
	if attractionId.isdigit():
		attractionId = int(attractionId)
	else:
		return {
			"error": True,
			"message": "This ID doesn't exist"
		}, 400

	try:
		cnx = cnxpool.get_connection()
		cursor = cnx.cursor()
		sql = "SELECT * FROM `attraction_info` WHERE id = %s;"
		values = (attractionId,)
		cursor.execute(sql, values)
		database = cursor.fetchone()
		if database:
			print(database)
			database = list(database)
			attraction_info = {
			"id": database[0],
			"name": database[1],
			"category": database[2],
			"description": database[3],
			"address": database[4],
			"transport": database[5],
			"mrt": database[6],
			"lat": database[7],
			"lng": database[8],
			"images": database[9].split(",")
			}
			return {"data": attraction_info}, 200
		else:
			return {
				"error": True,
				"message": "This ID doesn't exist"
			}, 400
	except:
		return {
			"error": True,
			"message": "Error"}, 500
	finally:
			cursor.close()
			cnx.close()

# -----------------------------------------------------

@app.route("/api/categories") 
def api_categories():
	try:
		cnx = cnxpool.get_connection()
		cursor = cnx.cursor()
		sql = "SELECT DISTINCT `category` FROM `attraction_info`;"
		cursor.execute(sql)
		database= cursor.fetchall()
		categories = []
		for category in database:
			categories.append(str(category).replace("('", "").replace("',)", "").replace("\\u3000", "　"))
		return {"data": categories}, 200
	except:
		return {
			"error": True,
			"message": "Error"}, 500
	finally:
		cursor.close()
		cnx.close()


app.run(host="0.0.0.0", port=3000)