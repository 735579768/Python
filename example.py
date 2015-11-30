import sys
import urllib
sys.path.append('./lib/')
import kl_log,kl_db,kl_http


if __name__ == '__main__':
    try:
        page=kl_http.kl_http()
        print(page.posturl('http://www.baidu.com'))
        kl_log.write('success')
        input('按任意键继续...')
    except KeyboardInterrupt as e:
        print('程序已经退出')
        print(e)
