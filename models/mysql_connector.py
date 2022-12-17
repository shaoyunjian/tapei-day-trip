import os
from dotenv import load_dotenv
load_dotenv() 
mysql_username = os.getenv("MYSQL_USERNAME")
mysql_password = os.getenv("MYSQL_PASSWORD")

from mysql.connector.pooling import MySQLConnectionPool

pool = MySQLConnectionPool(
  pool_name = "mypool",
  pool_size=32,
  host="localhost",
  port="3306", 
  user=mysql_username, 
  password=mysql_password, 
  database="taipei_day_trip_db"
)