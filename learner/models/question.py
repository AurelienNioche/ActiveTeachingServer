# Create your models here.
from django.db import models
from datetime import datetime
import numpy as np

from learner.models import User, Session
from teaching_material.models import Kanji, Meaning


class QuestionManager(models.Manager):

    def create(self, possible_replies, **kwargs):
        # Do some extra stuff here on the submitted data before saving...

        # Now call the super method which does the actual creation
        obj = super().create(**kwargs)
        for pr in possible_replies:
            obj.possible_replies.add(pr)

        return obj


class Question(models.Model):

    N_POSSIBLE_REPLIES = 6

    # Set at the moment of the creation
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    t = models.IntegerField(default=-1)
    question = models.ForeignKey(Kanji, on_delete=models.SET_NULL,
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

    @staticmethod
    def convert_to_time(string_time):
        return datetime.strptime(string_time, '%Y-%m-%d %H:%M:%S.%f')

    @classmethod
    def register_user_reply(cls, question_id, id_user_reply,
                            time_display,
                            time_reply,
                            success):
        question = cls.objects.filter(id=question_id).first()

        if question is not None:
            question.user_reply = Meaning.objects.get(id=id_user_reply)
            question.success = success
            question.time_display = cls.convert_to_time(time_display)
            question.time_reply = cls.convert_to_time(time_reply)
            question.save()
        else:
            question = None

        return question

    @classmethod
    def next_question(cls, user, previous_question):

        if previous_question.session.is_done():
            previous_question.session.close = True
            previous_question.session.save()
            return None

        else:
            question = user.get_question_not_answered()

            if question is None:
                question = cls.create_new_question(
                    user=user)

            return question

    @classmethod
    def create_new_question(cls, user):

        kanji = user.leitner.ask(user=user)
        hist_question = user.get_historic()

        possible_replies = cls.get_possible_replies(user=user, kanji=kanji)

        question_entry = Question.objects.create(
            user=user,
            session=user.current_session,
            t=hist_question.count(),
            question=kanji,
            new=kanji not in [q.question for q in hist_question],
            possible_replies=possible_replies)

        return question_entry

    @classmethod
    def get_possible_replies(cls, kanji, user):

        """
        Select randomly possible replies, including the correct one
        """

        id_replies = [q.meaning.id for q in user.leitner.material.all()]
        id_correct_reply = kanji.meaning.id
        hist_id_reply = [q.user_reply.id for q in user.question_set.all()]

        for i in hist_id_reply:
            assert i in id_replies, i

        all_seen_replies = list(np.unique(hist_id_reply))

        if id_correct_reply in all_seen_replies:
            all_seen_replies.remove(id_correct_reply)

        missing = cls.N_POSSIBLE_REPLIES - (len(all_seen_replies) + 1)

        if missing <= 0:
            set_replies = all_seen_replies

        else:
            all_replies = list(np.unique(id_replies))
            for i in all_seen_replies:
                all_replies.remove(i)

            if id_correct_reply in all_replies:
                all_replies.remove(id_correct_reply)

            set_replies = \
                list(
                    np.random.choice(all_replies, size=missing, replace=False)) \
                + all_seen_replies

        id_possible_replies = \
            [id_correct_reply, ] + list(np.random.choice(
                set_replies,
                size=cls.N_POSSIBLE_REPLIES - 1, replace=False))
        id_possible_replies = np.array(id_possible_replies)
        np.random.shuffle(id_possible_replies)

        return [Meaning.objects.get(id=i) for i in id_possible_replies]