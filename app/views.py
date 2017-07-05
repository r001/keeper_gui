from flask import render_template,make_response,Response
from app import app
from time import sleep

@app.route('/')
def index():
    return render_template('index.html',
            title='Keeper monitoring'
            )
@app.route('/stream')
def stream():
	def generate():
		with open('job.log') as f:
			read_data = f.read()
		f.close()
		return read_data 
	return app.make_response(generate())
#return app.response_class(generate(), mimetype='text/plain')
