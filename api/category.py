from flask import *
from models.mysql_connector import pool

category = Blueprint(
	"category", 
	__name__, 
	static_folder="static", 
	template_folder="templates")


# -----------------------------------------------------

@category.route("/api/categories") 
def api_categories():
	try:
		connection = pool.get_connection()
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
