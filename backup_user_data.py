import os

os.system('pg_dump --data-only  --table question --table user ActiveTeaching --inserts > data/data_only.sql')