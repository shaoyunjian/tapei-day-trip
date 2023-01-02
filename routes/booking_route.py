from flask import *
from models.booking import Booking
from routes import jwt_key, jwt

booking = Blueprint(
  "booking", 
  __name__, 
  static_folder="static", 
  template_folder="templates")


#------------- Check itinerary/booking cart -------------

@booking.route("/api/booking", methods=["GET"])
def check_itinerary():
  try:
    encoded_jwt= request.cookies.get("token")
    decoded_jwt = jwt.decode(encoded_jwt, jwt_key, algorithms="HS256")
    if decoded_jwt: 
      user_email = decoded_jwt["email"]
      booking_cart_data = Booking.query_booking_list_by_email(user_email)

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



#---------------- Add an itinerary ------------------

@booking.route("/api/booking", methods=["POST"])
def add_itinerary():
  data = request.get_json()
  attraction_id = data["attractionId"]
  date = data["itineraryDate"]
  time = data["itineraryTime"]
  price = data["itineraryPrice"]

  try:
    imageData = Booking.query_attraction_image(attraction_id)
    image = imageData[0]

    encoded_jwt= request.cookies.get("token")
    decoded_jwt = jwt.decode(encoded_jwt, jwt_key, algorithms="HS256")
    if decoded_jwt:
      user_email = decoded_jwt["email"]
    
      itinerary_data = Booking.query_booking_datetime(user_email)
      
      for datetime in itinerary_data:
        if datetime[0] == date and datetime[1] == time:
          return {
            "error": True,
            "message": "data already exists"
          }, 400
   
      if date and time and price:
        value = (user_email, attraction_id, image, date, time, price)
        result = Booking.insert_booking_info(value)
        if result:
          return {"ok": True}, 200
        else:
          return {
            "error": True,
            "message": "error"
          }, 500
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

# ---------------- Delete an itinerary ------------------

@booking.route("/api/booking", methods=["DELETE"])
def delete_itinerary():
  data = request.get_json()
  booking_id = data["booking_id"]
  
  try:
    db_current_user_email = Booking.select_email_from_booking_list(booking_id)

    encoded_jwt= request.cookies.get("token")
    decoded_jwt = jwt.decode(encoded_jwt, jwt_key, algorithms="HS256")

    if decoded_jwt["email"] == db_current_user_email[0]:
      result = Booking.delete_booking_list_by_id(booking_id)
      if result:
        return {"ok": True}, 200
      else:
        return {
          "error": True, 
          "message": "Server error"}, 500
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
