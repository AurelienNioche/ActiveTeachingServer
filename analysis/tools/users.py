import os
import pickle

from learner.models import User

BKP_FOLDER = os.path.join("data", "Pilot20190902", "pickle", "learner")
BKP_FILE = os.path.join(BKP_FOLDER, "learner.p")
os.makedirs(BKP_FOLDER, exist_ok=True)


def get(force=False):

    if not force and os.path.exists(BKP_FILE):
        user_id = pickle.load(open(BKP_FILE, 'rb'))
    else:
        user_id = [u.id for u in User.objects.all().order_by('id')]
        pickle.dump(user_id, open(BKP_FILE, 'wb'))

    return user_id
