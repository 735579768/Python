from pymongo import MongoClient
conn = MongoClient('localhost', 27017)
db = conn.kelidb #连接库
#db.authenticate("tage","123")
#
print(db.col.find().count())

for item in db.col.find():
    print(item)