from models.mysql_db import Database

class Category:
  def query_categories():
    sql = """
			SELECT DISTINCT `category` 
			FROM `attraction_info`;
			"""
    result = Database.fetch_all_data(sql)
    return result