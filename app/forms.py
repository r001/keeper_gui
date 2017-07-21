from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DecimalField, SelectField
from wtforms.validators import DataRequired,Regexp

class LoginForm(FlaskForm):
    app = Flask(__name__)
    app.config.from_object('config')
    eth_from = StringField('eth_from', validators=[Regexp("^0x[0-9a-zA-Z]{40}")], 
                            description="Ethereum account from which to send transactions")
    frequency = DecimalField('frequency', default="5", description="Monitoring frequency in seconds")
    minimum_profit = DecimalField('minimum_profit', default=".01", description="Minimum profit in SAI from one arbitrage operation")
    maximum_engagement = DecimalField('maximum_engagement', default=1000, description="Maximum engagement in SAI in one arbitrage operation")
    tx_manager = StringField('tx_manager', validators=[Regexp("^0x[0-9a-zA-Z]{40}")], description="Address of the TxManager to use for multi-step arbitrage") 
    keeper = SelectField('keeper', choices=[("sai_ar",
    app.config['SAI_AR']),("sai_bi", app.config['SAI_BI'])])
