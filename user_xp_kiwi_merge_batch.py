import os
import pandas as pd

from user_xp_kiwi_create import CSV, save_csv

NEW_BATCH = os.path.join("subscriptions", "BatchF.csv")


def main():

    # import
    users_df = pd.read_csv(CSV, index_col=0)

    try:
        new_user_df = pd.read_csv(NEW_BATCH, index_col=0, sep=",")
        assert "Email" in new_user_df.columns
    except AssertionError:
        new_user_df = pd.read_csv(NEW_BATCH, index_col=0, sep=";")

    # print original
    print("original\n", users_df)

    # remove empty rows
    new_user_df.dropna(axis=0, subset=['Email'], inplace=True)

    # Make sure index is int
    new_user_df.index = new_user_df.index.map(int)

    # Concat
    users_df = pd.concat([users_df, new_user_df], axis=0,
                          verify_integrity=True)
    # save
    save_csv(users_df)

    # display
    print("new\n", users_df)


if __name__ == "__main__":
    main()
