import sqlite3
from connect import connection

def insertClassroom():
    """
    classroom table
    insert some default classroom(["EA" , "EB" , "EC" , "ED" , "EE", "SA", "SB", "SC", "AC", "A", "AB", "HA", "EO"] 101 ~ 120 , capacity:50)
    """
    record = []
    sql = "INSERT INTO classroom (building, roomname , capacity) VALUES (%s, %s , %s)"
    build = ["EA" , "EB" , "EC" , "ED" , "EE", "SA", "SB", "SC", "AC", "A", "AB", "HA", "EO"]
    for b in build:
        for story in range(101,121):
                name = b + str(story)
                l = [b , name , "50"]
                record.append(l)
    connection.ping(reconnect = True)
    with connection.cursor() as cursor:
        cursor.executemany(sql,record)
        connection.commit()