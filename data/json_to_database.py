import mysql.connector 
import json
from dotenv import load_dotenv
import os
load_dotenv() 
USER=os.getenv("USER")
PASSWORD=os.getenv("PASSWORD")

connection = mysql.connector.connect(
  host = "localhost",
  port = "3306",
  user = USER,
  password = PASSWORD)
cursor = connection.cursor()

# cursor.execute("CREATE DATABASE `taipei_day_trip_db`")
cursor.execute("USE `taipei_day_trip_db`")
# cursor.execute("CREATE TABLE `attraction_info`(`id` BIGINT PRIMARY KEY, `name` VARCHAR(255) NOT NULL, `category` VARCHAR(255) NOT NULL, `description` VARCHAR(5000) NOT NULL, `address` VARCHAR(255) NOT NULL, `direction`  VARCHAR(1000) NOT NULL, `mrt` VARCHAR(255), `latitude` FLOAT(10, 6) NOT NULL, `longitude` FLOAT(11, 6) NOT NULL, `images` VARCHAR(5000));")

with open("taipei-attractions.json", encoding="UTF-8") as file:
  data = json.load(file)
  attractions = data["result"]["results"]
  
  for attraction in attractions:
    id = attraction["_id"]
    name = attraction["name"]
    category = attraction["CAT"]
    description = attraction["description"]
    address = attraction["address"]
    direction = attraction["direction"]
    mrt = attraction["MRT"]
    latitude = attraction["latitude"]
    longitude = attraction["longitude"]
    images = []
    for link in attraction["file"].split("https://"):
      if ".jpg" in link.lower() or ".png" in link.lower():
        imgLink = "https://" + link
        images.append(imgLink)
    images = ",".join(images)

    sql = "INSERT INTO `attraction_info` VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (id, name, category, description, address, direction, mrt, latitude, longitude, images)
    cursor.execute(sql, val)
    connection.commit()


connection.close()
cursor.close()
