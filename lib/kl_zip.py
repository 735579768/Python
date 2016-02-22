import zipfile,os
class kl_zip(zipfile.ZipFile):

    def __init__(self,zip_dest_name, b='w'):
        zipfile.ZipFile.__init__(self,zip_dest_name,b)

    def addfile(self,filepath):
        self.write(filepath,os.path.basename(filepath))

    def addfolder(self,folderpath):
        self.__zipfolder(folderpath,os.path.basename(folderpath))

    def __zipfolder(self,folderpath,rootpath):
        #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for parent,dirnames,filenames in os.walk(folderpath):
            #压缩文件
            for filename in filenames:
                filepath=os.path.join(folderpath,filename).replace('\\','/')
                arcpath=os.path.join(rootpath,os.path.basename(filename)).replace('\\','/')

                print(filepath)
                if os.path.exists(filepath):
                   # print('adding  file %s =>%s'%(filepath,arcpath))
                    try:
                        self.write(filepath,arcpath)
                    except Exception as e:
                        print(e)

            #输出文件夹信息
            for dirname in  dirnames:
                if dirname!='.' and dirname!='..':
                    dirnam=os.path.join(folderpath,dirname).replace('\\','/')
                    rotpath=os.path.join(rootpath,os.path.basename(dirname)).replace('\\','/')
                    self.__zipfolder(dirnam,rotpath)


    def complete(self):
        self.close()

if __name__ == '__main__':
    zip=kl_zip('E:/test.zip')
    zip.addfolder(r'E:\wwwroot\test')
    zip.complete()
    os.system('pause')