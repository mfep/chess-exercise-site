"""
Created on 28.04.2018
@author: lorinc
"""
from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware
from chessApi.resources import app as chessApi
from chessApi_site.application import app as chessApiSite

application = DispatcherMiddleware(chessApi, {
    '/site': chessApiSite
})

if __name__ == '__main__':
    run_simple('localhost', 5000, application,
               use_reloader=True, use_debugger=True, use_evalex=True)
