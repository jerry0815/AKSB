import os
import psycopg2
from psycopg2.extras import DictCursor
# Connect to the database(aws)

#connection = sqlite3.connect('mydatabase.db', check_same_thread=False)
connection = psycopg2.connect("host='database-1.cyg90vgh0c5y.us-east-1.rds.amazonaws.com' password='alex40713' dbname='postgres' user='postgres'",cursor_factory=DictCursor)