git submodule update --init --recursive
sudo apt-get install python3.6 gcc python3.6-dev python3.6-venv python3-pip
python3.6 -m pip install --upgrade pip
python3.6 -m pip install --upgrade venv
python3.6 -m venv flask
flask/bin/pip install --upgrade pip	
flask/bin/pip install flask
flask/bin/pip install flask-wtf
#flask/bin/pip install flipflop
