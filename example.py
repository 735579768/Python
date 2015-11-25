import sys
sys.path.append('./lib/')
import kl_db


if __name__ == '__main__':
    kl_db.mysql.conn({
            'host':'localhost',
            'user':'root',
            'passwd':'adminrootkl',
            'db':'ainiku',
            'charset':'utf8'
        })
    da=kl_db.mysql.select('select * from kl_article')
    for a in da:
        print(a)
    print('-------------------------------------')

    da=kl_db.mysql.select('select * from kl_article')
    for a in da:
        print(a['title']) # a[1] 表示当前游标所在行的的第2列值，如果是中文则需要处理编码

    kl_db.mysql.close()
    input('按任意键继续...')
