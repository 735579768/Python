import win32com.client,sys
class Access(object):
    """docstring for Access"""
    def __init__(self, arg=None):
        super(Access, self).__init__()
        self.dbfile=arg
        self.conn=None
        self.cur=None
        self.sql=''
        self.lasterror=None
        self.sqlparam=[]
        self.prefix=''
        self.primary=''
        self.sqlconf={
            'action':'',
            'table':'',
            'join':'',
            'where':'',
            'order':'',
            'limit':'',
            'field':'*'
        }
        self.__conn()

    #连接数据库
    def __conn(self):
        try:
            self.conn = win32com.client.Dispatch(r'ADODB.Connection')
            print(self.conn)
            DSN = 'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE='+self.dbfile+';'
            self.conn.Open(DSN)
        except Exception as e:
            print(e)
            sys.exit(0)

    def __getcur(self):
        self.cur=win32com.client.Dispatch(r'ADODB.Recordset')
        #self.cur.Open(self.sql, self.conn,1, 3)
        self.cur.Open('select * from content', self.conn,1, 3)
        return self.cur

    def __execute(self):
        self.cur=win32com.client.Dispatch(r'ADODB.Recordset')
        self.cur.Open(self.sql, self.conn,1, 3)
        return self.cur



    def getRsNum(self):
        return self.cur.RecordCount
##################################################3
    #组合sql语句
    def __zuhesqu(self):
        self.sqlparam=[]
        action=self.sqlconf['action']
        table=self.sqlconf['table']
        where=self.sqlconf['where']
        order=self.sqlconf['order']
        limit=self.sqlconf['limit']
        join=self.sqlconf['join']
        field=self.sqlconf['field']
        temsql=''
        if action=='':
            return None
        if table=='' and join=='':
            return None
        if field=='' and join=='':
            return None

        if action=='insert into':
            fie=''
            val=''
            for a in self.data:
                fie+=(',`%s`'%a) if fie!='' else  ('`%s`'%a)
                val+=(',%s') if val!='' else ('%s')
                self.sqlparam.append(self.data[a])
            temsql='insert into %s (%s) values(%s)'%(table, fie, val)

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
        elif tj=='eq':
            temdata=" (%s = '%s')"%(field,data[1])
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

    def query(self,data):
        self.lasterror=None
        self.sql=data
        return self.__execute()

    def save(self,data):
        self.lasterror=None
        self.sql=''
        self.data=data
        self.sqlconf['action']='update'
        return self.__execute()

    def add(self,data):
        self.lasterror=None
        self.sql=''
        self.data=data
        self.sqlconf['action']='insert into'
        return self.__execute()

    # def delete(self,id=''):
    #     self.__setprimary()
    #     self.lasterror=None
    #     self.sql=''
    #     self.sqlconf['action']='delete'
    #     if self.primary and id:
    #         self.sqlconf['where']='%s=%s'%(self.primary,id)
    #     return self.__execute()

    # def find(self,id=''):
    #     self.__setprimary()
    #     if self.primary and id:
    #         self.sqlconf['where']='where %s=%s'%(self.primary,id)
    #     data=self.getarr()
    #     return data[0] if len(data) else None


    def getarr(self):
        record=self.select()
        if record:
            return record.fetchall()
        else:
            return []

    def select(self):
        self.lasterror=None
        self.sql=''
        self.sqlconf['action']='select'
        return self.__getcur()

    # def add(self,data={}):
    #     self.cur.AddNew()
    #     self.cur.Fields.Item(1).Value = 'data'
    #     self.cur.Update()

    # def save(self,data={}):
    #     self.cur.Update()


if __name__ == '__main__':
    try:
        db=Access('db1.mdb')
        rs=db.select()
        print(rs.Fields.Count)

        #第一个字段名
        print(rs(0).Name)

        #第一个字段值
        print(rs('id'))

        print(rs.Fields.Item(1))
        print(rs.Fields.Item(1).Value)
        print(db.getRsNum())
        while not rs.EOF:
            rs.MoveNext()

        # rs.close()

    #     rs.MoveFirst：指向第一条记录。
    # 　　rs.MoveLast：指向最后一条记录。
    # 　　rs.MovePrev：指向上一条记录。
    # 　　rs.MoveNext：指向下一条记录。
    # 　　rs.GetRows：将数据放入数组中。
    except Exception as e:
        print(e)

