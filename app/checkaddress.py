#!/usr/bin/env python3.6 
import fileinput
from ethereum.utils import check_checksum, sha3, encode_hex
import re
import datetime
import time

normal_color="green"
alert_color="red"
alert_color_eth_address="purple"
number_color="yellow"
date_color="blue"
traceback = False

for line in fileinput.input():
    line = str.rstrip(line)
    date = re.sub(r'^(\S*\s+\S*\s+)(.*)',"\g<1>",line)
    line = re.sub(r'^(\S*\s+\S*\s+)(.*)',"\g<2>",line)
    #check for valid ethereum addresses
    matches = re.findall(r"0x[0-9a-zA-Z]*",line)
    for match in matches:
        if len(match) == 42 and check_checksum(match):
            line = line.replace(match,f"<font color=\"{normal_color}\">{match}</font>")
        else:
            line = line.replace(match,f"<font color=\"{alert_color_eth_address}\">{match}</font>")
    #traceback
    if re.search(r'Traceback',line,re.IGNORECASE):
        traceback=True
        line = f"<font color=\"{alert_color}\">"+line+"</font>"
    if traceback:
        line = f"<font color=\"{alert_color}\">"+line+"</font>"
    if re.search(r'Error',line,re.IGNORECASE):
        traceback=False
    
    #numbers are yellow
    line = re.sub(r'\b([+-]*[0-9]*\.*[0-9]+(E[0-9]+)*)\b',f'<font color="{number_color}">\g<1></font>',line)

    #line becomes red if failed or error
    if re.search(r'fail|error|exception',line, re.IGNORECASE):
        line = f"<font color=\"{alert_color}\">"+line+"</font>"
    
    #add hash and date time to beginning
    line = encode_hex(sha3(line+str(time.clock())))+f" <font\
    color='{date_color}'>" + date + "</font>" + line
    line = line + '<br/>'
    print(line)
