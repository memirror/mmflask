# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/6/29

from gevent.pywsgi import WSGIServer

from web.flask.magicmirror import app


if __name__ == '__main__':

    http_server = WSGIServer(('', 8910), app)
    http_server.serve_forever()
 
