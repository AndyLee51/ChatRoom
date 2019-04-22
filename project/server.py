import tornado,os
from application import myApplication
import config
if __name__ == "__main__":

    app = myApplication()
    server = tornado.web.HTTPServer(app,xheaders=True)
    server.listen(config.options["port"])
    tornado.ioloop.IOLoop().current().start()

