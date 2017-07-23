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
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DecimalField, SelectField, IntegerField, HiddenField
from wtforms.validators import DataRequired,Regexp, NumberRange, Optional
import configparser
import os

class KeeperForm(FlaskForm):
    config = configparser.ConfigParser()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    if config.read(dir_path + '/../keepers.conf') == []:
        print("Could not read configfile.\n")
        exit(-1)
    keeper = SelectField(
                           'Keeper:'
                         , choices = [
                              (
                                  "sai_ar"
                                , config['flask']['SAI_AR']
                              )
                            , (
                                  "sai_bi"
                                , config['flask']['SAI_BI']
                              )
                                     ]
                        )

class SaiArbitrageForm(FlaskForm):
    config = configparser.ConfigParser()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    if config.read(dir_path + '/../keepers.conf') == []:
        print("Could not read configfile.\n")
        exit(-1)
    eth_from = StringField(
                              'Eth-from:*',
                               validators = [Regexp("^0x[0-9a-zA-Z]{40}$")],
                              default = config['sai_arbitrage']['eth-from'],
                              description = "Ethereum account from which to send transactions"
                          )
    base_token = StringField(
                              'Base-token:*',
                               validators = [Regexp("^[0-9a-zA-Z]*$")],
                              default = config['sai_arbitrage']['base-token'],
                              description = "The base token of arbitrage transactions"
                          )
    minimum_profit = DecimalField(
                                    'Minimum profit:*',
                                    default = float(config['sai_arbitrage']['min-profit']),
                                    description = "Minimum profit in SAI from one arbitrage operation"
                                 )
    maximum_engagement = DecimalField(
                                         'Maximum engagement:*',
                                         default = float(config['sai_arbitrage']['max-engagement']),
                                         description = "Maximum engagement in SAI in one arbitrage operation"
                                     )
    max_errors = IntegerField(
                                         'Max errors:',
                                         default = int(float(config['sai_arbitrage']['max-engagement']) // 1),
                                         validators = [Optional()],
                                         description = "Maximum number of errors allowed."
                                     )
    tx_manager = StringField(
                               'Tx manager:',
                               default = config['sai_arbitrage']['tx-manager'],
                               validators = [Regexp("^0x[0-9a-zA-Z]{40}$|^$")],
                               description = "Address of the TxManager to use for multi-step arbitrage"
                            ) 
    auth_token = StringField(
                               'Auth token:*',
                               validators = [DataRequired()],
                               description = "Token to enable to modify parameters."
                            ) 

    rpc_host = StringField(
                              'Rpc-host:',
                              default = config['sai_arbitrage']['rpc-host'],
                              validators =
                              [Regexp("((?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$))|^(([0-9]|[1-9][0-9]|0[0-9][1-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|0[0-9][1-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$|^localhost$|^$")],
                              description = "Host with a running ethereum client"
                          )
    rpc_port = IntegerField(
                              'Rpc-port:',
                              default = config['sai_arbitrage']['rpc-port'],
                              validators = [NumberRange(0,65535),Optional()],
                              description = "Port of rpc-host"
                          )
    server_cmd = SelectField(
                           'Server cmd:'
                         , choices = [
                              (
                                  "restart"
                                , config['flask']['RESTART']
                              )
                            , (
                                  "start"
                                , config['flask']['START']
                              )
                            , (
                                  "stop"
                                , config['flask']['STOP']
                              )
                            , (
                                  "nothing"
                                , config['flask']['NOTHING']
                              )
                                     ]
                        )
class SaiBiteForm(FlaskForm):
    config = configparser.ConfigParser()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    if config.read(dir_path + '/../keepers.conf') == []:
        print("Could not read configfile.\n")
        exit(-1)
    eth_from = StringField(
                             'Eth from:*',
                             validators = [Regexp("^0x[0-9a-zA-Z]{40}$")],
                             default = config['sai_bite']['eth-from'],
                             description = "Ethereum account from which to send transactions"
                          )
    frequency = IntegerField(
                               'Frequency:',
                               validators = [Optional()],
                               description = "Monitoring frequency in seconds"
                            )
    auth_token = StringField(
                               'Auth token:*',
                               validators = [DataRequired()],
                               description = "Token to enable to modify parameters."
                            ) 
    rpc_host = StringField(
                              'Rpc-host:',
                              default = config['sai_arbitrage']['rpc-host'],
                              validators =
                              [Regexp("((?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$))|^(([0-9]|[1-9][0-9]|0[0-9][1-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|0[0-9][1-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$|^localhost$|^$")],
                              description = "Host with a running ethereum client"
                          )
    rpc_port = IntegerField(
                              'Rpc-port:',
                              default = config['sai_arbitrage']['rpc-port'],
                              validators = [NumberRange(0,65535),Optional()],
                              description = "Port of rpc-host"
                          )
    server_cmd = SelectField(
                           'Server cmd:'
                         , choices = [
                              (
                                  "restart"
                                , config['flask']['RESTART']
                              )
                            , (
                                  "start"
                                , config['flask']['START']
                              )
                            , (
                                  "stop"
                                , config['flask']['STOP']
                              )
                            , (
                                  "nothing"
                                , config['flask']['NOTHING']
                              )
                                     ]
                        )
