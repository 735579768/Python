import zipfile,os
class kl_zip(zipfile.ZipFile):

    def __init__(self,zip_dest_name, b='w'):
        zipfile.ZipFile.__init__(self,zip_dest_name,b)

    def addfile(self,filepath):
        self.write(filepath,os.path.basename(filepath))

    def addfolder(self,folderpath):
        self.__zipfolder(folderpath)

    def __zipfolder(self,folderpath):
        #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for parent,dirnames,filenames in os.walk(folderpath):
            #压缩文件
            for filename in filenames:
                filepath=os.path.join(parent,filename)
                arcpath=filepath[len(folderpath)+1:]

                if os.path.exists(filepath):
                    print('adding  file %s =>%s'%(filepath,arcpath))
                    try:
                        self.write(filepath,arcpath)
                    except Exception as e:
                        print(e)
                else:
                    print('file %s is not exist!'%filepath)


    def complete(self):
        self.close()

if __name__ == '__main__':
    zip=kl_zip('E:/test.zip')
    zip.addfolder(r'E:\wwwroot\test')
    zip.complete()
    os.system('pause')