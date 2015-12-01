import os,kl_log
import time  
import tarfile  
import zipfile
import threading
  
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
db_name=['union.0yuanwang.com','0yuanwang_db','5257','blog','ruzhouba','shijiyaolan_db','sjyl','sjyl_hb','sjyl_hc','sjyl_jx','sjyl_qx','sjyl_zz','taier','zhaokeli_db']  
db_charset="utf8"

def bakmysql(db_name,sss):
    try:
        global baknum
        baknum=baknum+1
        db_backup_name=r".\data\bakmysql\%s_%s.sql"%(time.strftime("%Y-%m-%d_%H-%M-%S"),db_name)  
        if os.path.exists(os.path.dirname(db_backup_name))==False :
            os.makedirs(os.path.dirname(db_backup_name))
        zip_src = db_backup_name  
        zip_dest = zip_src + ".zip"

        print("开始备份数据库:%s..."%db_name);  
        os.system("mysqldump -h%s -u%s -p%s %s --default_character-set=%s > %s" %(db_host, db_user, db_passwd, db_name, db_charset, db_backup_name))  
        print("开始压缩数据库:%s..."%db_name)  
        #zip_files(zip_src,zip_dest)
        f = zipfile.ZipFile(zip_dest, 'w' ,zipfile.ZIP_DEFLATED)   
        f.write(zip_src)  
        f.close()
        os.remove(zip_src)
        print("数据库%s备份完成!"% db_name)
        baknum=baknum-1
    except:
        baknum=baknum-1
        kl_log.write('备份数据库%s时出错'%db_name,'bakmysql')
    
if __name__ == "__main__":
    baknum=0
    for i in db_name:
        threading.Thread(target=bakmysql,args=(i,'')).start()
        
    while baknum != 0:
        pass
    
    try:
        input("所有数据库备份完成,按任意键继续...") 
    except:
        pass
     
