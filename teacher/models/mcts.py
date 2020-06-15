from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

import numpy as np
import pandas as pd
import datetime

from . psychologist import Psychologist, Learner

from teaching_material.models import Kanji
from learner.models.user import User

from . mcts_tools.mcts import MCTS, State


class LearnerStateParam:

    def __init__(self, learner_param, is_item_specific, learnt_threshold,
                 n_item, horizon, delta_time):

        self.horizon = horizon
        self.delta_time = delta_time

        self.n_item = n_item
        self.learnt_threshold = learnt_threshold

        self.learner_param = learner_param
        self.is_item_specific = is_item_specific


class LearnerState(State):

    def __init__(self, param, last_pres, n_pres, timestep, timestamp):

        self.param = param

        self.timestep = timestep
        self.timestamp = timestamp

        self.n_pres = n_pres
        self.last_pres = last_pres

        self._p_seen, self._seen = Learner.p_seen(
                param=self.param.learner_param,
                is_item_specific=self.param.is_item_specific,
                n_pres=n_pres,
                last_pres=last_pres,
                now=self.timestamp
        )

        self._reward = self._cpt_reward()
        self._actions = self._cpt_possible_actions()
        self._is_terminal = timestep == self.param.horizon - 1

        self.children = dict()

    @property
    def reward(self):
        return self._reward

    @property
    def possible_actions(self):
        """Returns an iterable of all actions which can be taken
        from this state"""
        return self._actions

    def take_action(self, action):
        """Returns the state which results from taking action 'action'"""

        if action in self.children:
            new_state = self.children[action]

        else:
            n_pres = self.n_pres.copy()
            n_pres[action] += 1
            last_pres = self.last_pres.copy()
            last_pres[action] = self.timestamp
            timestamp = self.timestamp + self.param.delta_time[self.timestep]
            timestep = self.timestep + 1
            new_state = LearnerState(
                param=self.param,
                last_pres=last_pres,
                n_pres=n_pres,
                timestep=timestep,
                timestamp=timestamp,
            )
            self.children[action] = new_state

        return new_state

    @property
    def is_terminal(self):
        """Returns whether this state is a terminal state"""
        return self._is_terminal

    def new_rollout_action(self):
        n_seen = np.sum(self._seen)

        if n_seen == 0:
            item = 0

        else:
            n_item = self.param.n_item
            tau = self.param.learnt_threshold

            min_p = np.min(self._p_seen)

            if n_seen == n_item or min_p <= tau:
                is_min = self._p_seen == min_p
                selection = np.arange(n_item)[self._seen][is_min]
                item = np.random.choice(selection)
            else:
                item = np.max(np.arange(n_item)[self._seen]) + 1

        return item

    def _cpt_reward(self):
        n_learnt = np.sum(self._p_seen > self.param.learnt_threshold)
        return n_learnt / self.param.n_item

    def _cpt_possible_actions(self):
        n_seen = np.sum(self._seen)
        if n_seen == 0:
            possible_actions = np.arange(1)
        elif n_seen == self.param.n_item:
            possible_actions = np.arange(self.param.n_item)
        else:
            already_seen = np.arange(self.param.n_item)[self._seen]
            new = np.max(already_seen) + 1
            possible_actions = list(already_seen) + [new]
        return possible_actions


class MCTSManager(models.Manager):

    def create(self, user, material, learnt_threshold, bounds, grid_size,
               is_item_specific, iter_limit, time_limit):

        n_item = material.count()
        id_items = [m.id for m in material]
        psychologist = Psychologist.objects.create(
            n_item=n_item,
            bounds=bounds,
            grid_size=grid_size,
            is_item_specific=is_item_specific)

        obj = super().create(
            user=user,
            psychologist=psychologist,
            id_items=id_items,
            n_item=n_item,
            learnt_threshold=learnt_threshold,
            iter_limit=iter_limit,
            time_limit=time_limit
        )

        obj.material.set(material)
        return obj


class MCTSTeacher(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)
    psychologist = models.OneToOneField(Psychologist,
                                        on_delete=models.CASCADE)

    material = models.ManyToManyField(Kanji, related_name="mcts_material")
    id_items = ArrayField(models.IntegerField(), default=list)
    n_item = models.IntegerField()

    learnt_threshold = models.FloatField()

    iter_limit = models.IntegerField(null=True)
    time_limit = models.FloatField(null=True)

    objects = MCTSManager()

    def _revise_goal(self):

        h = 10

        return h, [datetime.timedelta(seconds=2) for _ in range(h)]

    def _select_item(self):

        m = MCTS(iteration_limit=self.iter_limit)

        horizon, delta_time = self._revise_goal()

        learner_state = LearnerState(
            param=LearnerStateParam(
                learner_param=self.psychologist.inferred_learner_param(),
                is_item_specific=self.psychologist.is_item_specific,
                learnt_threshold=self.learnt_threshold,
                n_item=self.n_item,
                horizon=horizon,
                delta_time=delta_time
            ),
            n_pres=np.asarray(self.psychologist.n_pres),
            last_pres=pd.Series(self.psychologist.last_pres),
            timestamp=timezone.now(),
            timestep=0
        )

        item_idx = m.run(initial_state=learner_state)
        return item_idx

    def ask(self):

        last_q_entry = self.question_set.order_by("id").reverse().first()
        if last_q_entry is None:
            print("No previous entry: Present new item!")
            item_idx = 0

        else:
            last_was_success = last_q_entry.success
            last_time_reply = last_q_entry.time_reply
            idx_last_q = self.id_items.index(last_q_entry.item.id)

            self.psychologist.update(item=idx_last_q,
                                     response=last_was_success,
                                     timestamp=last_time_reply)

            item_idx = self._select_item()

        item = self.material.get(id=self.id_items[item_idx])
        return item
