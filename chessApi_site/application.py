"""
Created on 28.04.2018
@author: lorinc
"""
from flask import Flask

app = Flask(__name__, static_folder='static', static_url_path='')
app.debug = True
