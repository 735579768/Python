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
class mysql(object):

    def __init__(self, arg):
        self.sql=''
        self.sqlparam=[]
        self.prefix=''
        self.sqlconf={
            'action':'',
            'table':'',
            'where':'',
            'order':'',
            'limit':'',
            'field':'*'
        }
        #要操作的数据
        self.data={}
        self.con=None
        self.cur=None
        self.arg = arg
        self.conn(arg)
    def conn(self,config):
        self.prefix=config['prefix'];
        if self.con == None :
            self.con=pymysql.connect(host=config['host'],user=config['user'],passwd=config['passwd'],db=config['db'],charset=config['charset'])
        self.cur=self.con.cursor(pymysql.cursors.DictCursor);#获取操作游标
    #返回一个记录集
    def __getcur(self):
        if self.sql=='':
            self.__zuhesqu()
        self.cur.execute(self.sql)
        self.con.commit()
        return self.cur

    #返回执行结果记录数
    def __execute(self):
        if self.sql=='':
            self.__zuhesqu()
        try:
            num=0
            if len(self.sqlparam):
                num=self.cur.execute(self.sql,self.sqlparam)
            else:
                num=self.cur.execute(self.sql)
            self.con.commit()
            return num
        except pymysql.err.InternalError as e:
            print(e)
            print('SQL:[%s]'%self.sql)
            return 0
        except pymysql.err.ProgrammingError as e:
            print(e)
            print('SQL:[%s]'%self.sql)
            return 0

    #组合sql语句
    def __zuhesqu(self):
        self.sqlparam=[]
        action=self.sqlconf['action'];
        table=self.sqlconf['table'];
        where=self.sqlconf['where'];
        order=self.sqlconf['order'];
        limit=self.sqlconf['limit'];
        field=self.sqlconf['field'];
        temsql='';
        if action=='':
            return None
        if table=='':
            return None
        if field=='':
            return None

        if action=='insert':
            fie=''
            val=''
            for a in self.data:
                if fie!='':
                    fie+=',`%s`'%a
                else:
                    fie+='`%s`'%a

                if val!='':
                    val+=',%s'
                else:
                    val+='%s'
                self.sqlparam.append(self.data[a])
            temsql='insert %s (%s) values(%s)'%(table, fie, val)

        elif action=='update':
            val=''
            for a in self.data:
                if val!='':
                    val+=',`'+a+'`=%s'
                else:
                    val+='`'+a+'`=%s'
                self.sqlparam.append(self.data[a])
            temsql='update %s set %s %s %s'%(table, val, where,limit)

        elif action=='select':
            temsql='select %s from %s %s %s %s'%(field,table,where,order,limit)
        elif action=='delete':
            temsql='delete from %s %s'%(table,where)
        self.sql=temsql

    def table(self,data):
        if self.prefix!='':
            data=self.prefix+data
        self.sqlconf['table']=data
        return self

    def field(self,data):
        self.sqlconf['field']=data;
        return self

    def where(self,data):
        data=' where '+data
        self.sqlconf['where']=data;
        return self

    def order(self,data):
        data=' order '+data
        self.sqlconf['order']=data;
        return self

    def limit(self,start=0,end=0):
        if start!=0 and end!=0:
            data='limit %d,%d'%(start,end)
        elif start!=0 and end==0:
            data='limit 0,%d'%(start)
        elif start==0 and end==0:
            data=''
        self.sqlconf['limit']=data;
        return self

    def query(self,data):
        self.sql=data
        return self.__execute()

    def save(self,data):
        self.sql=''
        self.data=data
        self.sqlconf['action']='update'
        return self.__execute()

    def add(self,data):
        self.sql=''
        self.data=data
        self.sqlconf['action']='insert'
        return self.__execute()

    def delete(self):
        self.sql=''
        self.sqlconf['action']='delete'
        return self.__execute()

    def select(self):
        self.sql=''
        self.sqlconf['action']='select'
        return self.__getcur()

    def close(self):#关闭所有连接
        self.cur.close();
        self.con.close();

if __name__ == '__main__':
    db=mysql({
            'host':'localhost',
            'user':'root',
            'passwd':'adminrootkl',
            'db':'test',
            'prefix':'kl_',
            'charset':'utf8'
        })
    # da=db.table('article').limit(2).select()
    # for a in da:
    #     print(a['title']) # a[1] 表示当前游标所在行的的第2列值，如果是中文则需要处理编码
    content="<html '>"
    # num=db.table('article').add({
    #     'title':'测试标题',
    #     'content':content
    #     })
    #num=db.table('article').where('id=1').save({'content':'已经更新'})
    # num=db.table('article').where('id=3').delete()
    #print(num)
    list=db.table('article').select()
    for a in list:
        print(a['title']) # a[1] 表示当前游标所在行的的第2列值，如果是中文则需要处理编码
        print(a['content'])


    db.close()
    input('按任意键继续...')
