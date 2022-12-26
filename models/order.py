from models.mysql_db import Database

class Order:
  def select_data_from_booking_list(user_email):
    sql = """
      SELECT * 
      FROM `user_booking_list` 
      WHERE user_email = %s;
    """
    value = (user_email,)
    result = Database.fetch_all_data(sql, value)
    return result

  def insert_data_into_orders(value):
    sql = """
        INSERT INTO 
        `orders`(
          `order_number`, 
          `user_email`, 
          `prime`, 
          `total_price`, 
          `contact_name`, 
          `contact_email`, 
          `contact_phone`) 
        VALUES(%s, %s, %s, %s, %s, %s, %s);
      """
    result = Database.update_data(sql, value)
    return result
  
  def insert_data_into_order_itinerary_detail(value):
    try:
      sql = """
        INSERT INTO 
        `order_itinerary_detail`(
          `order_number`, 
          `attraction_id`, 
          `image`, 
          `date`, 
          `time`, 
          `price`) 
        VALUES(%s, %s , %s, %s , %s, %s);
      """
      Database.update_data(sql, value)
    except:
      return False
    return True

  def delete_booking_list_by_email(user_email):
    try:
      sql = """
          DELETE FROM `user_booking_list` 
          WHERE `user_email` = %s;
        """
      value = (user_email, )
      Database.update_data(sql, value)
    except:
      return False
    return True
  
  def search_order_number(order_number):
    sql = """
      SELECT 
        `orders`.`user_email`, 
        `orders`.`total_price`,  
        `orders`.`contact_name`, 
        `orders`.`contact_email`, 
        `orders`.`contact_phone`, 
        `order_itinerary_detail`.`attraction_id`, 
        `attraction_info`.`name`, 
        `attraction_info`.`address`, 
        `order_itinerary_detail`.`image`,  
        `order_itinerary_detail`.`date`,  
        `order_itinerary_detail`.`time`,  
        `order_itinerary_detail`.`price`
      FROM (`orders` 
        INNER JOIN `order_itinerary_detail` 
        ON `orders`.`order_number` = `order_itinerary_detail`.`order_number`
        )
      INNER JOIN `attraction_info` 
      ON `order_itinerary_detail`.`attraction_id`=`attraction_info`.`id`
      WHERE `orders`.`order_number`= %s;
    """

    value = (order_number,)
    result = Database.fetch_all_data(sql, value)
    return result