from models.mysql_db import Database

class Register:
  def check_if_user_exists(email):
    sql = """
      SELECT user.email 
      FROM user 
      WHERE email = %s;
    """
    value = (email,)
    result = Database.fetch_one_data(sql, value)
    return result
  
  def insert_user_data(value):
    try:
      sql = """
        INSERT INTO user(name, email, password) 
        VALUES (%s, %s, %s)
      """
      Database.update_data(sql, value)
    except:
      return False
    return True

class Login:
  def select_user_by_email(email):
    sql = """
      SELECT * 
      FROM user 
      WHERE email= %s
      """
    value = (email, )
    result = Database.fetch_one_data(sql, value)
    return result