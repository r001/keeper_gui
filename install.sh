t submodule update --init --recursive
sudo apt-get install python3.6 gcc python3.6-dev python3.6-venv python3-pip python3-daemon
python3.6 -m pip install --upgrade pip
python3.6 -m pip install --upgrade venv

#create virtual environment for flask
python3.6 -m venv flask

#upgrade pyhon3.6 module pip to up-to-date version for flask virtual env
flask/bin/pip install --upgrade pip

#install basic flask features for flask virtualenv
flask/bin/pip install flask
#install form handling module for flask virtualenv
flask/bin/pip install flask-wtf

#get script's directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ESCDIR=`echo $DIR|sed -e "s-/-\\\\\\/-g"`
#create sai_arbitrage.service and sai_bite.service file for systemd
sed -e "s/__pythonpath__/${ESCDIR}\/keeper\/:${ESCDIR}\/keeper\/keepers\//g" "${DIR}/app/sai_arbitrage.service.template" > "${DIR}/app/sai_arbitrage.service"
sed -i "s/__working_directory__/${ESCDIR}/g" "${DIR}/app/sai_arbitrage.service" 
sed -e "s/__pythonpath__/${ESCDIR}\/keeper\/:${ESCDIR}\/keeper\/keepers\//g" "${DIR}/app/sai_bite.service.template" > "${DIR}/app/sai_bite.service"
sed -i "s/__working_directory__/${ESCDIR}/g" "${DIR}/app/sai_bite.service" 

#add services to systemv
ln -s "${DIR}/app/sai_arbitrage.service" /etc/systemd/system/sai_arbitrage.service
ln -s "${DIR}/app/sai_bite.service" /etc/systemd/system/sai_bite.service

#make possible for www-data user (apache2) to control sai services
echo 'www-data ALL=NOPASSWD: /bin/systemctl start sai_arbitrage.service' | sudo EDITOR='tee -a' visudo >>/dev/null
echo 'www-data ALL=NOPASSWD: /bin/systemctl restart sai_arbitrage.service' | sudo EDITOR='tee -a' visudo >>/dev/null
echo 'www-data ALL=NOPASSWD: /bin/systemctl stop sai_arbitrage.service' | sudo EDITOR='tee -a' visudo >>/dev/null
echo 'www-data ALL=NOPASSWD: /bin/systemctl start sai_bite.service' | sudo EDITOR='tee -a' visudo >>/dev/null
echo 'www-data ALL=NOPASSWD: /bin/systemctl restart sai_bite.service' | sudo EDITOR='tee -a' visudo >>/dev/null
echo 'www-data ALL=NOPASSWD: /bin/systemctl stop sai_bite.service' | sudo EDITOR='tee -a' visudo >>/dev/null

#reload system service list
/bin/systemctl daemon-reload

#start services
service sai_arbitrage start
service sai_bite start
