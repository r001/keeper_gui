#
# This file is part of Maker Keeper Framework.
#
# Copyright (C) 2017 r001
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from flask import render_template,make_response,Response,flash,redirect,request, Flask
from app import app
from time import sleep
import subprocess
from .forms import KeeperForm, SaiArbitrageForm, SaiBiteForm
from app.utils import reverse_readline, set_page_text
import os
import configparser

title="Dai Credit System - Keeper Monitoring"

@app.route('/')
def index():
    form = KeeperForm();
    sai_arbitrage_form = SaiArbitrageForm()
    sai_bite_form = SaiBiteForm()
    config = configparser.ConfigParser()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    if config.read(dir_path + '/../keepers.conf') == []:
        print("Could not read configfile.\n")
        exit(-1)
    return render_template('defaults.html',
                           title=title,
                           keeper_form=form,
                           sai_arbitrage_form=sai_arbitrage_form,
                           sai_bite_form=sai_bite_form,
                           keeper="sai_ar", 
                           config=config
                           )

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
        lines = []
        for pos, line in enumerate(reverse_lines):
            if last_id != "" and line.startswith(last_id):
                break
            yield line + "\n"
    return Response(inner(last_id,keeper), mimetype='text/html')

@app.route('/keeper', methods=['GET', 'POST'])
def keeper():
    form = KeeperForm()
    sai_arbitrage_form = SaiArbitrageForm()
    sai_bite_form = SaiBiteForm()
    config = configparser.ConfigParser()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    if config.read(dir_path + '/../keepers.conf') == []:
        print("Could not read configfile.\n")
        exit(-1)
    return render_template('defaults.html',
                           title=title,
                           keeper_form=form,
                           sai_arbitrage_form=SaiArbitrageForm(),
                           sai_bite_form=SaiBiteForm(),
                           keeper=form.keeper.data, 
                           config=config
                           )

@app.route('/sai_arbitrage', methods=['GET', 'POST'])
def saiArbitrage():
    form = KeeperForm();
    sai_arbitrage_form = SaiArbitrageForm() 
    sai_bite_form = SaiBiteForm() 
    return processBiteAndArbitrage("sai_arbitrage",sai_arbitrage_form, sai_bite_form, form);

@app.route('/sai_bite', methods=['GET', 'POST'])
def saiBite():
    form = KeeperForm();
    sai_arbitrage_form = SaiArbitrageForm() 
    sai_bite_form = SaiBiteForm() 
    return processBiteAndArbitrage("sai_bite",sai_arbitrage_form, sai_bite_form, form);
def processBiteAndArbitrage(action, sai_arbitrage_form, sai_bite_form, form):
    if action == "sai_arbitrage":
        curr_form = sai_arbitrage_form
    else:
        curr_form = sai_bite_form
    config = configparser.ConfigParser()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    if config.read(dir_path + '/../keepers.conf') == []:
        print("Could not read configfile.\n")
        exit(-1)
    if curr_form.auth_token.data != config['Default']['auth-token']:
        config[action]['auth_error']="Invalid Auth token"
    else:
        if curr_form.validate():
            if action == "sai_arbitrage":
                config['sai_arbitrage']['eth-from']      =     curr_form.eth_from.data
                config['sai_arbitrage']['base-token']    =     curr_form.base_token.data
                config['sai_arbitrage']['min-profit']    = str(curr_form.minimum_profit.data) \
                                                           if str(curr_form.minimum_profit.data) != "None" else ""
                config['sai_arbitrage']['max-engagement']= str(curr_form.maximum_engagement.data)\
                                                           if str(curr_form.maximum_engagement.data) != "None" else "" 
                config['sai_arbitrage']['tx-manager']    =     curr_form.tx_manager.data
                config['sai_arbitrage']['max-errors']    = str(curr_form.max_errors.data) if str(curr_form.max_errors.data) != "None" else ""
                config['sai_arbitrage']['rpc-host']      =     curr_form.rpc_host.data
                config['sai_arbitrage']['rpc-port']      = str(curr_form.rpc_port.data) if str(curr_form.rpc_port.data) != "None" else ""
            elif action == "sai_bite":
                config['sai_bite']['eth-from']           =     curr_form.eth_from.data
                config['sai_bite']['rpc-host']           =     curr_form.rpc_host.data
                config['sai_bite']['rpc-port']           = str(curr_form.rpc_port.data) if str(curr_form.rpc_port.data) != "None" else ""
                config['sai_bite']['frequency']          = str(curr_form.frequency.data) if str(curr_form.frequency.data) != "None" else ""
            with open(dir_path + '/../keepers.conf', 'w') as configfile:
                config.write(configfile)
            if curr_form.server_cmd.data != "nothing":
                if subprocess.Popen(f"/usr/bin/sudo /bin/systemctl {curr_form.server_cmd.data} {action}.service",
                shell=True) == 0:
                    config[action]['service_error']=f"Could not {curr_form.server_cmd.data} service."
                else:
                    config[action]['service_ok']=f"Service {curr_form.server_cmd.data} successful."
    return render_template('index.html',
                           title=title,
                           keeper_form=form,
                           sai_arbitrage_form=sai_arbitrage_form,
                           sai_bite_form=sai_bite_form,
                           keeper= "sai_bi" if action == "sai_bite" else "sai_ar" , 
                           config=config
                           )
