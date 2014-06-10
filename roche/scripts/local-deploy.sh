
# Keep in sync with dedalus-infrastructure (but without apache2)
sudo apt-get install -y		\
	python-django		\
	python-django-south	\
	python-imaging		\
	python-lxml		\
	python-markdown		\
	python-memcache		\
	python-pip		\
	python-ply		\
	python-psycopg2		\
	python-sorl-thumbnail	\
	gettext			\
	git			\
	libpython-dev		\
	tesseract-ocr		\
	tesseract-ocr-chi-tra

sudo pip install -r requirements.txt

# Export Docker link variables
export DOCKER_PASSWORD='quoongi'
export DB_PORT_5432_TCP_ADDR='localhost'
export DB_PORT_5432_TCP_PORT='5432'
export XMLDB_PORT_8080_TCP_ADDR='localhost'
export XMLDB_PORT_8080_TCP_PORT='8080'
export SPARQL_PORT_3030_TCP_ADDR='localhost'
export SPARQL_PORT_3030_TCP_PORT='3030'

python manage.py syncdb --noinput
python manage.py compilemessages
