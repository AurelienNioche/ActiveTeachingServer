import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from user_data.db_operation import backup_user_data

backup_user_data(bkp_file=os.path.join('data', "user.sql"))
