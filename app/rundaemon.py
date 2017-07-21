#!/usr/bin/env python3.6
import fileinput
from ethereum.utils import check_checksum, sha3, encode_hex
import re
import datetime
import time
import argparse
import sai_arbitrage
import sai_bite
import sys
import configparser
import unittest.mock

class RunDaemon:
    def __init__(self):
        parser = argparse.ArgumentParser(description=f"{type(self).__name__}")

        parser.add_argument("keeper"
        , help="Keeper to start"
        , choices=['sai_arbitrage','sai_bite']
        , type=str
        , default="sai_arbitrage"
        , nargs="?")
        
        self.arguments = parser.parse_args()
        self.run_script = self.arguments.keeper
        self.runDaemon()
    def runDaemon(self):
        stderr = sys.stderr
        pr = PrettyPrint(self.run_script,stderr)
        sys.stderr = pr
        config = configparser.ConfigParser()
        config.read('../keepers.conf')

        mocked_argv = [self.run_script+".py"] + \
        [   
            item for sublist in 
            [   
                [ "--"+k, config[self.run_script][k] ] 
                for k in config[self.run_script] 
                if config[self.run_script][k] != ''
            ] 
            for item in sublist
        ]

        print(str(mocked_argv))
        with unittest.mock.patch('sys.argv',mocked_argv):
            if self.run_script == 'sai_arbitrage':
                sai_arbitrage.SaiArbitrage().start()
            elif self.run_script == 'sai_bite':
                sai_bite.SaiBite().start()
class PrettyPrint:
    def __init__(self, run_script, stderr):
        self.normal_color="green"
        self.alert_color="red"
        self.warning_color="orange"
        self.alert_color_eth_address="purple"
        self.number_color="yellow"
        self.date_color="blue"
        self.traceback = False
        self.run_script = run_script
        self.stderr = stderr
    def flush(self):
        pass
    def write(self,buf):
        save_stderr = sys.stderr
        sys.stderr = self.stderr
        for line in buf.rstrip().splitlines():
            line = line.rstrip()
            f = re.search(r'^\d{4}-\d\d-\d\d\s+\d\d:\d\d:\d\d,\d+\s+',line)
            if f:
                date=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]+"(UTC) "
                line = re.sub(r'^(\S*\s+\S*\s+)(.*)',"\g<2>",line)
            else:
                date=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]+"(UTC) "
            print(line,file=sys.stdout)
            sys.stdout.flush()
            #check for valid ethereum addresses
            matches = re.findall(r"0x[0-9a-zA-Z]*",line)
            for match in matches:
                if len(match) == 42 and check_checksum(match):
                    line = line.replace(match,f"<font color=\"{self.normal_color}\">{match}</font>")
                else:
                    line = line.replace(match,f"<font color=\"{self.alert_color_eth_address}\">{match}</font>")
            #self.traceback
            if re.search(r'Traceback',line,re.IGNORECASE):
                self.traceback=True
                line = f"<font color=\"{self.alert_color}\">"+line+"</font>"
            if self.traceback:
                line = f"<font color=\"{self.alert_color}\">"+line+"</font>"
            if re.search(r'Error',line,re.IGNORECASE):
                self.traceback=False
            
            #numbers are yellow
            line = re.sub(r'\b([+-]*[0-9]*\.*[0-9]+(E[0-9]+)*)\b',f'<font color="{self.number_color}">\g<1></font>',line)

            #line becomes red if failed or error
            if re.search(r'fail|error|exception|CRITICAL',line, re.IGNORECASE):
                line = f"<font color=\"{self.alert_color}\">"+line+"</font>"
            if re.search(r'WARNING',line ):
                line = f"<font color=\"{self.warning_color}\">"+line+"</font>"
             
            #add hash and date time to beginning
            line = encode_hex(sha3(line+str(time.clock())))+f" <font\
            color='{self.date_color}'>" + date + "</font>" + line
            line = line + "<br/>\n"

            logfile = open("../log/" + self.run_script + ".log", "a")
            logfile.write(line)
            logfile.close() 
        sys.stderr = save_stderr
if __name__ == '__main__':
    RunDaemon()