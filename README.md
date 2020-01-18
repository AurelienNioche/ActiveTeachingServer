# ActiveTeachingServer

Server part for the Active Teaching project. 

Instructions are given for MacOS (unless specified otherwise), using homebrew package manager (https://brew.sh/).


## Dependencies

#### Python

    brew install python3

#### Python libraries

* django
* psycopg2-binary (interaction with postgreSQL)
* channels (for websockets)
* websocket-client (only for using the 'bot_client.py' script)
* pyGPGO 
* gensim

    pip3 install django psycopg2-binary channels websocket-client


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

Check the ArchWiki (https://wiki.archlinux.org/index.php/PostgreSQL). In short:

Install the postgresql package. It will also create a system user called postgres.

*Make sure you run commands starting with "$" as your normal/super user and those starting by "[postgres]" as postgres (use "sudo -iu postgres" and "exit" to swap between the two)*

Switch to the PostgreSQL user:

    $ sudo -iu postgres

Initialize the database:

    [postgres]$ initdb -D /var/lib/postgres/data

Start the postgresql service:

    $ systemctl start postgresql.service

(Optional) Enable the postgresql service:

    $ systemctl enable postgresql.service


## Configuration

#### PostgreSQL

Create user 'postgres' if it doesn't exist
    
    createuser postgres

Create a database named 'ActiveTeaching'

    createdb ActiveTeaching --owner postgres

#### Django

Move to the directory containing this script

    cd <path to the parent folder>/ActiveTeachingServer

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

#### Kanji table modifications

To make a backup from the kanji table, run:

    python3 db_backup_kanji_table

To load kanji table from the backup, run:

    python 3 db_prepare.py

#### User data modifications

To make a backup of the user data, run:

    python3 db_backup_user_data.py

To *delete* the user data on the db and load the ones from the backup, run:
 
    python3 db_load_user_data.py


#### Manipulations of DB

Remove the db
    
    dropdb ActiveTeaching 

    
#### Sources

*  Kanji database
   
   Coming from Tamaoka, K., Makioka, S., Sanders, S. & Verdonschot, R.G. (2017). 
www.kanjidatabase.com: a new interactive online database for psychological and linguistic research on Japanese kanji 
and their compound words. Psychological Research, 81, 696-708.


### Deployment server

* Create a virtual environment

        sudo apt-get install virtualenv
        cd <code>
        virtualenv -p python3 venv
        source venv/bin/activate
        pip install ...
    
* Install Apache2

        sudo apt install apache2 libapache2-mod-wsgi-py3
        a2enmod rewrite
        a2enmod proxy_http
        a2enmod proxy_wstunnel
   
* Add to apache2 config file (`/etc/apache2/sites-enabled/000-default.conf`) inside `<VirtualHost *:80>`

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
    
* Create Daphne daemon file at `/etc/systemd/system/daphne.service`

        [Unit]
        Description=ActiveTeaching Daphne Service
        After=network.target
        
        [Service]
        Type=simple
        User=www-data
        WorkingDirectory=/var/www/html/ActiveTeachingServer
        ExecStart=/var/www/html/ActiveTeachingServer/venv/bin/python /var/www/html/ActiveTeachingServer/venv/bin/daphne -p 8001 ActiveTeachingServer.asgi:application
        Restart=on-failure
        
        [Install]
        WantedBy=multi-user.target
        
    * Run `sudo systemctl daemon-reload`
    * `sudo systemctl start daphne.service`
    * Check with `sudo systemctl status daphne.service`
