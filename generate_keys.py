import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["Admin","Job Driver Careers"]
usernames = ["admin@thejobsdriver.careers","sales@thejobsdriver.careers"]
passwords = ["Admin@24","make$ome$ales-24"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent/ "hashed_pw.pkl"

with file_path.open("wb") as file:
    pickle.dump(hashed_passwords,file)