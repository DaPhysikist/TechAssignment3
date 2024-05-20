# Add the necessary imports
import mysql.connector as mysql
import os
from dotenv import load_dotenv

load_dotenv()   #Load environment file

# Read Database connection variables
db_host = "localhost"
db_user = "root"
db_pass = os.environ['MYSQL_ROOT_PASSWORD']

# Connect to the db and create a cursor object
db = mysql.connect(user=db_user, password=db_pass, host=db_host)
cursor = db.cursor()

cursor.execute("CREATE DATABASE if not exists TechAssignment3")  #create database
cursor.execute("USE TechAssignment3")

cursor.execute("drop table if exists Menu_Items;")   #creates Menu_Items table with fields, drops table if it exists already
try:
   cursor.execute("""
   CREATE TABLE Menu_Items(
       item_id          integer  AUTO_INCREMENT PRIMARY KEY,
       item_name        TEXT NOT NULL,
       price       DECIMAL(12,2) NOT NULL
   );
 """)
except RuntimeError as err:
   print("runtime error: {0}".format(err))

cursor.execute("drop table if exists Orders;")   #creates Orders table with fields, drops table if it exists already
try:
   cursor.execute("""
   CREATE TABLE Orders(
       order_id          integer  AUTO_INCREMENT PRIMARY KEY,
       item_id          integer REFERENCES Menu_Items(item_id),
       customer_name        VARCHAR(50) NOT NULL,
       quantity       integer NOT NULL,
       status    VARCHAR(50) NOT NULL
   );
 """)
except RuntimeError as err:
   print("runtime error: {0}".format(err))

db.commit()  #finishes database initialization
db.close()