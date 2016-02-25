import xlrd,xlwt
from datetime import date,datetime

from xlwt.examples.zoom_magnification import book


class kl_excel(object):
    """docstring for kl_excel"""
    def __init__(self, filepath,head=False):
        super(kl_excel, self).__init__()
        #是否有表头
        self.head=head
        self.field=[]
        #初始化表格
        self.sheets =None
        #当前操作的表格
        self.cur_sheet=None
        self.__initsheet(filepath)

    def __initsheet(self,filepath):
        #初始化表格
        self.sheets = xlrd.open_workbook(filepath)
        #当前操作的表格
        self.cur_sheet=self.sheets.sheets()[0]
        #设置表头
        if self.head:
            self.field=self.getrow(0)
        else:
            self.field=[i for i in range(0,self.getcolnum())]

    def readexcel(self,filepath):
        self.__initsheet(filepath)
        return self.getalldata()

    #设置单元格样式
    def __getstyle(self,name,height,bold=False):
      style = xlwt.XFStyle() # 初始化样式
      font = xlwt.Font() # 为样式创建字体
      font.name = name # 'Times New Roman'
      #font.bold = bold
      font.color_index = 4
      font.height = height
      # borders= xlwt.Borders()
      # borders.left= 6
      # borders.right= 6
      # borders.top= 6
      # borders.bottom= 6

      style.font = font
      # style.borders = borders
      return style

    def writeexcel(self,filepath,data=[]):
        try:
            if not data:
                return None
            #创建工作簿
            f= xlwt.Workbook()
            #创建第一个sheet:
            sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True)
            #取键值列表
            fieldlist=data[0].keys()
            for i in range(0,len(data)):
                m=0
                for j in fieldlist:
                    value=data[i][j]
                    sheet1.write(i,m,value,self.__getstyle('Times New Roman',220,True))
                    m+=1
            f.save(filepath)
        except Exception as e:
            print(e)
            return None

    #取表格全部数据
    def getalldata(self):
        '''
        python读取excel中单元格的内容返回的有5种类型
        ctype : 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
        '''
        try:
            rownum=self.getrownum()
            colnum=self.getcolnum()
            startrow=0
            if self.head:
                startrow=1
            else:
                startrow=0
            rearr=[]
            for i in range(startrow,rownum):
                tem={}
                for j in range(0,colnum):
                    value=self.gettellvalue(i, j)
                    tem[self.field[j]]=value
                rearr.append(tem)
            return rearr
        except Exception as e:
            print(e)
            return None

    #设置单元格的值
    def settellvalue(self,row,col,ctype,value,xf=0):
        self.cur_sheet.put_cell(row, col, ctype, value, xf)

    #取单元格的值
    def gettellvalue(self,row,col):
        tellvalue=self.cur_sheet.cell(row,col)
        if tellvalue.ctype==0:#empty
            tellvalue=''
        elif tellvalue.ctype==1:#string
            tellvalue=tellvalue.value
        elif tellvalue.ctype==2:#number
            tellvalue=tellvalue.value
        elif tellvalue.ctype==3:#date
            tellvalue=tellvalue.value
            date_value = xlrd.xldate_as_tuple(tellvalue,book.datemode)
            date_tmp = date(*date_value[:3]).strftime('%Y/%m/%d')
        elif tellvalue.ctype==4:#boolean
            tellvalue=tellvalue.value
        elif tellvalue.ctype==5:#error
            tellvalue=''
        return tellvalue

    def getrownum(self):
        return  self.cur_sheet.nrows

    def getcolnum(self):
        return  self.cur_sheet.ncols

    def setsheet(self,index=0):
        self.cur_sheet=self.sheets.sheets()[index]
        return self

    def getrow(self,index=0):
        return  self.cur_sheet.row_values(index)

    def getcol(self,index=0):
        return  self.cur_sheet.col_values(index)

if __name__ == '__main__':
    excel=kl_excel('./test.xlsx',False)
    row1=excel.getrow(0)
    row2=excel.getrow(1)
    row3=excel.getcol(0)
    row4=excel.getcol(1)

    num1=excel.getrownum()
    num2=excel.getcolnum()

    value1=excel.gettellvalue(0,2)
    value2=excel.gettellvalue(4,1)
    data=excel.getalldata()

    #写excel
    data=[
        {
            'name':'名字',
            'title':'标题',
            'pic':'图片'
        },
        {
            'name':'名字',
            'title':'标题',
            'pic':'图片'
        }
    ]
    excel.writeexcel('./save.xls',data)
    input()
