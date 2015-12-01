import os  
import time  
import tarfile  
import zipfile  
  
''''' 
mysqldump 
Usage: mysqldump [OPTIONS] database [tables] 
OR     mysqldump [OPTIONS] --databases [OPTIONS] DB1 [DB2 DB3...] 
OR     mysqldump [OPTIONS] --all-databases [OPTIONS] 
For more options, use mysqldump --help 
'''  
db_host="116.255.214.72"  
db_user="root"  
db_passwd="adminrootkl"  
db_name="0yuanwang_db"  
db_charset="utf8"  
db_backup_name=r".\data\bakmysql\%s_%s.sql" %(db_name,time.strftime("%Y%m%d%H%M"))  
if os.path.exists(os.path.dirname(db_backup_name))==False :
    os.makedirs(os.path.dirname(db_backup_name))
zip_src = db_backup_name  
zip_dest = zip_src + ".zip"  
  
def zip_files():  
    f = zipfile.ZipFile(zip_dest, 'w' ,zipfile.ZIP_DEFLATED)   
    f.write(zip_src)  
    f.close()   
      
if __name__ == "__main__":  
    print("开始备份数据库:%s..."%db_name);  
    os.system("mysqldump -h%s -u%s -p%s %s --default_character-set=%s > %s" %(db_host, db_user, db_passwd, db_name, db_charset, db_backup_name))  
    print("开始压缩数据库文件...")  
    zip_files()  
    input("数据库备份完成")  
