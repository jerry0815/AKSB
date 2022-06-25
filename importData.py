from connect import connection
import pandas as pd
import time

df = pd.read_csv("random_record.csv")
vals = df.values
records = vals.tolist()
sql = "INSERT INTO `record` (`title`, `CR_ID`,`startDate` , `startSection` , `endDate` , `endSection` , `participant` ,  `B_ID` , `type`) \
VALUES (?,?,?,?,?,?,?,?,?)"
cursor = connection.cursor()
start = time.time()
cursor.executemany(sql,records)
connection.commit()
end = time.time()
print(format(end-start))