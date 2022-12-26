from mysql.connector.pooling import MySQLConnectionPool
from routes import mysql_username, mysql_password

pool = MySQLConnectionPool(
  pool_name = "mypool",
  pool_size=32,
  host="localhost",
  port="3306", 
  user=mysql_username, 
  password=mysql_password, 
  database="taipei_day_trip_db"
)

class Database:
  def fetch_all_data(sql, value=()):
    try: 
      connection = pool.get_connection()
      cursor = connection.cursor()
      cursor.execute(sql, value)
      result = cursor.fetchall()
      return result
    except:
      return "error"
    finally:
      cursor.close()
      connection.close()

  def fetch_one_data(sql, value=()):
    try: 
      connection = pool.get_connection()
      cursor = connection.cursor()
      cursor.execute(sql, value)
      result = cursor.fetchone()
      return result
    except:
      return "error"
    finally:
      cursor.close()
      connection.close()

  def update_data(sql, value=()):
    try:
      connection = pool.get_connection()
      cursor = connection.cursor()
      cursor.execute(sql, value)
      connection.commit()
    except:
      return "error"
    finally:
      cursor.close()
      connection.close()


