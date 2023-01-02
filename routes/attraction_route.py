from flask import *
from models.attraction import Attraction

attraction = Blueprint(
	"attraction", 
	__name__, 
	static_folder="static", 
	template_folder="templates")


# -----------------------------------------------------

@attraction.route("/api/attractions", methods=["GET"])
def get_attractions():
	keyword = request.args.get("keyword")
	page = request.args.get("page", type=int)
	page_size = 12
	if keyword: 
		attractions = Attraction.query_attraction_by_keyword_and_page(keyword, page, page_size)
	else:
		attractions = Attraction.query_attraction_by_page(page, page_size)
	
	attractions_info = []

	if attractions != "error":
		for index, data in enumerate(attractions):
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

		if len(attractions) <= 12:
			next_page = None
		else:
			next_page = page + 1
		return {
			"nextPage": next_page ,
			"data": attractions_info
		}, 200
	return {
			"error": True,
			"message": "Server error"
		}, 500
	

# -----------------------------------------------------

@attraction.route("/api/attraction/<attractionId>", methods=["GET"]) 
def get_attraction_by_id(attractionId):
	if attractionId.isdigit():
		attractionId = int(attractionId)
		result = Attraction.query_attraction_by_id(attractionId)
		if result != "error":
			if result:
				attraction_info = {
				"id": result[0],
				"name": result[1],
				"category": result[2],
				"description": result[3],
				"address": result[4],
				"transport": result[5],
				"mrt": result[6],
				"lat": float(result[7]),
				"lng": float(result[8]),
				"images": result[9].split(",")
				}
				return {
					"data": attraction_info
				}, 200
			else:
				return {
					"error": True,
					"message": "This ID doesn't exist"
				}, 400
		return {
			"error": True,
			"message": "Server error"
			}, 500
	else:
		return {
			"error": True,
			"message": "This ID doesn't exist"
		}, 400