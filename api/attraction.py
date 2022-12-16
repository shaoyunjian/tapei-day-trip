from flask import *
import api.mysql_connector as connector

attraction = Blueprint(
	"attraction", 
	__name__, 
	static_folder="static", 
	template_folder="templates")

cnxpool = connector.connect()

# -----------------------------------------------------

@attraction.route("/api/attractions")
def api_attractions():
	try:
		connection = cnxpool.get_connection()
		cursor = connection.cursor()
		keyword = request.args.get("keyword")
		page = request.args.get("page", type=int)
		page_size = 12
		if keyword: 
			sql = """
				SELECT 
					`attraction_info`.*, 
					GROUP_CONCAT(`url`) AS `url`
				FROM `attraction_info`
				INNER JOIN `image`
				ON `attraction_info`.`id`=`image`.`attraction_id`
				WHERE `category` = %s
				OR `name` LIKE %s
				GROUP BY `image`.`attraction_id` 
				ORDER BY `attraction_info`.`id` 
				LIMIT %s OFFSET %s;
				"""
			
			values = (keyword, "%"+keyword+"%", page_size + 1, page * page_size)
			cursor.execute(sql, values)
			database = cursor.fetchall()
		else:
			sql = """
				SELECT 
					`attraction_info`.*, 
					GROUP_CONCAT(`url`) AS `url`
				FROM `attraction_info`
				INNER JOIN `image`
				ON `attraction_info`.`id`=`image`.`attraction_id`
				GROUP BY `image`.`attraction_id` 
				ORDER BY `attraction_info`.`id` 
				LIMIT %s OFFSET %s;
				"""
			values = (page_size + 1, page * page_size)
			cursor.execute(sql, values)
			database = cursor.fetchall()
		
		attractions_info = []
		
		for index, data in enumerate(database):
			if index == 12:
				break
			attraction_info = {
				"id": data[0],
				"name": data[1],
				"category": data[2],
				"description": data[3],
				"address": data[4],
				"transport": data[5],
				"mrt": data[6],
				"lat": float(data[7]),
				"lng": float(data[8]),
				"images": data[9].split(",")
			}
			attractions_info.append(attraction_info)
		
		if len(database) <= 12:
			next_page = None
		else:
			next_page = page + 1

		return {
			"nextPage": next_page ,
			"data": attractions_info
		}, 200
	except:
		return {
			"error": True,
			"message": "Error"
		}, 500
	finally:
		cursor.close()
		connection.close()

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
		connection = cnxpool.get_connection()
		cursor = connection.cursor()
		sql = """
			SELECT 
				`attraction_info`.*, 
				GROUP_CONCAT(`url`) AS `url`
			FROM `attraction_info`
			INNER JOIN `image`
			ON `attraction_info`.`id`=`image`.`attraction_id`
			WHERE attraction_info.id = %s
			GROUP BY `image`.`attraction_id` 
			ORDER BY `attraction_info`.`id` 
			"""
		values = (attractionId,)
		cursor.execute(sql, values)
		database = cursor.fetchone()
		if database:
			attraction_info = {
			"id": database[0],
			"name": database[1],
			"category": database[2],
			"description": database[3],
			"address": database[4],
			"transport": database[5],
			"mrt": database[6],
			"lat": float(database[7]),
			"lng": float(database[8]),
			"images": database[9].split(",")
			}
			return {
				"data": attraction_info
			}, 200
		else:
			return {
				"error": True,
				"message": "This ID doesn't exist"
			}, 400
	except:
		return {
			"error": True,
			"message": "Error"
		}, 500
	finally:
			cursor.close()
			connection.close()

