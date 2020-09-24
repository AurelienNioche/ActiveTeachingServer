#%%
""" Send an email upon account creation """
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
from django.utils import timezone

application = get_wsgi_application()

import os
import sys
from smtplib import SMTP_SSL

import numpy as np
import pandas as pd
from numpy.random import MT19937, RandomState, SeedSequence, default_rng

import ActiveTeachingServer.credentials as credentials
from experimental_condition.models.experiment import (RecursiveCondition,
                                                      ThresholdCondition)
from user.authentication import sign_up
from user.models.user import User

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

import datetime

from pytz import timezone

from experimental_condition.models.experiment import (RecursiveCondition,
                                                      ThresholdCondition)
from user.authentication import sign_up
from user.models.user import User


def get_credentials() -> dict:
    """Get email username and password"""

    return {
        "host": credentials.EMAIL_HOST_USER,
        "passwrd": credentials.EMAIL_HOST_PASSWORD,
    }


def make_email_addr(local_part: str, domain_name: str) -> str:
    """Make a email-like string"""

    return f"{local_part}@{domain_name}"


def make_pin(rng: np.random.Generator) -> np.ndarray:
    """Give a 4-digit PIN"""

    return str(rng.integers(0, 9999)).rjust(4, "0")


def load_animal_names(f_path):
    """Load the CSV with animals"""

    # Squeeze = load as pd.Series instead of pd.Dataframe
    return pd.read_csv(f_path, squeeze=True)


# def main_anonimize():
#
#     SEED = 123
#     # random state for in case you want shuffling
#     rs = RandomState(MT19937(SeedSequence(SEED)))
#     rng = default_rng(SEED)
#
#     animals_series = load_animal_names("./animals.csv")
#     # Next var is what you want to use
#     anon_emails = animals_series.apply(make_email_addr, domain_name="aalto.fi").sample(
#         frac=1, random_state=rs
#     )


SEED = 123
# random state for in case you want shuffling
rs = RandomState(MT19937(SeedSequence(SEED)))
rng = default_rng(SEED)

animals_series = load_animal_names("./animals.csv")
users_df = pd.read_csv("./subscriptions/20200924-active-teaching-data.csv", index_col=0)

anon_emails = animals_series.apply(make_email_addr, domain_name="aalto.fi").sample(
    frac=1, random_state=rs
)


#%%
users_df_ = users_df.copy()
row_list = []
for idx, user_data in users_df_.iterrows():
    user_data.loc["AnonName"] = make_email_addr(animals_series[idx], "aalto.fi")
    user_data.loc["PIN"] = make_pin(rng)
    row_list.append(user_data)

spam = pd.DataFrame(row_list)


# Manual user input
def input_error_message():
    """Input error message string"""

    return "Didn't get that"


def set_email():
    # Email management
    email = input("Email: ")
    if User.objects.filter(email=email).first():
        print("Warning! User already exists!")
        erase_user = input("Erase existing user (enter 'yes' or 'y' to continue)?")
        if erase_user:  # !!!!!!!!!!!!!! ALWAYS ERASES
            # User.objects.filter(email=email).first().delete()  # !!!!!!!!!!!!!
            print("Previous user erased")
            print(f"Email: {email}")
        else:
            print("Cannot create user with same email. Operation canceled")
            exit(0)
    return email


def set_condition():
    # Condition (select active teacher)
    while True:
        condition = input(
            "Condition ('0' for 'threshold', '1' for 'recursive', '2' for 'forward'): "
        )
        if condition not in ("0", "1", "2"):
            print(input_error_message())
        else:
            break

    condition = (
        RecursiveCondition.__name__ if int(condition) else ThresholdCondition.__name__
    )

    print(f"Condition selected: {condition}")
    return condition


def set_condition_begin():
    # Condition to start with (baseline, active)
    while True:
        begin_with_active = input(
            "Teacher first in session ('0' for 'leitner' and '1' for 'active'): "
        )
        if begin_with_active not in ("0", "1"):
            print(input_error_message())
        else:
            break

    begin_with_active = bool(int(begin_with_active))
    return begin_with_active


def set_gender():
    # Gender
    while True:
        gender = input("Gender (enter '0' for female, '1' for male, '2' for other):")
        if gender not in (str(User.MALE), str(User.FEMALE), str(User.OTHER)):
            print(input_error_message())
        else:
            break

    gender = int(gender)
    return gender


def set_password():
    # Password
    password = input("Password (nnnn): ")
    return password


def set_age():
    # Age
    while True:
        try:
            age = int(input("Age: "))
            break
        except Exception:
            print(input_error_message())

    return age


def set_mother_tongue():
    # Languages
    mother_tongue = input("mother tongue:")
    return mother_tongue


def set_other_language():
    other_language = input("other language(s) (please separate by ','):")
    return other_language


