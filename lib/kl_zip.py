import zipfile,os
class kl_zip(zipfile.ZipFile):

    def __init__(self,zip_dest_name, b='w'):
        zipfile.ZipFile.__init__(self,zip_dest_name,b)

    def addfile(self,filepath):
        self.write(filepath)

    def addfolder(self,folderpath):
        self.__zipfolder(folderpath,folderpath)

    def __zipfolder(self,folderpath,rootpath):
        #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for parent,dirnames,filenames in os.walk(folderpath):
                #输出文件夹信息
            for dirname in  dirnames:
                if dirname!='.' and dirname!='..':
                    dirname=os.path.join(rootpath,dirname).replace('\\','/')
                    self.__zipfolder(dirname,dirname)

            for filename in filenames:
                #print(rootpath)
                filepath=os.path.join(rootpath,filename).replace('\\','/')
                print('adding  file %s'%filepath)
                if os.path.exists(filepath):
                    self.write(filepath)

    def complete(self):
        self.close()

if __name__ == '__main__':
    zip=kl_zip('E:/test.zip')
    zip.addfolder('E:/wwwroot/test')
    zip.complete()