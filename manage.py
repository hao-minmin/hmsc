from application import app,manager

# flask_script  提供的服务器
import urls
from flask_script import Server

#配置runserve指令   添加指令add_command   主机 端口  开发模式  热更新
manager.add_command('runserver',Server(host="localhost",port="5000",use_debugger=True,use_reloader=True))


# run起来
def main():
    manager.run()

if __name__=="__main__":

    try:
        import sys
        sys.exit(main())
    except Exception as e:
        import traceback
        traceback.print_exc()