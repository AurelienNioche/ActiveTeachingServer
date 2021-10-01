import pandas as pd
import numpy as np
import os


def create_demographic_data(df, user_mail):

    path = "subscriptions/20200924-active-teaching-data.csv"
    output_path = "data/demographic_info.csv"

    assert os.path.exists(path), \
        "The subscriptions data are not available"

    df_demo = pd.read_csv(path)

    # In[130]:

    user = df.user.unique()
    gender = np.zeros(len(user), dtype=object)
    age = np.zeros(len(user), dtype=int)
    native_lang = np.zeros(len(user), dtype=object)
    other_lang = np.zeros(len(user), dtype=object)

    for u in user:
        df_demo_u = df_demo[df_demo.app_email == user_mail[u]]
        gender[u] = df_demo_u.Gender.item().upper()
        age[u] = df_demo_u.Age.item()
        native_lang[u] = df_demo_u.NativeLanguage.item().lower()
        other_lang[u] = df_demo_u.OtherLanguages.item().lower()

    df_demo_new = pd.DataFrame({
        "user": user,
        "gender": gender,
        "age": age,
        "native_lang": native_lang,
        "other_lang": other_lang
    })

    df_demo_new.to_csv(output_path, index=False)


def create_clean_data():

    path = "data/data_full.csv"
    output_path = "data/data.csv"

    assert os.path.exists(path), \
        "The script 'get_data_full.py' should be called before"

    df = pd.read_csv(path, index_col=0,
                     dtype={"success": "boolean"},
                     parse_dates=['ts_display', 'ts_reply'])
    # Keep only users from the last experiment and that did it until the end
    # (6 + 1  sessions for each teacher)
    df.drop(df[(df.domain != "active.fi") | (df.n_session_done != 14)].index,
            inplace=True)

    # Rename users with IDs
    user_id, user_mail = pd.factorize(df.user)
    df.user = user_id

    # Sort by user and values
    df.sort_values(["user", "ts_display"], inplace=True)

    # Remove unnecessary columns
    df.drop(["domain", "item", "psy_md", "learner_md", "n_session_done"],
            axis=1, inplace=True)

    # Rename few things
    df.replace({"condition": {"ForwardCondition": "conservative",
                              "ThresholdCondition": "myopic"}}, inplace=True)
    df.replace({"teacher_md": {"forward": "conservative",
                               "threshold": "myopic"}}, inplace=True)

    # Convert timestamps into seconds
    beginning_history = pd.Timestamp("1970-01-01", tz="UTC")
    df["ts_reply"] = (
                df["ts_reply"] - beginning_history).dt.total_seconds().values
    df["ts_display"] = (
                df["ts_display"] - beginning_history).dt.total_seconds().values

    # Rename columns
    df.rename(columns={f"pos_reply_{i}": f"option{i}" for i in range(6)},
              inplace=True)
    df.rename(columns={"teacher_md": "teacher",
                       "item_character": "character",
                       "item_meaning": "meaning"},
              inplace=True)

    for u in df.user.unique():
        is_u = df.user == u
        for t in df.loc[df.user == u, "teacher"].unique():
            is_t = df.teacher == t
            ut = is_u * is_t
            df.loc[ut, "session"] = pd.factorize(df.loc[ut, "session"])[0]

    # re-order columns
    df = df[['user', 'character', 'meaning', 'success',
             'ts_display', 'ts_reply',
             'option0', 'option1', 'option2', 'option3', 'option4', 'option5',
             'condition', 'teacher',
             'session', 'is_eval']]

    df.to_csv(output_path, index=False)

    return df, user_mail


def create_data_incl_preliminary_exp():

    path = "data/data_full.csv"
    output_path = "data_incl_preliminary_exp.csv"

    assert os.path.exists(path), \
        "The script 'get_data_full.py' should be called before"

    df = pd.read_csv(path, index_col=0,
                     dtype={"success": "boolean"},
                     parse_dates=['ts_display', 'ts_reply'])

    df.dropna(subset=["success"], inplace=True)

    # Sort by user and values
    df.sort_values(["user", "ts_display"], inplace=True)

    # Remove unnecessary columns
    df.drop(["domain", "item", "psy_md", "teacher_md", "condition", "is_eval",
             "learner_md", "session", "n_session_done"], axis=1, inplace=True)

    # Remove useless stuff
    df.user = [f"s{u}" for u in pd.factorize(df.user)[0]]

    # Convert timestamps into seconds
    beginning_history = pd.Timestamp("1970-01-01", tz="UTC")
    df["ts_reply"] = (
                df["ts_reply"] - beginning_history).dt.total_seconds().values
    df["ts_display"] = (
                df["ts_display"] - beginning_history).dt.total_seconds().values

    # Rename columns
    df.rename(columns={f"pos_reply_{i}": f"option{i}" for i in range(6)},
              inplace=True)
    df.rename(columns={"item_character": "character",
                       "item_meaning": "meaning"},
              inplace=True)

    # re-order columns
    df = df[['user', 'character', 'meaning', 'success',
             'ts_display', 'ts_reply',
             'option0', 'option1', 'option2', 'option3', 'option4', 'option5']]

    df.to_csv(output_path, index=False)


def main():

    df, user_mail = create_clean_data()
    create_demographic_data(df=df, user_mail=user_mail)
    create_data_incl_preliminary_exp()




