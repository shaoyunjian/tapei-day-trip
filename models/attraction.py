from models.mysql_db import Database

class Attraction:
  def query_attraction_by_keyword_and_page(keyword, page, page_size):
    try:
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
      value = (keyword, "%"+keyword+"%", page_size + 1, page * page_size)
      result = Database.fetch_all_data(sql, value)
      return result
    except:
      return "error"
  
  def query_attraction_by_page(page, page_size):
    try:
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
      value = (page_size + 1, page * page_size)
      result = Database.fetch_all_data(sql, value)
      return result
    except:
      return "error"

  def query_attraction_by_id(attraction_id):
    try:
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
      value = (attraction_id,)
      result = Database.fetch_one_data(sql, value)
      return result
    except:
      return "error"