import streamlit as st
from helpers.openai_utils import get_quiz_data, get_true_false
from helpers.quiz_utils import string_to_list, get_randomized_options
from helpers.toast_messages import get_random_toast
from docx import Document
import PyPDF2
import math
import random
import pickle
from pathlib import Path
import streamlit_authenticator as stauth

st.set_page_config(
    page_title="Quiz GPT",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

#----USER AUTHENTICATION-------

names = ["Job Driver Careers"]
usernames = ["sales@thejobsdriver.careers"]

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate({"usernames":{usernames[0]:{"name":names[0],"password":hashed_passwords[0]}}},cookie_name="Quiz",key="abcdef",cookie_expiry_days=0)

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


    st.title(":red[QuizGPT] — Read. Learn. Quiz. 🧠", anchor=False)
    st.write("""
    Ever read a Ebook and wondered how well you understood its content? Here's a fun twist: Instead of just reading on book, come to **Quiz GPT** and test your comprehension!

    **How does it work?** 🤔
    1. Upload your Ebook as pdf file.
    2. Enter your [OpenAI API Key](https://platform.openai.com/account/api-keys).

    ⚠️ Important: The pdf **must** have content in english for the tool to work.

    Once you've input the details, voilà! Dive deep into questions crafted just for you, ensuring you've truly grasped the content of the video. Let's put your knowledge to the test! 
    """)

    # with st.expander("💡 Video Tutorial"):
    #     with st.spinner("Loading video.."):
    #         st.video("https://youtu.be/yzBr3L2BIto", format="video/mp4", start_time=0)

    def read_pdf_content(uploaded_file):
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        num_pages = len(pdf_reader.pages)

        text_content = ''
        for page_num in range(5):
            page = pdf_reader.pages[page_num]
            text_content += page.extract_text()

        return text_content

    def read_file_content(uploaded_file):
        content = ""
        if uploaded_file is not None:
            content_type = uploaded_file.type
            if "pdf" in content_type:
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                num_pages = len(pdf_reader.pages)
                for page_num in range(5):
                    page = pdf_reader.pages[page_num]
                    content += page.extract_text()
            elif "word" in content_type:
                doc = Document(uploaded_file)
                full_text = []
                for para in doc.paragraphs:
                    full_text.append(para.text)
                content = '\n'.join(full_text)
        return content

    with st.form("user_input"):
        pdf_file = st.file_uploader("Upload your pdf file", type=["pdf", "docx"])
        count = st.text_input("Enter the number of questions you want to generate:")
        difficulty = st.radio("Select Difficulty level:",["Very Easy","Easy","Moderate","Hard","Extreme Hard"])
        OPENAI_API_KEY = st.text_input("Enter your OpenAI API Key:", placeholder="sk-XXXX", type='password')
        submitted = st.form_submit_button("Craft my quiz!")

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
                st.session_state.quiz_data_list = quiz_questions[:int(count)]  

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

            with st.form(key='quiz_form'):
                st.subheader("🧠 Quiz Time: Test Your Knowledge!", anchor=False)
                for i, q in enumerate(st.session_state.quiz_data_list):
                    options = st.session_state.randomized_options[i]
                    default_index = st.session_state.user_answers[i] if st.session_state.user_answers[i] is not None else 0
                    response = st.radio(q[0], options, index=default_index, key="QA"+str(i))
                    user_choice_index = options.index(response)
                    st.session_state.user_answers[i] = user_choice_index  # Update the stored answer right after fetching it


                results_submitted = st.form_submit_button(label='Unveil My Score!')

                if results_submitted:
                    score = sum([ua == st.session_state.randomized_options[i].index(ca) for i, (ua, ca) in enumerate(zip(st.session_state.user_answers, st.session_state.correct_answers))])
                    st.success(f"Your score: {score}/{len(st.session_state.quiz_data_list)}")

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