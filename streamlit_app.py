import streamlit as st
from helpers.youtube_utils import extract_video_id_from_url, get_transcript_text
from helpers.openai_utils import get_quiz_data
from helpers.quiz_utils import string_to_list, get_randomized_options
from helpers.toast_messages import get_random_toast
import PyPDF2


st.set_page_config(
    page_title="Quiz GPT",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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

with st.form("user_input"):
    pdf_file = st.file_uploader("Upload your pdf file", type="pdf")
    count = st.text_input("Enter the number of questions you want to generate:")
    OPENAI_API_KEY = st.text_input("Enter your OpenAI API Key:", placeholder="sk-XXXX", type='password')
    submitted = st.form_submit_button("Craft my quiz!")

if submitted or ('quiz_data_list' in st.session_state):
    if not pdf_file:
        st.info("Please provide a valid pdf file.")
        st.stop()
    elif not OPENAI_API_KEY:
        st.info("Please fill out the OpenAI API Key to proceed. If you don't have one, you can obtain it [here](https://platform.openai.com/account/api-keys).")
        st.stop()
        
    with st.spinner("Crafting your quiz...🤓"):
        if submitted:
            pdf_content = read_pdf_content(pdf_file)
            quiz_data_str = get_quiz_data(pdf_content, OPENAI_API_KEY, count)
            st.session_state.quiz_data_list = string_to_list(quiz_data_str)

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
                response = st.radio(q[0], options, index=default_index)
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