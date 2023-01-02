from flask import *
from models.category import Category

category = Blueprint(
	"category", 
	__name__, 
	static_folder="static", 
	template_folder="templates")


# -----------------------------------------------------

@category.route("/api/categories", methods=["GET"]) 
def api_categories():
	result = Category.query_categories()
	categories = []
	if result:
		for category in result:
			categories.append(category[0])
		return {"data": categories}, 200
	else:
		return {
			"error": True,
			"message": "Server error"
		}, 500