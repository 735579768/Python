'''
+----------------------------------------------------------------------
// | Author: 赵克立 <735579768@qq.com> <http://www.zhaokeli.com>
// |mysql数据库操作类
+----------------------------------------------------------------------
// |#返回单行数据
// |result = cursor.fetchone()
// |#返回所有数据
// |result = cursor.fetchall()
// |
// |获得游标
// |cursor = conn.cursor(cursorclass=MySQLdb.cursors.Cursor)
// |cursorclass参数:
// |MySQLdb.cursors.Cursor， 默认值，执行SQL语句返回List，每行数据为tuple
// |MySQLdb.cursors.DictCursor， 执行SQL语句返回List，每行数据为Dict
'''
import pymysql
class mysql(object):

    def __init__(self, arg):
        self.sql=''
        self.lastsql=''
        self.sqlparam=[]
        self.prefix=''
        self.sqlconf={
            'action':'',
            'table':'',
            'join':'',
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
            self.con=pymysql.connect(
                host=config['host'],
                user=config['user'],
                passwd=config['passwd'],
                db=config['db'],
                charset=config['charset'],
                port=3306,
                cursorclass=pymysql.cursors.DictCursor
                )
        self.cur=self.con.cursor(pymysql.cursors.DictCursor);#获取操作游标

    #返回一个记录集
    def __getcur(self):
        if self.sql=='':
            self.__zuhesqu()
        try:
            try:
                self.cur.execute(self.sql)
                self.con.commit()
                self.lastsql=self.sql
                self.__init()
                return self.cur
            except pymysql.err.ProgrammingError as e:
                print(e)
                print('SQL:[%s]'%self.sql)
                self.lastsql=self.sql
                self.__init()
                return None
        except pymysql.err.InternalError as e:
            print(e)
            print('SQL:[%s]'%self.sql)
            self.lastsql=self.sql
            self.__init()
            return None

    #返回执行结果记录数
    def __execute(self):
        if self.sql=='':
            self.__zuhesqu()
        try:
            try:
                num=0
                if len(self.sqlparam):
                    num=self.cur.execute(self.sql,self.sqlparam)
                else:
                    num=self.cur.execute(self.sql)
                if self.sqlconf['action']=='insert':
                    #最新插入行的主键ID
                    zhuid=int(self.cur.lastrowid)
                    if num>0 and zhuid>0:
                        num=zhuid
                elif self.sqlconf['action']=='select count(*)':
                    da=self.cur.fetchone()
                    num=da['num']
                self.con.commit()
                self.lastsql=self.sql
                self.__init()
                return num
            except pymysql.err.ProgrammingError as e:
                print(e)
                print('SQL:[%s]'%self.sql)
                self.lastsql=self.sql
                self.__init()
                return 0
        except pymysql.err.InternalError as e:
            print(e)
            print('SQL:[%s]'%self.sql)
            self.lastsql=self.sql
            self.__init()
            return 0

    #组合sql语句
    def __zuhesqu(self):
        self.sqlparam=[]
        action=self.sqlconf['action'];
        table=self.sqlconf['table'];
        where=self.sqlconf['where'];
        order=self.sqlconf['order'];
        limit=self.sqlconf['limit'];
        join=self.sqlconf['join'];
        field=self.sqlconf['field'];
        temsql='';
        if action=='':
            return None
        if table=='' and join=='':
            return None
        if field=='' and join=='':
            return None

        if action=='insert':
            fie=''
            val=''
            for a in self.data:
                fie+=(',`%s`'%a) if fie!='' else  ('`%s`'%a)
                val+=(',%s') if val!='' else ('%s')
                self.sqlparam.append(self.data[a])
            temsql='insert %s (%s) values(%s)'%(table, fie, val)

        elif action=='update':
            val=''
            for a in self.data:
                val+=(',`'+a+'`=%s') if val!='' else ('`'+a+'`=%s')
                self.sqlparam.append(self.data[a])
            temsql='update %s set %s %s %s'%(table, val, where,limit)

        elif action=='select':
            temsql='select %s from %s %s %s %s %s'%(field,table,join,where,order,limit)
        elif action=='delete':
            temsql='delete from %s %s'%(table,where)
        elif action=='select count(*)':
            temsql='select count(*) as num from %s %s %s %s %s'%(table,join,where,order,limit)
        self.sql=temsql

    #对数组进行条件组合
    def __tjzh(self,field,data):
        temdata=''
        tj=data[0]
        if tj=='like':
            temdata=" (%s like '%s')"%(field,data[1])
        elif tj=='in':
            temdata=" (%s in(%s))"%(field,data[1])
        elif tj=='gt':
            temdata=" (%s > %s)"%(field,data[1])
        elif tj=='egt':
            temdata=" (%s >= %s)"%(field,data[1])
        elif tj=='lt':
            temdata=" (%s < %s)"%(field,data[1])
        elif tj=='elt':
            temdata=" (%s <= %s)"%(field,data[1])
        elif tj=='neq':
            temdata=" (%s <> %s)"%(field,data[1])
        return temdata

    #处理查询条件
    def __where(self,data):
        temdata='1=1'
        for field in data:
            temf=data[field]
            if type(temf)==type([]):
                le=len(temf)
                if le>2:
                    zuhe=temf[le-1]
                    t='1=1'
                    for i in temf:
                        if i!=zuhe:
                            t+=' %s %s'%(zuhe,self.__tjzh(field,i))
                    t=t.replace('1=1 %s'%zuhe,'')
                    temdata+=' and (%s)'%(t)
                else:
                    te0=self.__tjzh(field,temf)
                    temdata+=' and %s'%(te0)
            else:
                temdata+=" and (%s='%s')"%(field,temf)
        temdata=temdata.replace('1=1 and','')
        return temdata

    #初始化查询条件
    def __init(self):
        self.sqlconf={
            'action':'',
            'table':'',
            'join':'',
            'where':'',
            'order':'',
            'limit':'',
            'field':'*'
        }
        self.sql=''
        self.sqlparam={}

    #切换数据库
    def selectdb(self,dbname):
        self.con.select_db(dbname)

    #返回主机信息
    def gethostinfo(self):
        return self.con.get_host_info()

    #返回数据库版本
    def getserverinfo(self):
        return self.con.get_server_info()

    def table(self,data):
        if self.prefix!='':
            data=self.prefix+data
        self.sqlconf['table']=data
        return self

    def field(self,data):
        self.sqlconf['field']=data
        return self

    def where(self,data):
        temdata='where '
        if type(data)==type({}):
            temdata+=self.__where(data)
        else:
            temdata+=data
        self.sqlconf['where']=temdata
        return self

    def order(self,data):
        data=' order by '+data
        self.sqlconf['order']=data
        return self

    def join(self,data):
        tem=''
        first=''
        field=''
        for i in data:
            tb=self.prefix+i
            bas=data[i]['_as']
            if ('_on') in data[i]:
                bon=data[i]['_on']
                tem+=" inner join %s as %s on %s"%(tb,bas,bon)
            else:
                first="%s as %s "%(tb,bas)
            #给字段加上前缀
            fie=data[i]['field']
            arr=fie.split(',')
            for fi in arr:
                if field=='':
                    field+="%s.%s"%(bas,fi)
                else:
                    field+=','+"%s.%s"%(bas,fi)
        self.sqlconf['join']=first+tem
        self.sqlconf['field']=field
        return self

    def limit(self,start=0,end=0):
        if start!=0 and end!=0:
            data='limit %d,%d'%(start,end)
        elif start!=0 and end==0:
            data='limit 0,%d'%(start)
        elif start==0 and end==0:
            data=''
        self.sqlconf['limit']=data
        return self

    def getlastsql(self):
        return self.lastsql

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

    def count(self):
        self.sql=''
        self.sqlconf['action']='select count(*)'
        return self.__execute()

    def close(self):#关闭所有连接
        self.cur.close();
        self.con.close();

#使用示例
if __name__ == '__main__':
    db=mysql({
            'host':'localhost',
            'user':'root',
            'passwd':'adminrootkl',
            'db':'test',
            'prefix':'kl_',
            'charset':'utf8'
        })
    #查询数据列表
    '''
     da=db.table('article').limit(2).select()
     for a in da:
         print(a['title']) # a[1] 表示当前游标所在行的的第2列值，如果是中文则需要处理编码

    '''
    #添加数据
    ''''
    content="<html '>"
    num=db.table('article').add({
         'title':'测试标题',
         'content':content
         })
    '''
    #更新数据
    '''
    num=db.table('article').where('id=1').save({'content':'已经更新'})
    num=db.table('article').where('id=3').delete()
    print(num)
    '''
    #组合查询条件查询
    '''
    map={
    'title':['like','%1%'],
    'id':[['gt',0],['lt',1],['lt',8],['lt',9],'or']
    }
    list=db.table('article').order('id desc').where(map).select()
    for a in list:
        print(a['title']) # a[1] 表示当前游标所在行的的第2列值，如果是中文则需要处理编码
        print(a['content'])

    print(db.getlastsql())
    '''

    #多表联合查询
    '''
    model={
     'article':{'_as':'a','field':'title,id,content,category_id'},
     'category':{'_as':'b','field':'category_id as cate_id','_on':'a.category_id=b.category_id'}
    }
    list=db.join(model).where("a.title like '%%'").select()
    for a in list:
        print(a['title']) # a[1] 表示当前游标所在行的的第2列值，如果是中文则需要处理编码
        print(a['content'])

    print(db.getlastsql())
    '''

    #创建数据表
    '''
    sql = """CREATE TABLE EMPLOYEE (
         FIRST_NAME  CHAR(20) NOT NULL,
         LAST_NAME  CHAR(20),
         AGE INT,
         SEX CHAR(1),
         INCOME FLOAT )"""
    db.query(sql)
    '''

    #删除表
    '''
    sql="DROP TABLE IF EXISTS EMPLOYEE"
    db.query(sql)
    '''

    #切换数据库
    '''
    db.selectdb('ainiku')
    list=db.table('article').select()
    for a in list:
        print(a['title']) # a[1] 表示当前游标所在行的的第2列值，如果是中文则需要处理编码
        print(a['content'])
    '''

    print("主机信息:%s"%db.gethostinfo())
    print("数据库版本:%s"%db.getserverinfo())
    db.close()
    input('按任意键继续...')