def set_first_session():
    # Date and time
    while True:
        try:

            first_session_string = input(
                "Helsinki time for the first session "
                "(enter using YYYY-MM-DD HH:MM format, "
                "ex: '2020-11-04 08:00'):"
            )

            first_session = datetime.datetime.fromisoformat(first_session_string)
            first_session = timezone("Europe/Helsinki").localize(first_session)
            first_session = first_session.astimezone(timezone("UTC"))
            break

        except Exception as e:
            print(f"Got exception '{e}', please try again!")
    return first_session


#%%
if "interactive" in sys.argv or "int" in sys.argv:
    interactive = True
    print("=== Running script in interactive mode ===")
else:
    interactive = False
while interactive:
    experiment_name = input("Experiment name: ")

    email = set_email()
    condition = set_condition()
    begin_with_active = set_condition_begin()
    gender = set_gender()
    age = set_age()
    mother_tongue = set_mother_tongue()
    other_language = set_other_language()
    first_session = set_first_session()

    # Confirm creation
    ready = input("create user (enter 'yes' or 'y' to continue)?")
    if ready not in ("y", "yes"):
        print("Operation cancelled")
        exit(0)

    user = sign_up(
        email=email,
        password=password,
        gender=gender,
        age=age,
        mother_tongue=mother_tongue,
        other_language=other_language,
        experiment_name=experiment_name,
        condition=condition,
        first_session=first_session,
        begin_with_active=begin_with_active,
    )

    if user is not None:
        print("Success!")
    else:
        raise ValueError("Something went wrong!")

    # if len(sys.argv) > 1:


#%%


def main_email():

    # Working to send plain text email
    # If you check internet to make the html version, filter results by date
    # My trials on things that didn't work farther below
    email_credentials = get_credentials()
    address_from = email_credentials["host"]
    address_to = ("carlos.1.delatorreortiz@aalto.fi",)
    alala = "fdsafdsafdsafdsadfasfdaf"
    text = f"""
    Dear {alala},

    Your account has been created!
    You can connect to:

    http://activeteaching.research.comnet.aalto.fi/

    id: XXXX@aalto.fi
    pwd: XXXX

    Your first session is on XXX, XXX at XXX.

    Training plan: 2 sessions per day, for 7 days.

    Don't hesitate to reach me if you have any questions or concerns!

    Good luck!

    Best,
    Aurelien


    --
    Aurelien Nioche, PhD

    Finnish Center for Artificial Intelligence (FCAI)
    Aalto University
    Department of Communications and Networking
    Computer Science Building - Office B235
    Konemiehentie 2
    02150 Espoo, Finland
    phone: (FI) +358 (0) 5 04 75 83 05, (FR) +33 (0) 6 86 55 02 55
    mail: nioche.aurelien@gmail.com
    """

    with SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(email_credentials["host"], email_credentials["passwrd"])
        # text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
        s.sendmail(address_from, address_to, text)


main_email()

#%%

if User.objects.filter(email="dog@aalto.fi").first():
    print("AAAAAAAAAAAAAG")
else:
    print("NNNNNNNNNNNNO")

#%%
# def _encapsulation():
#     """Don't call me, I'm just storage"""
#
#     new_account_data = {
#         "ExperimentName": input("Experiment name: "),
#         "Email": input("Email: "),
#         "StartDate": input("Start date (d.m.yyyy): "),
#         "SessionTime": input("Session time (H:mm): "),
#         "Gender": input("Gender (male/female/other): "),
#         "Age": input("Age: "),
#         "FirstLanguage": input("First language: "),
#         "OtherLanguages": input("Other languages (x,y,z): "),
#         "AnonEmail": input("Anonymous email (xyz@aalto.fi): "),
#         "Password": input("PIN (nnnn): "),
#     }
# Old type of creation
#     start_date = input("Start date (d.m.yyyy): ")
#     session_time = input("Session time (H:mm): ")
#     age = input("Age: ")
#     first_language = input("First language: ")
#     other_languages = input("Other languages (x,y,z): ")
#     anon_name = input("Anonymous email (xyz@aalto.fi): ")
#     print("*" * 40)
#     print("The following user will be added:")
#     new_account_data = dict()
#     print(pd.Series(new_account_data))
#
#     prompt_message = "Confirm adding user?"
#     confirmation = input(f"{prompt_message} [y/N]")
#     if (
#         confirmation == "y"
#         or confirmation == "Y"
#         or confirmation == "yes"
#         or confirmation == "Yes"
#     ):
#         # TODO call add_user
#         print("User created! TODO\n")
#         pass
#     elif confirmation == "n" or confirmation == "N" or confirmation == "":
#         print("User NOT added.")
#         pass
#     else:
#         correct_input = False
#         print(f"Didn't get that. {prompt_message} [y/N]: ")
#     expecting_output = True
#     while expecting_output == True:
#         prompt_message = "Add another user?"
#         another = input(f"{prompt_message} [y/N]: ")
#         if another == "y" or another == "Y" or another == "yes" or another == "Yes":
#             interactive = True
#             break
#         elif another == "n" or another == "N" or another == "":
#             interactive = False
#             break
#         else:
#             correct_input = False
#             print(f"Didn't get that. {prompt_message} [y/N]: ")

