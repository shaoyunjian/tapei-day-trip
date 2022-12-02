from dotenv import load_dotenv
import os
load_dotenv() 
USER=os.getenv("USER")
PASSWORD=os.getenv("PASSWORD")

from mysql.connector.pooling import MySQLConnectionPool

def connect():
  return MySQLConnectionPool(
    pool_name = "mypool",
    pool_size=32,
    host="localhost",
    port="3306", 
    user=USER, 
    password=PASSWORD, 
    database="taipei_day_trip_db"
  )