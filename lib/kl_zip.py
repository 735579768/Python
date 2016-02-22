import zipfile,os,kl_log
class kl_zip(zipfile.ZipFile):

    def __init__(self,zip_dest_name, b='w'):
        self.log=kl_log.kl_log('kl_zip')
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
                    try:
                        print('adding  file %s =>%s'%(filepath,arcpath))
                        self.write(filepath,arcpath)
                    except Exception as e:
                        self.log.write(e)
                        print(e)
                else:
                    print('file %s is not exist!'%filepath)
    def extract_to(self, path):
        for p in self.namelist():
            self.extract(p, path)

    def extract(self, filename, path):
        try:
            if not filename.endswith('/'):
                f = os.path.join(path, filename).replace('\\','/')
                dir = os.path.dirname(f)
                if not os.path.exists(dir):
                    os.makedirs(dir)
                print('extracting :%s => %s'%(filename, f))
                f=open(f,'wb')
                f.write(self.read(filename))
                f.close()
        except Exception as e:
            pass

    def complete(self):
        self.close()

if __name__ == '__main__':
    #压缩
    # zip=kl_zip('E:/test.zip')
    # zip.addfolder(r'E:\wwwroot\test')
    # zip.complete()

    #解压
    zip=kl_zip('E:/test.zip','r')
    zip.extract_to('E:/test')

    os.system('pause')