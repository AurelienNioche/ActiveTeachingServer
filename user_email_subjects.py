#%%
""" Send an email upon account creation """
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
from django.utils import timezone

application = get_wsgi_application()

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
users_df = pd.read_csv("./fake_users.csv", index_col=0)

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


#%%
if "interactive" in sys.argv or "int" in sys.argv:
    interactive = True
    print("=== Running script in interactive mode ===")
else:
    interactive = False
while interactive:
    new_account_data = {
        "ExperimentName": input("Experiment name: "),
        "Email": input("Email: "),
        "StartDate": input("Start date (d.m.yyyy): "),
        "SessionTime": input("Session time (H:mm): "),
        "Gender": input("Gender (male/female/other): "),
        "Age": input("Age: "),
        "FirstLanguage": input("First language: "),
        "OtherLanguages": input("Other languages (x,y,z): "),
        "AnonEmail": input("Anonymous email (xyz@aalto.fi): "),
        "Password": input("PIN (nnnn): "),
    }
    print("*" * 40)
    print("The following user will be added:")
    print(pd.Series(new_account_data))
    prompt_message = "Confirm adding user?"
    confirmation = input(f"{prompt_message} [y/N]")
    if (
        confirmation == "y"
        or confirmation == "Y"
        or confirmation == "yes"
        or confirmation == "Yes"
    ):
        # TODO call add_user
        print("User created! TODO\n")
        pass
    elif confirmation == "n" or confirmation == "N" or confirmation == "":
        print("User NOT added.")
        pass
    else:
        correct_input = False
        print(f"Didn't get that. {prompt_message} [y/N]: ")
    expecting_output = True
    while expecting_output == True:
        prompt_message = "Add another user?"
        another = input(f"{prompt_message} [y/N]: ")
        if another == "y" or another == "Y" or another == "yes" or another == "Yes":
            interactive = True
            break
        elif another == "n" or another == "N" or another == "":
            interactive = False
            break
        else:
            correct_input = False
            print(f"Didn't get that. {prompt_message} [y/N]: ")

# if len(sys.argv) > 1:


#%%


def main_email():

    # Working to send plain text email
    # If you check internet to make the html version, filter results by date
    # My trials on things that didn't work farther below
    email_credentials = get_credentials()
    address_from = email_credentials["host"]
    address_to = ("carlos.1.delatorreortiz@aalto.fi",)
    with SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(email_credentials["host"], email_credentials["passwrd"])
        text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
        s.sendmail(address_from, address_to, text)


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
