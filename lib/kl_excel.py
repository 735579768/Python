import xlrd
class kl_excel(object):
    """docstring for kl_excel"""
    def __init__(self, filepath,head=False):
        super(kl_excel, self).__init__()
        #是否有表头
        self.head=head
        self.field=[]
        #初始化表格
        self.sheets = xlrd.open_workbook(filepath)
        #当前操作的表格
        self.cur_sheet=self.sheets.sheets()[0]
        self.__sethead()
        #设置表头
    def __sethead(self):
        if self.head:
            self.field=self.getrow(0)
        else:
            self,field=[range(0,self.getcolnum())]

    def readexcel(self,filepath):
        pass

    def writeexcel(self,filepath):
        pass

    #取表格全部数据
    def getalldata(self):
        rownum=self.getrownum()
        colnum=self.getcolnum()
        startrow=0
        if self.head:
            startrow=1
        else:
            startrow=0

        rearr=[]
        for i in range(startrow,rownum-1):
            tem={}
            for j in range(0,colnum-1):
                value=self.gettellvalue(i, j)
                tem[self.field[j]]=value
            rearr.append(tem)
        return rearr

    #设置单元格的值
    def settellvalue(self,row,col,ctype,value,xf=0):
        self.cur_sheet.put_cell(row, col, ctype, value, xf)

    #取单元格的值
    def gettellvalue(self,row,col):
        return self.cur_sheet.cell(row,col).value

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
    excel=kl_excel('./test.xlsx',True)
    row1=excel.getrow(0)
    row2=excel.getrow(1)
    row3=excel.getcol(0)
    row4=excel.getcol(1)

    num1=excel.getrownum()
    num2=excel.getcolnum()

    value1=excel.gettellvalue(0,2)
    value2=excel.gettellvalue(4,1)
    data=excel.getalldata()
    input()
