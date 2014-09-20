
# Keep in sync with dedalus-infrastructure (but without apache2)
sudo apt-get install -y		\
	python-lxml		\
	python-pip		\
	python-ply		\
	libpython-dev

sudo pip install -r requirements.txt

# Export Docker link variables
export DOCKER_PASSWORD='iSoof4Vo'
export DB_PORT_5432_TCP_ADDR='localhost'
export DB_PORT_5432_TCP_PORT='5432'
export XMLDB_PORT_8080_TCP_ADDR='localhost'
export XMLDB_PORT_8080_TCP_PORT='8080'
export SPARQL_PORT_3030_TCP_ADDR='localhost'
export SPARQL_PORT_3030_TCP_PORT='3030'
export RABBITMQ_PORT_5672_TCP_ADDR='localhost'
export RABBITMQ_PORT_5672_TCP_PORT='5672'
export DJANGO_SETTINGS_MODULE=roche.settings

python manage.py syncdb --noinput
python manage.py compilemessages