# Clean run
# if __name__ == "__main__":
#     main_anonimize()
#     main_email()

# ##### Block to do vertical additions
# def make_merge_idx(
#     len_animals: int, len_users: int, rng_gen: np.random.Generator, random: bool
# ) -> pd.Series:
#     """Asign a number (random or not) for later merge of anonymous name"""
#
#     if len_users > len_animals:
#         raise ValueError("There are more users than anon names (animals).")
#     if random:
#         array = rng_gen.integers(len_animals, size=len_users)
#     else:
#         array = np.arange(len_users)
#
#     return pd.Series(array, name="AnonNum")
#
#
# def subject_assign(
#     users_df: pd.DataFrame, to_assign: pd.Series, random=True
# ) -> pd.DataFrame:
#     """"""
#     pass
#
#
# idx_merge = make_merge_idx(len(animals_series), len(users_df), rng, random=True)
#
# users_df_ = pd.concat((users_df, idx_merge), axis=1)
# # Merge the corresponding animal to assigned idx
# rabbit = users_df_.merge(
#     animals_series, how="left", left_on="AnonNum", right_index=True
# )
# # Make the final email form
# rabbit["AnonName"] = (
#     rabbit["Animal"]
#     .apply(make_email_addr, domain_name="aalto.fi")
#     .sample(frac=1, random_state=rs)
# )
# # Drop the preprocessing columns
# rabbit.drop(columns=["Animal", "AnonNum"])
# ##### End block
# from email.headerregistry import Address
# from email.message import EmailMessage
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.utils import make_msgid
# #%%
# from smtplib import SMTP_SSL
#
# email_credentials = get_credentials()
# address_from = email_credentials["host"]
# address_to = ("carlos.1.delatorreortiz@aalto.fi",)
#
# msg = EmailMessage()
# msg["Subject"] = "hehehheehh emailo"
# msg["From"] = address_from
# msg["To"] = address_to
#
# # msg.set_content("""\
# # Salut!
# #
# # Cela ressemble à un excellent recipie[1] déjeuner.
# #
# # [1] http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718
# #
# # --Pepé
# # """)
#
# # Add the html version.  This converts the message into a multipart/alternative
# # container, with the original text message as the first part and the new html
# # message as the second part.
# msg.set_content(
#     """\
# <html>
#   <head></head>
#   <body>
#     <p>Salut!</p>
#     <p>Cela ressemble à un excellent
#         <a href="http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718">
#             recipie
#         </a> déjeuner.
#     </p>
#     <img src="cid:{asparagus_cid}" />
#   </body>
# </html>
# """
# )  # .format(subtype='html')
# # note that we needed to peel the <> off the msgid for use in the html.
#
# #%%
#
# #%%
# import smtplib
# from email.headerregistry import Address
# from email.message import EmailMessage
# from email.utils import make_msgid
#
# email_credentials = get_credentials()
# address_from = email_credentials["host"]
# address_to = ("carlos.1.delatorreortiz@aalto.fi",)
#
# msg = EmailMessage()
# msg["Subject"] = "hehehheehh emailo"
# msg["From"] = address_from
# msg["To"] = address_to
#
# # Create the base text message.
# msg.set_content(
#     """\
# Salut!
#
# Cela ressemble à un excellent recipie[1] déjeuner.
#
# [1] http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718
#
# --Pepé
# """
# )
#
# # Add the html version.  This converts the message into a multipart/alternative
# # container, with the original text message as the first part and the new html
# # message as the second part.
# msg.add_alternative(
#     """\
# <html>
#   <head></head>
#   <body>
#     <p>Salut!</p>
#     <p>Cela ressemble à un excellent
#         <a href="http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718">
#             recipie
#         </a> déjeuner.
#     </p>
#   </body>
# </html>
# """
# )  # .format(asparagus_cid=asparagus_cid[1:-1]), subtype='html')
# # note that we needed to peel the <> off the msgid for use in the html.
#
#
# # Send the message via local SMTP server.
# with SMTP_SSL("smtp.gmail.com", 465) as s:
#     s.send_message(msg)
#
# #%%
# def manage_smtp_session() -> None:
#     email_credentials = get_credentials()
#     session = SMTP_SSL("smtp.gmail.com", 587)
#
#     # session.starttls()  # TLS for security needed??
#     session.login(email_credentials["host"], email_credentials["passwrd"])
#     return
#     message = "Helo participanterino XYZ"
#
#     session.sendmail("sender_email_id", "receiver_email_id", message)
#
#     session.quit()
#     pass
#
#
# manage_smtp_session()
# #%%
#
# subjects_df = pd.read_csv("subjects.csv", index_col=0)
# anon_names = subjects_df["AnonName"]
# for idx, anon_name in anon_names.iteritems():
#     pass
