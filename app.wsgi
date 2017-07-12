import sys
import os
path_current = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, path_current)
sys.path.insert(0, path_current+"/flask/bin/")
from app import app
