# ActiveTeachingServer

Server part for the Active Teaching project.


## Prerequisites

### Python

    brew install python3

### Python libraries

* django


    pip3 install django

* psycopg2-binary (interaction with postgreSQL)


    pip3 install psycopg2-binary
    
* channels (for websockets)


    pip3 install channels    

* websocket-client (only for using the 'bot_client.py' script)


    pip3 install websocket-client
    
### PostgreSQL

Install postgresql (all commands are given considering the application running under MacOs)

    brew install postgresql
    
Run pgsql server (to have launchd start postgresql now and restart at login): 

    brew services start postgresql

OR if you don't want/need a background service:

    pg_ctl -D /usr/local/var/postgres start

Create user and db

    createuser dasein
    createdb ActiveTeaching --owner postgres

### Initialize Django

Prepare the DB (make migrations and migrate)

    python3 manage.py makemigrations
    python3 manage.py migrate
    
Create superuser in order to have access to admin interface

    python3 manage.py createsuperuser
   
### Run Django server
   
Using the Django command

    python3 manage.py runserver
    
## Manipulations of DB

If you need to remove the db
    
    dropdb ActiveTeaching 

If you need to reset the table contents, you can write a script 'reset.sql' and call it:
    
    psql ActiveTeaching -a -f reset.sql
    
    
   ## Info on the database
   
   Coming from Tamaoka, K., Makioka, S., Sanders, S. & Verdonschot, R.G. (2017). 
www.kanjidatabase.com: a new interactive online database for psychological and linguistic research on Japanese kanji and their compound words. Psychological Research, 81, 696-708.
