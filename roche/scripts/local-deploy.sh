
# Keep in sync with dedalus-infrastructure (but without apache2)
sudo apt-get install -y		\
	python-django		\
	python-django-celery	\
	python-django-south	\
	python-imaging		\
	python-lxml		\
	python-markdown		\
	python-pip		\
	python-ply		\
	python-psycopg2		\
	python-sorl-thumbnail	\
	gettext			\
	git			\
	libpython-dev

sudo pip install -r requirements.txt

# Export Docker link variables
export DOCKER_PASSWORD=''
export DB_PORT_5432_TCP_ADDR='localhost'
export DB_PORT_5432_TCP_PORT='5432'
export XMLDB_PORT_8080_TCP_ADDR='localhost'
export XMLDB_PORT_8080_TCP_PORT='8080'

python manage.py syncdb --noinput
python manage.py compilemessages
