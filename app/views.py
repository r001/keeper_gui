from flask import render_template,make_response,Response,flash,redirect,request, Flask
from app import app
from time import sleep
import subprocess
from .forms import LoginForm
from app.utils import reverse_readline, set_page_text
import os

title="Dai Credit System - Keeper Monitoring"

@app.route('/')
def index():
    form = LoginForm();
    app = Flask(__name__)
    app.config.from_object('config')
    return render_template('index.html', 
        title=title, 
        form=form , 
        keeper = "sai_ar", 
        sai_ar=app.config['SAI_AR'], 
        dai_bb=app.config['DAI_BB'], 
        sai_bi=app.config['SAI_BI'], 
        sai_to=app.config['SAI_TO']) 

@app.route('/stream', methods=['GET', 'POST'])
def stream():
    last_id=request.args['last_id']
    keeper=request.args['keeper']
    def inner(last_id,keeper):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        prefix="/../log/"
        if 'keeper' not in globals() and 'keeper' not in locals():
            keeper="sai_ar"
        if keeper == "dai_bb":
            log="dai_buy_and_burn.log"
        elif keeper == "sai_ar":
            log="sai_arbitrage.log"
        elif keeper == "sai_bi":
            log="sai_bite.log"
        elif keeper == "sai_to":
            log="sai_top_up.log"
        else:
            log="sai_arbitrage"
        reverse_lines = reverse_readline(dir_path + prefix + log)
        start=False
        for pos, line in enumerate(reverse_lines):
            if last_id != "" and line.startswith(last_id):
                break
            yield line
    return Response(inner(last_id,keeper), mimetype='text/html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    app = Flask(__name__)
    app.config.from_object('config')
    return render_template('index.html',
                           title=title,
                           form=form,
                           keeper=form.keeper.data, 
                           sai_ar=app.config['SAI_AR'], 
                           dai_bb=app.config['DAI_BB'], 
                           sai_bi=app.config['SAI_BI'], 
                           sai_to=app.config['SAI_TO'])
