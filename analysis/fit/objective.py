import numpy as np


def objective(model,
              hist_question,
              hist_success,
              param,
              task_param,):

    n_iteration = len(hist_question)
    agent = model(param=param, n_iteration=n_iteration,
                  **task_param)
    diff = np.zeros(n_iteration)

    for t in range(n_iteration):
        item = hist_question[t]
        p_r = agent.p_recall(item=item)
        s = hist_success[t]

        diff[t] = (s - p_r)

        agent.learn(item)

    diff = np.power(diff, 2)
    value = np.sum(diff)
    return value
