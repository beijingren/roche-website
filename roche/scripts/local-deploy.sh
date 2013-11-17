
# Keep in sync with dedalus-infrastructure (but without apache2)
sudo apt-get install -y		\
	python-django		\
	python-django-mptt	\
	python-django-sekizai	\
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

python manage.py compilemessages

# Docker link variables
DOCKER_PASSWORD=''
DB_PORT_5432_TCP_ADDR='localhost'
DB_PORT_5432_TCP_PORT='5432'

export DOCKER_PASSWORD
export DB_PORT_5432_TCP_ADDR
export DB_PORT_5432_TCP_PORT
