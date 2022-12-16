from flask import *
import api.mysql_connector as connector

category = Blueprint(
	"category", 
	__name__, 
	static_folder="static", 
	template_folder="templates")

cnxpool = connector.connect()

# -----------------------------------------------------

@category.route("/api/categories") 
def api_categories():
	try:
		connection = cnxpool.get_connection()
		cursor = connection.cursor()
		sql = """
			SELECT DISTINCT `category` 
			FROM `attraction_info`;
			"""
		cursor.execute(sql)
		database= cursor.fetchall()
		categories = []
		for category in database:
			categories.append(category[0])
		return {"data": categories}, 200
	except:
		return {
			"error": True,
			"message": "Error"}, 500
	finally:
		cursor.close()
		connection.close()
