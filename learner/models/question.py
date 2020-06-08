# Create your models here.
from django.db import models
from utils.time import string_to_datetime
import numpy as np

from learner.models import User, Session
from teaching_material.models import Kanji, Meaning


class QuestionManager(models.Manager):

    def create(self, user):

        item = user.leitner.ask(user=user)
        hist_question = user.get_historic()

        possible_replies = self.get_possible_replies(user=user, item=item)

        current_session = user.session_set.filter(close=False).first()

        obj = super().create(
            user=user,
            session=current_session,
            t=hist_question.count(),
            item=item,
            new=item not in [q.item for q in hist_question])

        for pr in possible_replies:
            obj.possible_replies.add(pr)

        return obj

    @classmethod
    def get_possible_replies(cls, item, user):

        """
        Select randomly possible replies, including the correct one
        """

        id_replies = [q.meaning.id for q in user.leitner.material.all()]
        id_correct_reply = item.meaning.id
        hist_id_reply = [q.user_reply.id for q in user.question_set.all()]

        for i in hist_id_reply:
            assert i in id_replies, i

        all_seen_replies = list(np.unique(hist_id_reply))

        if id_correct_reply in all_seen_replies:
            all_seen_replies.remove(id_correct_reply)

        missing = Question.N_POSSIBLE_REPLIES - (len(all_seen_replies) + 1)

        if missing <= 0:
            set_replies = all_seen_replies

        else:
            all_replies = list(np.unique(id_replies))
            for i in all_seen_replies:
                all_replies.remove(i)

            if id_correct_reply in all_replies:
                all_replies.remove(id_correct_reply)

            new_replies = \
                np.random.choice(all_replies, size=missing, replace=False)

            set_replies = list(new_replies) + all_seen_replies

        id_possible_replies = \
            [id_correct_reply, ] + list(np.random.choice(
                set_replies,
                size=Question.N_POSSIBLE_REPLIES - 1, replace=False))
        id_possible_replies = np.array(id_possible_replies)
        np.random.shuffle(id_possible_replies)

        return [Meaning.objects.get(id=i) for i in id_possible_replies]


class Question(models.Model):

    N_POSSIBLE_REPLIES = 6

    # Set at the moment of the creation
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    t = models.IntegerField(null=True)
    item = models.ForeignKey(Kanji, on_delete=models.SET_NULL,
                             null=True)

    possible_replies = models.ManyToManyField(Meaning,
                                              related_name="possible_replies")
    new = models.BooleanField()

    # Set after the user reply
    user_reply = models.ForeignKey(Meaning, on_delete=models.SET_NULL,
                                   null=True, default=None,
                                   related_name='user_reply')
    success = models.BooleanField(null=True, default=None)
    time_display = models.DateTimeField(default=None, null=True)
    time_reply = models.DateTimeField(default=None, null=True)

    objects = QuestionManager()

    class Meta:

        db_table = 'question'
        app_label = 'learner'

    def register_user_reply(self, id_user_reply,
                            time_display,
                            time_reply,
                            success):

        self.user_reply = Meaning.objects.get(id=id_user_reply)
        self.success = success
        self.time_display = string_to_datetime(time_display)
        self.time_reply = string_to_datetime(time_reply)
        self.save()

    @classmethod
    def next_question(cls, user, previous_question):

        if previous_question is not None and previous_question.session.done:
            question = None

        else:
            question = user.get_question_not_answered()

            if question is None:
                question = cls.objects.create(user=user)

        return question
