import os, jwt
from dotenv import load_dotenv
load_dotenv() 

jwt_key = os.getenv("JWT_KEY")
partner_key = os.getenv("PARTNER_KEY")
merchant_id = os.getenv("MERCHANT_ID")
mysql_username = os.getenv("MYSQL_USERNAME")
mysql_password = os.getenv("MYSQL_PASSWORD")

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()