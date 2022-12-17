import mysql.connector 
import json
from dotenv import load_dotenv
import os
load_dotenv() 
mysql_username = os.getenv("MYSQL_USERNAME")
mysql_password = os.getenv("MYSQL_PASSWORD")

connection = mysql.connector.connect(
  host = "localhost",
  port = "3306",
  user= mysql_username,
  password= mysql_password
)

cursor = connection.cursor()

# cursor.execute("CREATE DATABASE `taipei_day_trip_db`")
cursor.execute("USE `taipei_day_trip_db`")

sql_create_table_attraction_info = """
  CREATE TABLE `attraction_info`(
    `id` BIGINT PRIMARY KEY, 
    `name` VARCHAR(255) NOT NULL, 
    `category` VARCHAR(255) NOT NULL, 
    `description` VARCHAR(5000) NOT NULL, 
    `address` VARCHAR(255) NOT NULL, 
    `direction` VARCHAR(1000) NOT NULL, 
    `mrt` VARCHAR(255), 
    `latitude` FLOAT(10, 6) NOT NULL, 
    `longitude` FLOAT(11, 6) NOT NULL
  );
"""

sql_create_table_image = """
  CREATE TABLE `image`(
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
    `attraction_id` BIGINT,
    `url` VARCHAR(1000) NOT NULL,
    FOREIGN KEY (`attraction_id`) REFERENCES `attraction_info`(`id`)
  );
"""

# cursor.execute(sql_create_table_attraction_info)
# cursor.execute(sql_create_table_image)

with open("taipei-attractions.json", encoding="UTF-8") as file:
  data = json.load(file)
  attractions = data["result"]["results"]
  
  # table name: attraction_info
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

    sql_attraction = """
      INSERT INTO `attraction_info` 
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    val_attraction = (id, name, category, description, address, direction, mrt, latitude, longitude)
    cursor.execute(sql_attraction, val_attraction)
    connection.commit()

    # table name: image
    for url in attraction["file"].split("https://"):
      if ".jpg" in url.lower() or ".png" in url.lower():
        img_id = attraction["_id"]
        img_url = "https://" + url
        sql_image = """
          INSERT INTO `image`(attraction_id, url)
          VALUES (%s, %s)
        """
        val_image = (id, img_url)
        cursor.execute(sql_image, val_image)
        connection.commit()

    
connection.close()
cursor.close()
