from config import config

from user.models.session import Session


def run(active_teaching_engine,
        leitner_teaching_engine,
        first_session, user,
        begin_with_active):

    teaching_engines = [active_teaching_engine, leitner_teaching_engine]
    if not begin_with_active:
        teaching_engines.reverse()

    session_time = []

    session_is_first = []

    for ss_idx in range(config.N_SESSION + 1):

        for i, te in enumerate(teaching_engines):

            if not session_time:

                available_time = first_session
                session_time.append(available_time)
                session_is_first.append(True)

            else:
                if session_is_first[-1]:
                    available_time = session_time[-1] \
                                     + config.TIME_DELTA_TWO_TEACHERS

                else:
                    available_time = session_time[-2] \
                                     + config.TIME_DELTA_TWO_SESSIONS

                session_time.append(available_time)
                session_is_first.append(not session_is_first[-1])

            if ss_idx < config.N_SESSION:

                Session.objects.create(
                    user=user,
                    available_time=available_time,
                    n_iteration=config.N_ITER_PER_SESSION,
                    teaching_engine=te,
                    is_evaluation=False)

            else:
                Session.objects.create(
                    user=user,
                    available_time=available_time,
                    n_iteration=None,
                    teaching_engine=te,
                    is_evaluation=True)
