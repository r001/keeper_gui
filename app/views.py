from flask import render_template,make_response,Response,flash,redirect,request
from app import app
from time import sleep
import subprocess
from .forms import LoginForm
import os

title="Dai Credit System - Keeper Monitoring"
def reverse_readline(filename, buf_size=8192):
    """a generator that returns the lines of a file in reverse order"""
    with open(filename) as fh:
        segment = None
        offset = 0
        fh.seek(0, os.SEEK_END)
        file_size = remaining_size = fh.tell()
        while remaining_size > 0:
            offset = min(file_size, offset + buf_size)
            fh.seek(file_size - offset)
            buffer = fh.read(min(remaining_size, buf_size))
            remaining_size -= buf_size
            lines = buffer.split('\n')
            # the first line of the buffer is probably not a complete line so
            # we'll save it and append it to the last line of the next buffer
            # we read
            if segment is not None:
                # if the previous chunk starts right from the beginning of line
                # do not concact the segment to the last line of new chunk
                # instead, yield the segment first
                if buffer[-1] is not '\n':
                    lines[-1] += segment
                else:
                    yield segment
            segment = lines[0]
            for index in range(len(lines) - 1, 0, -1):
                if len(lines[index]):
                    yield lines[index]
        # Don't yield None if the file was empty
        if segment is not None:
            yield segment
@app.route('/')
def index():
    form = LoginForm();
    return render_template('index.html', title=title, form=form )

@app.route('/stream')
def stream():
    last_id=request.args['last_id'];
    def inner(last_id):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        reverse_lines = reverse_readline(dir_path+"/../sai_arbitrage.log")
        start=False
        for pos, line in enumerate(reverse_lines):
            if last_id != "" and line.startswith(last_id):
                break
            yield line
    return Response(inner(last_id), mimetype='text/html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('index.html',
                           title=title,
                           form=form)
