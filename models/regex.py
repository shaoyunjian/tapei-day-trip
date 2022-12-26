import re

class Regex:
  def registration_validation(name, email, password):
    name_regex = r"^.{1,10}$"
    email_regex = r"[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}"
    password_regex = r"^[a-zA-Z0-9]{8,16}$"
    
    name_match = re.match(name_regex, name)
    email_match = re.match(email_regex, email)
    password_match = re.match(password_regex, password)
      
    if not name_match:
      return {
        "error": True, 
        "message": "invalid name"
      }
    elif not email_match:
      return {
        "error": True, 
        "message": "invalid email"
      }
    elif not password_match:
      return {
        "error": True, 
        "message": "invalid password"
      }
    return {
      "response": "ok", 
      "message": "valid data"
    }

  def login_validation(email, password):
    email_regex = r"[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}"
    password_regex = r"^[a-zA-Z0-9]{8,16}$"
    
    email_match = re.match(email_regex, email)
    password_match = re.match(password_regex, password)
      
    if not email_match:
      return {
        "error": True, 
        "message": "invalid email"
      }
    elif not password_match:
      return {
        "error": True, 
        "message": "invalid password"
      }
    return {
      "response": "ok", 
      "message": "valid data"
    }