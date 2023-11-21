import streamlit as st
from helpers.openai_utils import get_quiz_data, get_true_false
from helpers.quiz_utils import string_to_list, get_randomized_options
from helpers.toast_messages import get_random_toast
from helpers.document_utils import read_file_content, replace_with_list_of_lists, read_list_of_lists, get_quiz_log, add_quiz_log
import random
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
from dotenv import dotenv_values
import pandas as pd
from dotenv import load_dotenv
import os

st.set_page_config(
    page_title="Quiz GPT",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# load .env file
load_dotenv()

#----USER AUTHENTICATION-------

names = ["Admin","Job Driver Careers"]
usernames = ["admin@thejobsdriver.careers","sales@thejobsdriver.careers"]

# Github data

# Your GitHub Personal Access Token
token = "sl.BqTcPLeFQYTyaxrC5V4dhpLNx9xuWqcIxND-jPX0SqjiXLwXyMXevvtQ-daiIsTnDXkJqtKz5VYXiflE8jxZdiyVdJS5B6ZrtMSSpzmDNIJVjjf4yY5MVDi7qDIV47JhbYTGGRivAXwx"

# Path to the file in the repository
file_path = '/Questions.txt'  

file_path_passwords = Path(__file__).parent / "hashed_pw.pkl"
with file_path_passwords.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate({"usernames":{usernames[0]:{"name":names[0],"password":hashed_passwords[0]},usernames[1]:{"name":names[1],"password":hashed_passwords[1]}}},cookie_name="Quiz",key="abcdef",cookie_expiry_days=0)

name, authentication_status, username = authenticator.login("Login","main")

if authentication_status == False:
    st.error("Username/Password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:

    # Check if user is new or returning using session state.
    # If user is new, show the toast message.
    if 'first_time' not in st.session_state:
        message, icon = get_random_toast()
        st.toast(message, icon=icon)
        st.session_state.first_time = False
    
    if username=="admin@thejobsdriver.careers":
        
        # Welcome message to admin
        st.title("Welcome Admin",anchor=False)
        st.text(token)
        
        # Generate quiz
        with st.form("user_input"):
            pdf_file = st.file_uploader("Upload your pdf file", type=["pdf", "docx"])
            count = st.text_input("Enter the number of questions you want to generate:")
            difficulty = st.radio("Select Difficulty level:",["Very Easy","Easy","Moderate","Hard","Extreme Hard"])
            OPENAI_API_KEY = st.text_input("Enter your OpenAI API Key:", placeholder="sk-XXXX", type='password')
            submitted = st.form_submit_button("Craft my quiz!")

        st.subheader("Quiz Log",anchor=False)

        logs = get_quiz_log(token)

        scores = logs.split('\n')
        quiz_log = [score.split(':') for score in scores[1:]]

        # Create a DataFrame
        df = pd.DataFrame(quiz_log, columns=['Name', 'Score'])
        
        st.markdown(f'<div style="background-color:#002b36;border-radius:5px;padding:10px;margin-bottom:20px;">{df.to_html(classes="table table-striped table-hover text-center text-nowrap", justify="center")}</div>', unsafe_allow_html=True)

        if submitted or ('quiz_data_list' in st.session_state):
            if not pdf_file:
                st.info("Please provide a valid pdf file or a word file.")
                st.stop()
            elif not OPENAI_API_KEY:
                st.info("Please fill out the OpenAI API Key to proceed. If you don't have one, you can obtain it [here](https://platform.openai.com/account/api-keys).")
                st.stop()
                
            with st.spinner("Crafting your quiz...🤓"):
                if submitted:
                    pdf_content = read_file_content(pdf_file)
                    quiz_data_str = get_quiz_data(pdf_content, OPENAI_API_KEY, count, difficulty)
                    quit_data_tf = get_true_false(pdf_content, OPENAI_API_KEY, int(int(count)/2), difficulty)
                    # quiz_data_tf = get_true_false(pdf_content, OPENAI_API_KEY, math.floor(int(count)*0.2), difficulty)
                    # quiz_questions = string_to_list(quiz_data_str)[:math.ceil(int(count)*0.8)]
                    # +string_to_list(quiz_data_tf)[:math.floor(int(count)*0.2)]
                    # random.shuffle(quiz_questions)
                    quiz_questions = string_to_list(quiz_data_str)+string_to_list(quit_data_tf)
                    random.shuffle(quiz_questions)

                    # ---Store Quiz Questions in Github-----
                    replace_with_list_of_lists(file_path, quiz_questions, token)
                    st.info("Questions generated successfully!")
                    st.subheader("Generated Quiz!", anchor=False)
                    randomized_options = []
                    for q in quiz_questions:
                        options, correct_answer = get_randomized_options(q[1:])
                        randomized_options.append(options)
                    for i, q in enumerate(quiz_questions):
                        options = randomized_options[i]
                        response = st.radio(q[0], options, index=0, key="QA"+str(i))

                

    else:

        st.title(":red[QuizGPT] — Read. Learn. Quiz. 🧠", anchor=False)
    # st.write("""
    # Ever read a Ebook and wondered how well you understood its content? Here's a fun twist: Instead of just reading on book, come to **Quiz GPT** and test your comprehension!

    # **How does it work?** 🤔
    # 1. Upload your Ebook as pdf file.
    # 2. Enter your [OpenAI API Key](https://platform.openai.com/account/api-keys).

    # ⚠️ Important: The pdf **must** have content in english for the tool to work.

    # Once you've input the details, voilà! Dive deep into questions crafted just for you, ensuring you've truly grasped the content of the video. Let's put your knowledge to the test! 
    # """)

    # with st.expander("💡 Video Tutorial"):
    #     with st.spinner("Loading video.."):
    #         st.video("https://youtu.be/yzBr3L2BIto", format="video/mp4", start_time=0)

        # ---Get Questions from Github----

        result = read_list_of_lists(file_path, token)

        st.session_state.quiz_data_list = result  

        if 'user_answers' not in st.session_state:
            st.session_state.user_answers = [None for _ in st.session_state.quiz_data_list]
        if 'correct_answers' not in st.session_state:
            st.session_state.correct_answers = []
        if 'randomized_options' not in st.session_state:
            st.session_state.randomized_options = []

        for q in st.session_state.quiz_data_list:
            options, correct_answer = get_randomized_options(q[1:])
            st.session_state.randomized_options.append(options)
            st.session_state.correct_answers.append(correct_answer)

        full_name = st.text_input("Enter your name:",placeholder="Full Name") 

        with st.form(key='quiz_form'):
                st.subheader("🧠 Quiz Time: Test Your Knowledge!", anchor=False)
                for i, q in enumerate(st.session_state.quiz_data_list):
                    options = st.session_state.randomized_options[i]
                    default_index = st.session_state.user_answers[i] if st.session_state.user_answers[i] is not None else 0
                    response = st.radio(q[0], options, index=default_index, key="QA"+str(i))
                    user_choice_index = options.index(response)
                    st.session_state.user_answers[i] = user_choice_index  
                    
                # Update the stored answer right after fetching iit

                results_submitted = st.form_submit_button(label='Unveil My Score!')

                if results_submitted:
                    score = sum([ua == st.session_state.randomized_options[i].index(ca) for i, (ua, ca) in enumerate(zip(st.session_state.user_answers, st.session_state.correct_answers))])
                    st.success(f"Your score: {score}/{len(st.session_state.quiz_data_list)}")

                    add_quiz_log(full_name+":"+str(score)+"/"+str(len(st.session_state.quiz_data_list)),token)

                    if score == len(st.session_state.quiz_data_list):  # Check if all answers are correct
                        st.balloons()
                    else:
                        incorrect_count = len(st.session_state.quiz_data_list) - score
                        if incorrect_count == 1:
                            st.warning(f"Almost perfect! You got 1 question wrong. Let's review it:")
                        else:
                            st.warning(f"Almost there! You got {incorrect_count} questions wrong. Let's review them:")

                    for i, (ua, ca, q, ro) in enumerate(zip(st.session_state.user_answers, st.session_state.correct_answers, st.session_state.quiz_data_list, st.session_state.randomized_options)):
                        with st.expander(f"Question {i + 1}", expanded=False):
                            if ro[ua] != ca:
                                st.info(f"Question: {q[0]}")
                                st.error(f"Your answer: {ro[ua]}")
                                st.success(f"Correct answer: {ca}")
    authenticator.logout("Logout","main")
