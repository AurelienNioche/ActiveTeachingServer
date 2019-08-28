# ActiveTeachingServer

Server part for the Active Teaching project.


## Dependencies

#### Python

    brew install python3

#### Python libraries

* django
* psycopg2-binary (interaction with postgreSQL)
* channels (for websockets)
* websocket-client (only for using the 'bot_client.py' script)

    
    pip3 install django psycopg2-binary channels websocket-client
    
#### PostgreSQL

Install postgresql (all commands are given considering the application running under MacOs)

    brew install postgresql
    
Run pgsql server (to have launchd start postgresql now and restart at login): 

    brew services start postgresql

OR if you don't want/need a background service:

    pg_ctl -D /usr/local/var/postgres start

## Configuration

#### PostgreSQL

Create user and db

    createuser postgres
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
    
Load sql backup
    
    python3 prepare_db.py
    
   
## Run 

Run Django server using the Django command

    python3 manage.py runserver

## Extra information

#### Manipulations of DB

Remove the db
    
    dropdb ActiveTeaching 

    
#### Sources

*  Kanji database
   
   Coming from Tamaoka, K., Makioka, S., Sanders, S. & Verdonschot, R.G. (2017). 
www.kanjidatabase.com: a new interactive online database for psychological and linguistic research on Japanese kanji 
and their compound words. Psychological Research, 81, 696-708.
