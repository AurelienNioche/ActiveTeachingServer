import numpy as np


def objective(model,
              hist_question,
              hist_success,
              param,
              task_param, ):
    n_item = task_param['n_item']

    seen = np.zeros(n_item, dtype=bool)

    n_possible_replies = task_param['n_possible_replies']

    n_iteration = len(hist_question)
    agent = model(param=param, n_iteration=n_iteration,
                  **task_param)
    log_likelihood_sum = 1

    for t in range(n_iteration):

        item = hist_question[t]

        # Ignore first presentation
        if seen[item]:
            p_r = agent.p_recall(item=item)

            p_random = (1 - p_r) / n_possible_replies

            p_choose_correct = p_r + p_random

            s = hist_success[t]

            lh = p_choose_correct if s else p_random

            # if lh > 0:
            #     log_likelihood_sum = -np.inf
            #     break
            # else:
            log_likelihood_sum += np.log(lh)

        else:
            seen[item] = True

        agent.learn(item=item)

    value = - log_likelihood_sum
    return value

# def objective(model,
#               hist_question,
#               hist_success,
#               param,
#               task_param,):
#
#     p_random = 1/task_param['n_possible_replies']
#
#     n_iteration = len(hist_question)
#     agent = model(param=param, n_iteration=n_iteration,
#                   **task_param)
#     diff = np.zeros(n_iteration)
#
#     for t in range(n_iteration):
#         item = hist_question[t]
#         p_r = agent.p_recall(item=item)
#         p_choose_correct = min(1, p_r + p_random)
#
#         s = hist_success[t]
#
#         diff[t] = (s - p_choose_correct)
#
#         agent.learn(item=item)
#
#     diff = np.power(diff, 2)
#     value = np.sum(diff)
#     return value
