#%%
""" Send an email upon account creation """

from smtplib import SMTP_SSL

import numpy as np
import pandas as pd
from numpy.random import MT19937, RandomState, SeedSequence, default_rng

import credentials


def get_credentials() -> dict:
    """Get email username and password"""

    return {
        "host": credentials.EMAIL_HOST_USER,
        "passwrd": credentials.EMAIL_HOST_PASSWORD,
    }


def make_email_addr(local_part: str, domain_name: str) -> str:
    """Make a email-like string"""

    return f"{local_part}@{domain_name}"


def make_pin(rng: object) -> np.ndarray:
    """Give a 4-digit PIN"""

    return str(rng.integers(0, 9999)).rjust(4, "0")


def load_animal_names(f_path):
    """Load the CSV with animals"""

    # Squeeze = load as pd.Series instead of pd.Dataframe
    return pd.read_csv(f_path, squeeze=True)


def main_anonimize():

    SEED = 123
    # random state for in case you want shuffling
    rs = RandomState(MT19937(SeedSequence(SEED)))
    rng = default_rng(SEED)

    animals_series = load_animal_names("./animals.csv")
    # Next var is what you want to use
    anon_emails = animals_series.apply(make_email_addr, domain_name="aalto.fi").sample(
        frac=1, random_state=rs
    )


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


if __name__ == "__main__":
    main_anonimize()
    main_email()

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
