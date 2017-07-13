#!flask/bin/pythonasss
import os 
import sys
import logging
dir_path = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,dir_path)
sys.path.insert(0,dir_path + "flask/lib/python3.6/site-packages")
from app import app as application
from flipflop import WSGIServer
if __name__ == '__main__':
    WSGIServer(app).run()
