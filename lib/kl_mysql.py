'''
#返回单行数据
result = cursor.fetchone()
#返回所有数据
result = cursor.fetchall()

获得游标
cursor = conn.cursor(cursorclass=MySQLdb.cursors.Cursor)
cursorclass参数:
MySQLdb.cursors.Cursor， 默认值，执行SQL语句返回List，每行数据为tuple
MySQLdb.cursors.DictCursor， 执行SQL语句返回List，每行数据为Dict
'''
import pymysql
class kl_db(object):
    con=None
    cur=None
    def __init__(self, arg):
        super(ClassName, self).__init__()
        self.arg = arg
    def conn(config):
        if kl_db.con == None :
            kl_db.con=pymysql.connect(host=config['host'],user=config['user'],passwd=config['passwd'],db=config['db'],charset=config['charset'])
        kl_db.cur=kl_db.con.cursor(pymysql.cursors.DictCursor);#获取操作游标
    def select(sql):
        sta=kl_db.cur.execute(sql);
        kl_db.con.commit()
        return kl_db.cur
    def execute():
        sta=kl_db.cur.execute(sql);
        kl_db.con.commit()
        return sta       
    def close():#关闭所有连接
        kl_db.cur.close();
        kl_db.con.close();

if __name__ == '__main__':
    kl_db.conn({
            'host':'localhost',
            'user':'root',
            'passwd':'adminrootkl',
            'db':'ainiku',
            'charset':'utf8'
        })
    da=kl_db.select('select * from kl_article')
    for a in da:
        print(a)
    print('-------------------------------------')

    da=kl_db.select('select * from kl_article')
    for a in da:
        print(a['title']) # a[1] 表示当前游标所在行的的第2列值，如果是中文则需要处理编码

    kl_db.close()
    input('按任意键继续...')
