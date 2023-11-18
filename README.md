# 🧠 QuizTube: Transforming YouTube Videos into Quizzes with Streamlit

QuizGPT offers an innovative approach to create interactive quizzes from Ebooks. By processing the text with OpenAI's LLM, `QuizTube` serves as a powerful tool for enhancing document content interaction.

## Video Tutorial
[![YouTube Video](https://img.youtube.com/vi/xCsAbe5MVLc/0.jpg)](https://youtu.be/xCsAbe5MVLc)

## Website Link
👉 Check out the app here: https://quizgpt.streamlit.app/

## How It Works

1. **Content Extraction:** Using a document reader, texts are extracted from a uploaded pdf / word file.
2. **Quiz Generation:** The extracted captions are then fed into OpenAI's LLM using [`LangChain Python`](https://python.langchain.com/) with a predefined prompt template. The model generates questions based on the content, turning the video's key points into an interactive quiz.
3. **Streamlit Integration:** The quizzes are seamlessly integrated and displayed in a Streamlit app, providing users with a unique and interactive experience.

