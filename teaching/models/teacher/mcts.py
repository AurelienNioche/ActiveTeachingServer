from django.db import models

from learner.models.user import User

import numpy as np

from . mcts_tools.mcts import MCTS


class LearnerStateParam:

    def __init__(self, learner, learner_param, learnt_threshold,
                 n_item, horizon, timestamps):

        self.learner = learner

        self.horizon = horizon
        self.timestamps = timestamps

        self.n_item = n_item
        self.learnt_threshold = learnt_threshold

        self.learner_param = learner_param


class LearnerState:

    def __init__(self, param, hist, ts, timestep):

        self.param = param

        self.timestep = timestep

        self.hist = hist
        self.ts = ts

        p_seen, seen = self.param.learner.p_seen_spec_hist(
            param=self.param.learner_param,
            hist=hist,
            ts=ts)

        n_seen = np.sum(seen)

        self.reward = self._cpt_reward(p_seen)
        self.possible_actions = self._cpt_possible_actions(n_seen=n_seen)
        self.is_terminal = timestep == self.param.horizon
        self.rollout_action = self._cpt_rollout_action(n_seen=n_seen,
                                                       p_seen=p_seen)

        self.children = dict()

    def take_action(self, action):
        """Returns the state which results from taking action 'action'"""

        if action in self.children:
            new_state = self.children[action]

        else:
            timestep = self.timestep + 1
            new_state = LearnerState(
                param=self.param,
                hist=self.hist + [action, ],
                ts=self.ts + [self.param.timetamps[timestep]],
                timestep=timestep,
            )
            self.children[action] = new_state

        return new_state

    def _cpt_rollout_action(self, p_seen, n_seen):

        if n_seen:
            n_item = self.param.n_item
            tau = self.param.learnt_threshold

            min_p = p_seen.min()

            if n_seen == n_item or min_p <= tau:
                item = p_seen.argmin()
            else:
                item = n_seen
        else:
            item = 0

        return item

    def _cpt_reward(self, p_seen):
        return np.mean(p_seen > self.param.learnt_threshold)

    def _cpt_possible_actions(self, n_seen):
        if n_seen == self.param.n_item:
            possible_actions = np.arange(self.param.n_item)
        else:
            possible_actions = np.arange(n_seen+1)
        return possible_actions


class MCTSTeacher(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    n_item = models.IntegerField()

    learnt_threshold = models.FloatField()

    iter_limit = models.IntegerField()
    time_limit = models.FloatField()
    time_per_iter = models.IntegerField()
    horizon = models.IntegerField()
    iter = models.IntegerField()

    ss_n_iter = models.IntegerField()
    ss_n_iter_between = models.IntegerField()

    # So need to set them at creation ---
    ss_it = models.IntegerField(default=0)

    class Meta:

        db_table = 'mcts'
        app_label = 'teaching'

    def _revise_goal(self, now):

        self.ss_it += 1
        if self.ss_it == self.ss_n_iter - 1:
            self.ss_it = 0

        remain = self.ss_n_iter - self.ss_it

        self.iter += 1
        if self.iter == self.horizon:
            self.iter = 0
            h = self.horizon
        else:
            h = self.horizon - self.iter

        # delta in timestep (number of iteration)
        delta_ts = np.arange(h + 1, dtype=int)

        if remain < h + 1:
            delta_ts[remain:] += self.ss_n_iter_between
            assert h - remain <= self.ss_n_iter, "case not handled!"

        timestamps = now + delta_ts * self.time_per_iter

        return h, timestamps

    def _select_item(self, learner, param, now):

        m = MCTS(iteration_limit=self.iter_limit, time_limit=self.time_limit)

        horizon, timestamps = self._revise_goal(now)

        learner_state = LearnerState(
            param=LearnerStateParam(
                learner=learner,
                learner_param=param,
                learnt_threshold=self.learnt_threshold,
                n_item=self.n_item,
                horizon=horizon,
                timestamps=timestamps),
            hist=learner.hist,
            ts=learner.ts,
            timestep=0
        )

        item_idx = m.run(initial_state=learner_state)
        return item_idx

    def ask(self, learner, param, now):
        return self._select_item(learner=learner, param=param, now=now)
