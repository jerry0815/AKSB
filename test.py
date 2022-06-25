import psycopg2
from psycopg2.extras import DictCursor
DATABASES = {
"default": {
"ENGINE": "django.db.backends.postgresql_psycopg2",
"NAME": "postgres",
"USER" : "postgres",
"PASSWORD" : "alex40713",
"HOST" : "database-1.cyg90vgh0c5y.us-east-1.rds.amazonaws.com",
"PORT" : "5432",
}
}
connection = psycopg2.connect("host='database-1.cyg90vgh0c5y.us-east-1.rds.amazonaws.com' password='alex40713' dbname='postgres' user='postgres'",cursor_factory=DictCursor)
cursor = connection.cursor()
cursor.execute(
'''CREATE TABLE record
(recordID SERIAL  PRIMARY KEY,
title VARCHAR NOT NULL,
participant VARCHAR,
startDate DATE NOT NULL,
startSection INT NOT NULL,
endDate DATE NOT NULL,
endSection INT NOT NULL,
CR_ID INT NOT NULL,
B_ID INT NOT NULL,
type INT);''')
"""
cursor.execute(
'''CREATE TABLE test
(userID SERIAL PRIMARY KEY,
userName TEXT NOT NULL,
password TEXT NOT NULL,
email TEXT NOT NULL,
identity INT NOT NULL);''')
sql = "INSERT INTO test (userName, password , email , identity ) VALUES (%s,%s,%s,%s)"
user = ["Jerry" ,  "123456789" , "jerrylulala@gmail.com", 0 ]
cursor.execute(sql,user)"""
connection.commit()
print(connection)
