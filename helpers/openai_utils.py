import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain


def get_quiz_data(text, openai_api_key, count, difficulty):
    template = f"""
    You are a helpful assistant programmed to generate questions based on any text provided. For every chunk of text you receive, you're tasked with designing {count} distinct questions. Each of these questions will be accompanied by 4 possible answers: one correct answer and three incorrect ones. 

    For clarity and ease of processing, structure your response in a way that emulates a Python list of lists. 

    Your output should be shaped as follows:

    1. An outer list that contains {count} inner lists.
    2. Each inner list represents a set of question and answers, and contains exactly 5 strings in this order:
    - The generated question.
    - The correct answer.
    - The first incorrect answer.
    - The second incorrect answer.
    - The third incorrect answer.

    Your output should mirror this structure:
    [
        ["Generated Question 1", "Correct Answer 1", "Incorrect Answer 1.1", "Incorrect Answer 1.2", "Incorrect Answer 1.3"],
        ["Generated Question 2", "Correct Answer 2", "Incorrect Answer 2.1", "Incorrect Answer 2.2", "Incorrect Answer 2.3"],
        ...
    ]

    It is crucial that you adhere to this format as it's optimized for further Python processing.

    Also the difficulty level of the questions should be {difficulty} / 5. If 1 being very easy and 5 being extreme difficult, generate questions with difficulty level {difficulty}. 
    """
    try:
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )
        chain = LLMChain(
            llm=ChatOpenAI(openai_api_key=openai_api_key,model="gpt-4-1106-preview"),
            prompt=chat_prompt,
        )
        return chain.run(text)
    except Exception as e:
        if "AuthenticationError" in str(e):
            st.error("Incorrect API key provided. Please check and update your API key.")
            st.stop()
        else:
            st.error(f"An error occurred: {str(e)}")
            st.stop()

def get_true_false(text, openai_api_key, count, difficulty):
    template = f"""
    You are a helpful assistant programmed to generate True/False questions based on any text provided. For every chunk of text you receive, you're tasked with designing {count} distinct questions. Each of these questions will be accompanied by 2 possible answers: True and False. 

    For clarity and ease of processing, structure your response in a way that emulates a Python list of lists. 

    Your output should be shaped as follows:

    1. An outer list that contains {count} inner lists.
    2. Each inner list represents a set of question and answers, and contains exactly 3 strings in this order:
    - The generated True/False question.
    - The correct option.
    - The wrong option.

    Your output should mirror this structure:
    [
        ["Generated Question 1", "Correct option", "Incorrect option"],
        ["Generated Question 2", "Correct option", "Incorrect option"],
        ...
    ]

    It is crucial that you adhere to this format as it's optimized for further Python processing.

    The difficulty level of the questions should be {difficulty}. 
    """
    try:
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )
        chain = LLMChain(
            llm=ChatOpenAI(openai_api_key=openai_api_key,model="gpt-4-1106-preview"),
            prompt=chat_prompt,
        )
        return chain.run(text)
    except Exception as e:
        if "AuthenticationError" in str(e):
            st.error("Incorrect API key provided. Please check and update your API key.")
            st.stop()
        else:
            st.error(f"An error occurred: {str(e)}")
            st.stop()
