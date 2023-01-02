from flask import *
from models.user import Register, Login
from models.regex import Regex
from routes import jwt_key, bcrypt
import jwt

user = Blueprint(
  "user", 
  __name__, 
  static_folder="static", 
  template_folder="templates")


# ----------------- Register ---------------------

@user.route("/api/user", methods=["POST"])
def register():
  try:
    data = request.get_json()
    input_name = data["name"]
    input_email = data["email"]
    input_password = data["password"]

    email_data = Register.check_if_user_exists(input_email)

    # register validation
    register_validation_result = Regex.registration_validation(input_name, input_email, input_password)
    
    if register_validation_result["message"] == "invalid name":
      return register_validation_result, 400
    elif register_validation_result["message"] == "invalid email":
      return register_validation_result, 400
    elif register_validation_result["message"] == "invalid password":
      return register_validation_result, 400
    elif not email_data:
      hashed_password = bcrypt.generate_password_hash(input_password)
      
      value = (input_name, input_email, hashed_password)
      Register.insert_user_data(value)
      return {"ok": True}, 200
    else:
      return {
        "error": True,
        "message": "email already exists"
      }, 400
  except:
    return {
      "error": True,
      "message": "error"
    }, 500


# ---------- Check if user is logged in -------------

@user.route("/api/user/auth", methods=["GET"])
def logged_in_user_info():
  try:
    encoded_jwt= request.cookies.get("token")
    if encoded_jwt:
      decoded_jwt = jwt.decode(encoded_jwt, jwt_key, algorithms="HS256")
      return {
        "data": {
          "id": decoded_jwt["id"],
          "name": decoded_jwt["name"],
          "email": decoded_jwt["email"]
        }
      }, 200
    else:
      return {"data": None}, 200
  except jwt.exceptions.InvalidTokenError:
    return {"data": None}, 401


# ---------------- Login ---------------------

@user.route("/api/user/auth", methods=["PUT"])
def login():
  try:
    data = request.get_json()
    input_email = data["email"]
    input_password = data["password"]

    login_validation_result = Regex.login_validation(input_email, input_password)
    if login_validation_result["message"] == "invalid email":
      return login_validation_result, 400
    elif login_validation_result["message"] == "invalid password":
      return login_validation_result, 400

    user_data = Login.select_user_by_email(input_email)
    if user_data:
      if not input_email or not input_password:
        return {
          "error": True,
          "message": "empty input"
        }, 400
      elif user_data:
        if bcrypt.check_password_hash(user_data[3], input_password):
          payload = {
          "id": user_data[0],
          "name": user_data[1],
          "email": user_data[2]
          }
          encoded_jwt = jwt.encode(payload, jwt_key, algorithm="HS256")
          response = make_response({"ok": True})
          response.set_cookie(key="token", value=encoded_jwt, max_age=24*60*60*7)
          return response, 200
        else:
          return {
            "error": True,
            "message": "email or password is incorrect"
          }, 400
    else:
      return {
            "error": True,
            "message": "email or password is incorrect"
          }, 400
  except:
    return {
      "error": True,
      "message": "error"
    }, 500

# ------------------- Logout -------------------

@user.route("/api/user/auth", methods=["DELETE"])
def logout():
  response = make_response({"ok": True})
  response.delete_cookie("token")
  return response, 200