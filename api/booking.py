from flask import *
from models.mysql_connector import pool
import os
from dotenv import load_dotenv
load_dotenv() 
import jwt
jwt_key =os.getenv("JWT_KEY")

booking = Blueprint(
  "booking", 
  __name__, 
  static_folder="static", 
  template_folder="templates")


#------------- Check itinerary/booking cart -------------

@booking.route("/api/booking", methods=["GET"])
def check_itinerary():
  try:
    connection = pool.get_connection()
    cursor = connection.cursor()

    encoded_jwt= request.cookies.get("token")
    decoded_jwt = jwt.decode(encoded_jwt, jwt_key, algorithms="HS256")
    if decoded_jwt: 
      user_email = decoded_jwt["email"]

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
      
      cursor.execute(sql, value)
      booking_cart_data = cursor.fetchall()
      if not booking_cart_data:
        return {"data": None}, 200
      else:
        all_cart_data = []
        for cart_data in booking_cart_data:
          data = {
            "booking_id": cart_data[0],
            "attraction": {
              "id": cart_data[1],
              "name": cart_data[2],
              "address": cart_data[3],
              "image": cart_data[4],
            },
            "date": cart_data[5],
            "time": cart_data[6],
            "price": cart_data[7]
          }
          all_cart_data.append(data)
        
        return {"data": all_cart_data}, 200
    else:
      return {
        "error": True,
        "message": "user not logged in"
      }, 403
  except jwt.exceptions.InvalidTokenError:
    return {
    "error": True,
    "message": "invalid token"
    }, 401
  finally:
    cursor.close()
    connection.close()


#---------------- Add an itinerary ------------------

@booking.route("/api/booking", methods=["POST"])
def add_itinerary():
  data = request.get_json()
  attraction_id = data["attractionId"]
  date = data["itineraryDate"]
  time = data["itineraryTime"]
  price = data["itineraryPrice"]

  try:
    connection = pool.get_connection()
    cursor = connection.cursor()
    sql = """ 
      SELECT `url` 
      FROM `image` 
      WHERE `attraction_id` = %s 
      GROUP BY `attraction_id`;
    """
    value = (attraction_id, )
    cursor.execute(sql, value)
    imageData = cursor.fetchone()
    image = imageData[0]

    encoded_jwt= request.cookies.get("token")
    decoded_jwt = jwt.decode(encoded_jwt, jwt_key, algorithms="HS256")
    if decoded_jwt:
      user_email = decoded_jwt["email"]
      sql = """
        SELECT 
          `date`, 
          `time` 
        FROM `user_booking_list` 
        WHERE `user_email` = %s;
        """
      value = (user_email, )
      cursor.execute(sql, value)
      itineraryData = cursor.fetchall()
      
      for dateTime in itineraryData:
        if dateTime[0] == date and dateTime[1] == time:
          return {
            "error": True,
            "message": "data already exists"
          }, 400
   
      if date and time and price:
        sql = """
        INSERT INTO 
          `user_booking_list`(`user_email`, `attraction_id`, `image`, `date`, `time`, `price`) 
        VALUES(%s, %s, %s, %s, %s, %s);
        """
        value = (user_email, attraction_id, image, date, time, price)
        cursor.execute(sql, value)
        connection.commit()
        return {"ok": True}, 200
      else:
        return {
          "error": True,
          "message": "input error"
        }, 400
    else:
      return {
        "error": True,
        "message": "user not logged in"
      }, 403
  except jwt.exceptions.InvalidTokenError:
    return {
    "error": True,
    "message": "invalid token"
    }, 401
  except:
    return {
    "error": True,
    "message": "error"
    }, 500
  finally:
    cursor.close()
    connection.close()


# ---------------- Delete an itinerary ------------------

@booking.route("/api/booking", methods=["DELETE"])
def delete_itinerary():
  data = request.get_json()
  booking_id = data["booking_id"]
  
  try:
    connection = pool.get_connection()
    cursor = connection.cursor()

    sql = """ 
      SELECT user_email 
      FROM `user_booking_list` 
      WHERE `id` = %s;
    """
    value = (booking_id, )
    cursor.execute(sql, value)
    db_current_user_email = cursor.fetchone()

    encoded_jwt= request.cookies.get("token")
    decoded_jwt = jwt.decode(encoded_jwt, jwt_key, algorithms="HS256")

    if decoded_jwt["email"] == db_current_user_email[0]:
      sql = """
        DELETE FROM `user_booking_list` 
        WHERE `id` = %s;
      """
      value = (booking_id,)
      cursor.execute(sql, value)
      connection.commit()
      return {"ok": True}, 200
    else:
      return {
        "error": True,
        "message": "user not logged in"
      }, 403
  except jwt.exceptions.InvalidTokenError:
    return {
    "error": True,
    "message": "invalid token"
    }, 401
  except:
    return {
      "error": True,
      "message": "error"
    }, 500
