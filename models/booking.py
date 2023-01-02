from models.mysql_db import Database

class Booking:
  def query_booking_list_by_email(user_email):
    sql = """
        SELECT 
          `user_booking_list`.`id`, 
          `user_booking_list`.`attraction_id`, 
          `attraction_info`.`name`, 
          `attraction_info`.`address`, 
          `user_booking_list`.`image`, 
          `user_booking_list`.`date`, 
          `user_booking_list`.`time`, 
          `user_booking_list`.`price`
        FROM `user_booking_list` 
        INNER JOIN `attraction_info` 
        ON `user_booking_list`.`attraction_id`=`attraction_info`.`id` 
        WHERE `user_email` = %s;
      """
    value = (user_email,)
    result = Database.fetch_all_data(sql, value)
    return result
  
  def query_attraction_image(attraction_id):
    sql = """ 
      SELECT `url` 
      FROM `image` 
      WHERE `attraction_id` = %s 
      GROUP BY `attraction_id`;
    """
    value = (attraction_id, )
    result = Database.fetch_one_data(sql, value)
    return result

  def query_booking_datetime(user_email):
    sql = """
      SELECT 
        `date`, 
        `time` 
      FROM `user_booking_list` 
      WHERE `user_email` = %s;
      """
    value = (user_email, )

    result = Database.fetch_all_data(sql, value)
    return result
  
  def insert_booking_info(value):
    try:
      sql = """
        INSERT INTO 
          `user_booking_list`(`user_email`, `attraction_id`, `image`, `date`, `time`, `price`) 
        VALUES(%s, %s, %s, %s, %s, %s);
        """
      Database.update_data(sql, value)
    except:
      return False
    return True

  def select_email_from_booking_list(booking_id):
    sql = """ 
      SELECT user_email 
      FROM `user_booking_list` 
      WHERE `id` = %s;
    """
    value = (booking_id, )
    result = Database.fetch_one_data(sql, value)
    return result
  
  def delete_booking_list_by_id(booking_id):
    try:
      sql = """
        DELETE FROM `user_booking_list` 
        WHERE `id` = %s;
      """
      value = (booking_id,)
      Database.update_data(sql, value)
    except:
      return False
    return True