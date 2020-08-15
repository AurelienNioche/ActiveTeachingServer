# ActiveTeachingServer

Server part for the Active Teaching project. 

Instructions are given for MacOS (unless specified otherwise), using homebrew package manager (https://brew.sh/).


## Dependencies

#### Python

    brew install python3

Version used:
- Python 3.7.7

#### Python libraries

    pip3 install -r requirements.txt

Version used:

- pytz=2020.1
- python-dateutil=2.8.1
- Django=3.0.7
- numpy=1.18.5
- pandas=1.0.4
- scipy=1.4.1
- websocket-client=0.57.0
- requests=2.23.0
- channels=2.4.0


#### PostgreSQL (MacOS)

(Skip this if you are on GNU/Linux)

Install postgresql

    brew install postgresql
    
Run pgsql server (to have launchd start postgresql now and restart at login): 

    brew services start postgresql

OR if you don't want/need a background service:

    pg_ctl -D /usr/local/var/postgres start


#### PostgreSQL (GNU/Linux)

(Skip this if you are on MacOS)
Install postgresql

For Arch: https://wiki.archlinux.org/index.php/PostgreSQL

Make sure:
- you run commands starting with "$" as your normal/super user
 - you run commands starting by "[postgres]" as postgres

Switch to the user 'postgres':

    $ sudo -iu postgres
    
Switch bak

    postgres:$ exit

Initialize the database:

    postgres:$ initdb -D /var/lib/postgres/data

Start the postgresql service:

    $ systemctl start postgresql.service

(Optional) Enable the postgresql service:

    $ systemctl enable postgresql.service


## Configuration

#### PostgreSQL

Create user 'postgres' if it doesn't exist
    
    createuser postgres

Create a database named 'ActiveTeachingServer'

    createdb ActiveTeachingServer --owner postgres

#### Django

Move to the directory containing this script

    cd <path to the parent folder>/ActiveTeachingServer
    
Create a "credential.py" script

    nano ActiveTeachingServer/credentials.py

It should look like:
    
    SECRET_KEY = '<one arbirary combinaton of characters>'

    DB_NAME = 'ActiveTeachingServer'
    DB_USER = 'postgres'
    DB_PASSWORD = ''
    
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''

Prepare the DB (make migrations and migrate)

    python3 manage.py makemigrations
    python3 manage.py migrate

Create superuser in order to have access to admin interface

    python3 manage.py createsuperuser
    
#### Import Kanji data
    
Load sql backup of the kanji table
    
    python3 db_prepare.py
    
#### Import user data

Load sql backup of the tables containing user data

    python3 db_load_user_data.py
   
## Run

Run Django server using the Django command

    python3 manage.py runserver

## Extra information

#### Load specific session

Run:

    python3 db_load_xp_session.py
<<<<<<< HEAD
=======


#### Kanji table modifications
>>>>>>> master


#### Kanji table modifications

To load kanji table from the backup, run:

    python 3 db_prepare.py

#### Load experimental session

To make a backup of the user data, run:

    python3 db_backup_user_data.py

To *delete* the user data on the db and load the ones from the backup, run:
 
    python3 db_load_user_data.py


#### Manipulations of DB

Remove the db
    
    dropdb ActiveTeaching 

    
#### Sources

*  Kanji database: wanikani.com
    
 


### Deployment server

* Clone repository in /var/www/html/

* Create a virtual environment


        sudo apt-get install virtualenv
        cd /var/www/html/ActiveTeachingServer
        virtualenv -p python3 venv
        source venv/bin/activate
        pip install -r requirements.txt
        
In case of permission errors:

    sudo chmod -R o+rwx /var
    
* Install Apache2


        sudo apt install apache2 libapache2-mod-wsgi-py3
        a2enmod rewrite
        a2enmod proxy_http
        a2enmod proxy_wstunnel
   
* Edit apache2 config file `/etc/apache2/sites-enabled/000-default.conf`:


    <VirtualHost *:80>
    
        ....
            
        RewriteEngine on
        RewriteCond %{HTTP:UPGRADE} ^WebSocket$ [NC,OR]
        RewriteCond %{HTTP:CONNECTION} ^Upgrade$ [NC]
        RewriteRule .* ws://127.0.0.1:8001%{REQUEST_URI} [P,QSA,L]
    
    
        WSGIDaemonProcess active-teaching python-home=/var/www/html/ActiveTeachingServer/venv python-path=/var/www/html/ActiveTeachingServer
        WSGIProcessGroup active-teaching
    
        WSGIScriptAlias /admin /var/www/html/ActiveTeachingServer/ActiveTeachingServer/wsgi.py process-group=active-teaching
    
        <Directory /var/www/html/ActiveTeachingServer/ActiveTeachingServer>
            <Files wsgi.py>
                Require all granted
            </Files>
        </Directory>
    
* Create Daphne daemon file `/etc/systemd/system/daphne.service`


        [Unit]
        Description=ActiveTeaching Daphne Service
        After=network.target
        
        [Service]
        Type=simple
        User=www-data
        WorkingDirectory=/var/www/html/ActiveTeachingServer
        ExecStart=/var/www/html/ActiveTeachingServer/venv/bin/python /var/www/html/ActiveTeachingServer/venv/bin/daphne -p 8001 ActiveTeachingServer.asgi:application
   @     Restart=always
        
        [Install]
        WantedBy=multi-user.target
        
    * Run `sudo systemctl daemon-reload`
    * `sudo systemctl start daphne.service`
    * Check with `sudo systemctl status daphne.service`
    
    
### Build Unity

Do a build for Unity:

    Build Settings -> Build -> Save as 'Builds'

Structure is: 

    Builds
    -> Build/
    -> index.html
    -> TemplateData/
    -> UnityLoader.js

Be careful that the address is of the following form (don't include the port):
    
    ws://<domain>/


### Architecture server

    /var/www/html/
    -> ActiveTeachingServer
    -> Build
    -> index.html
    -> TemplateData
    -> UnityLoader.js


### List of config files
- /etc/apache2/sites-enabled/000-default.conf
- /etc/systemd/system/daphne.service
- /var/www/html/ActiveTeachingServer/credentials.py