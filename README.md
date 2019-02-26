# ActiveTeachingServer

Server part for the Active Teaching project.


## Prerequisites


### Python libraries

* django
* psycopg2-binary (interaction with postgreSQL)
* channels (for websockets)
* websocket-client (only for using the 'bot_client.py' script)

### PostgreSQL

Install postgresql (all commands are given considering the application running under MacOs)

    brew install postgresql
    
Run pgsql server (to have launchd start postgresql now and restart at login): 

    brew services start postgresql

OR if you don't want/need a background service:

    pg_ctl -D /usr/local/var/postgres start

Create user and db

    createuser dasein
    createdb ActiveTeaching --owner dasein

### Initialize Django

Make migrations and migrate

    python3 manage.py makemigrations
    python3 manage.py migrate
   
### Run Django server
   
Using the Django command

    python3 manage.py runserver
    
## Manipulations of DB

If you need to reset the table contents, you can write a script 'reset.sql' and call it:
    
    psql ActiveTeaching -a -f reset.sql

If you need to remove the db
    
    dropdb ActiveTeaching 