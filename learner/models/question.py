# Create your models here.
from django.db import models
from utils.time import string_to_datetime
import numpy as np

from teaching.models.teaching_engine import TeachingEngine
from teaching_material.models import Kanji, Meaning

from experimental_condition.models.session import Session

from learner.models.user import User


class QuestionManager(models.Manager):

    def create(self, teaching_engine, session, item, new, possible_replies):

        obj = super().create(
            session=session,
            item=item,
            new=new, teaching_engine=teaching_engine)

        obj.possible_replies.set(possible_replies)
        return obj


class Question(models.Model):

    N_POSSIBLE_REPLIES = 6

    # Set at the moment of the creation ----------------------------------
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    teaching_engine = models.ForeignKey(TeachingEngine,
                                        on_delete=models.CASCADE, null=True)

    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Kanji, on_delete=models.SET_NULL, null=True)

    possible_replies = models.ManyToManyField(Meaning,
                                              related_name="possible_replies")
    new = models.BooleanField()

    # Set after the user reply --------------------------------------------
    user_reply = models.ForeignKey(Meaning,
                                   on_delete=models.SET_NULL,
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

            session = Session.get_user_session(user=user)
            teaching_engine = session.teaching_engine

            question = \
                teaching_engine.question_set.filter(user_reply=None).first()

            if question is None:
                item = teaching_engine.ask()
                hist_question = \
                    teaching_engine.question_set.exclude(user_reply=None)

                new = hist_question.filter(item=item).count() == 0

                possible_replies = \
                    cls.get_possible_replies(teaching_engine=teaching_engine,
                                             item=item)

                # current_session = \
                #     teacher.user.session_set.filter(close=False).first()

                question = cls.objects.create(
                    teaching_engine=teaching_engine,
                    session=session,
                    item=item,
                    new=new,
                    possible_replies=possible_replies,
                )

        return question

    @classmethod
    def get_possible_replies(cls, item, teaching_engine):

        """
        Select randomly possible replies, including the correct one
        """

        id_correct_reply = item.meaning.id
        id_replies = teaching_engine.material.values_list(
            "meaning__id", flat=True)
        hist_id_reply = teaching_engine.question_set.values_list(
            "user_reply__id", flat=True)

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

        return Meaning.objects.filter(id__in=id_possible_replies)
