from django.db import models

from user.models.user import User


class ForwardConditionManager(models.Manager):

    def create(self, user, first_session, begin_with_active,
               is_item_specific, previous_email=None):

        from experimental_condition.models.experiment import \
            creation_material, creation_session, creation_engine

        leitner_m, active_teaching_m = \
            creation_material.run(previous_email=previous_email)

        leitner_te = creation_engine.create_leitner_engine(
            user=user,
            material=leitner_m)

        active_teaching_te = creation_engine.create_exp_decay_forward_engine(
            user=user,
            material=active_teaching_m,
            is_item_specific=is_item_specific)

        creation_session.run(
            active_teaching_engine=active_teaching_te,
            leitner_teaching_engine=leitner_te,
            first_session=first_session, user=user,
            begin_with_active=begin_with_active)

        obj = super().create(user=user)
        return obj


class ForwardCondition(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    objects = ForwardConditionManager()

    class Meta:

        db_table = 'forward_condition'
        app_label = 'experimental_condition'

    def new_session(self):
        return None
