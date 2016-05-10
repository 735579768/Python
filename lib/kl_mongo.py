from pymongo import MongoClient
conn = client = MongoClient('localhost', 27017)
db = conn.kelidb #连接库
#db.authenticate("tage","123")
print(db)