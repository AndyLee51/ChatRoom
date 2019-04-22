import tornado.web
from tornado.web import url
from views import index
import config
import os

class myApplication(tornado.web.Application):
    def __init__(self):
        # 启动数据库
        
        
        handler =[
            url(r"/login",index.LoginHandler,name="login",),
            url(r"/register",index.RegisterHandler,name="register",),
            url(r"/imgvalid",index.ImgValidHandler,name="imgvalid"),
            url(r"/main",index.MainHandler,name="main"),
            url(r"/group",index.GroupHandler,name="group"),
            url(r"/wschat",index.WSChatHandler,name="wschat"),
            url(r"/error",index.ErrorPageHandler,name="error"),
            # 添加默认路由(# 添加_xrsf验证刻写在继承StaticFileHandler的类__init__,在初次访问时开启)
            url(r"/(.*$)",tornado.web.StaticFileHandler,{"path":os.path.join(config.BASE_DIRS,"static/html"),"default_filename":"index.html"}),
        ]
        super(myApplication,self).__init__(handler,**config.settings)