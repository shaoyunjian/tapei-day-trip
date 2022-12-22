from flask import *
import requests, os
from datetime import datetime, timezone, timedelta

from models.mysql_connector import pool
from dotenv import load_dotenv
load_dotenv() 
import jwt
jwt_key = os.getenv("JWT_KEY")
partner_key = os.getenv("PARTNER_KEY")
merchant_id = os.getenv("MERCHANT_ID")

order = Blueprint(
  "order", 
  __name__, 
  static_folder="static", 
  template_folder="templates")


# ------------------ create an order -----------------------

@order.route("/api/orders", methods=["POST"])
def create_order():
  try:
    data = request.get_json()
    order_contact_name = data["order"]["contact"]["name"]
    order_contact_email = data["order"]["contact"]["email"]
    order_contact_phone = data["order"]["contact"]["phone"]
    
    if not order_contact_name or not order_contact_email or not order_contact_phone:
      return {
        "error": True,
        "message": "empty input"
      }, 400
    
    encoded_jwt= request.cookies.get("token")
    if not encoded_jwt:
      return {
        "error": True,
        "message": "user not logged in"
      }, 403
    
    decoded_jwt = jwt.decode(encoded_jwt, jwt_key, algorithms="HS256")
    
    # ------------ database ---------------

    connection = pool.get_connection()
    cursor = connection.cursor()

    booking_cart_sql = """
      SELECT * 
      FROM `user_booking_list` 
      WHERE user_email = %s;
    """
    booking_cart_values = (decoded_jwt["email"], )
    
    cursor.execute(booking_cart_sql, booking_cart_values)
    booking_cart_data = cursor.fetchall()
    booking_total_amount = 0
    for item in booking_cart_data:
      booking_total_amount += item[6]
    
    # if the amount of the request does not match the amount recorded in the database, the transaction will fail
    if booking_total_amount != data["order"]["totalAmount"]:
      return {
        "error": True,
        "message": "order error"
      }, 400

    # create order number
    tz_8 = timezone(timedelta(hours=+8))
    current_time = datetime.now(tz_8)
    datetime_string = current_time.strftime("%Y%m%d%H%M%S")
    order_number = datetime_string
    order_status = "unpaid"

    # send request to TapPay
    tappay_url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"

    headers = {
      "Content-Type": "application/json",
      "x-api-key": partner_key
    }

    order_info = {
      "prime": data["prime"],
      "partner_key": partner_key,
      "merchant_id": merchant_id,
      "details":"Taipei Day Trip",
      "amount": data["order"]["totalAmount"],
      "order_number": order_number,
      "cardholder": {
        "phone_number": data["order"]["contact"]["phone"],
        "name": data["order"]["contact"]["name"],
        "email": data["order"]["contact"]["email"]
      }
    }

    response = requests.post(tappay_url, headers = headers, json = order_info).json()
    status_code = response["status"]
    response_msg = response["msg"]

    if status_code == 0:
      order_status = "paid"

      # add order to database
      orders_sql = """
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
      values = (order_number, decoded_jwt["email"], data["prime"], data["order"]["totalAmount"], data["order"]["contact"]["name"], data["order"]["contact"]["email"], data["order"]["contact"]["phone"])
      
      cursor.execute(orders_sql, values)
      connection.commit()

      for item in booking_cart_data:
        booking_attraction_id = item[2]
        booking_attraction_image = item[3]
        booking_itinerary_date = item[4]
        booking_itinerary_time = item[5]
        booking_itinerary_price = item[6]
        booking_total_amount += item[6]

        # add data to table `order_itinerary_detail`
        order_details_sql = """
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
        order_details_values = (order_number, booking_attraction_id, booking_attraction_image, booking_itinerary_date, booking_itinerary_time, booking_itinerary_price)
        
        cursor.execute(order_details_sql, order_details_values)
        connection.commit()

      # delete data from cart
      delete_sql = """
        DELETE FROM `user_booking_list` 
        WHERE `user_email` = %s;
      """
      delete_value = (decoded_jwt["email"],)
      cursor.execute(delete_sql, delete_value)
      connection.commit()

      return {
        "data": {
          "number": order_number,
          "payment": {
            "status": status_code,
            "message": response_msg
          }
        }
      }, 200
    else:
      return {
        "data": {
          "number": order_number,
          "payment": {
            "status": status_code,
            "message": response_msg
          }
        }
      }, 200
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


#---------------- get order number ---------------------

@order.route("/api/order/<order_number>", methods=["GET"])
def get_order_number(order_number):
  try:
    connection = pool.get_connection()
    cursor = connection.cursor()
    
    encoded_jwt= request.cookies.get("token")
    if not encoded_jwt:
      return {
        "error": True,
        "message": "user not logged in"
      }, 403
    
    decoded_jwt = jwt.decode(encoded_jwt, jwt_key, algorithms="HS256")
    user_email = decoded_jwt["email"]

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
    cursor.execute(sql, value)
    order_data = cursor.fetchall()

    if not order_data:
      return {"data": None}, 200
    
    order_email = order_data[0][0]
    if user_email != order_email:
      return {
        "error": True,
        "message": "user not logged in"
      }, 403

    total_amount = order_data[0][1]
    contact_name = order_data[0][2]
    contact_email = order_data[0][3]
    contact_phone = order_data[0][4]
    trip_details = []
    
    if order_data:
      for item in order_data:
        trip = {
          "attraction": {
          "id": item[5],
          "name": item[6],
          "address": item[7],
          "image": item[8]
        },
        "date": item[9],
        "time": item[10],
        "price": item[11]
        }
        trip_details.append(trip)

      return {
        "data": {
          "number": order_number,
          "price": total_amount,
          "trip": trip_details,
          "contact": {
            "name":  contact_name,
            "email":  contact_email,
            "phone":  contact_phone
          },
          "status": 0
        }
      }, 200
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