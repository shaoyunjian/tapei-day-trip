from flask import Blueprint, request
import api.mysql_connector as connector

attraction = Blueprint("attraction", __name__, static_folder="static", template_folder="templates")

cnxpool = connector.connect()

# -----------------------------------------------------

@attraction.route("/api/attractions")
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

@attraction.route("/api/attraction/<attractionId>") 
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

