import os


BASE_DIRS = os.path.dirname(__file__)
options={
    "port":9000
}

settings={
    "static_path":os.path.join(BASE_DIRS,"static"),
    "template_path":os.path.join(BASE_DIRS,"templates"),
    # 安全coolie的加密值
    "cookie_secret":b'dtp4oqWiT4i8/ChlMHLpEuy5ILCm3ED5qVq3+jdCJ+U=',
    # 开启_xsrf防护
    "xsrf_cookies":True,
    # 指定验证不通过时跳转路由
    "login_url":"/login",
    "debug":True,
}

database={
    "port":27017,
    "host":"localhost",
}