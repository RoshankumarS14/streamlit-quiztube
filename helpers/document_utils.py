import streamlit as st
import PyPDF2
from docx import Document
import dropbox
from helpers.quiz_utils import string_to_list

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
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                content += page.extract_text()
        elif "word" in content_type:
            doc = Document(uploaded_file)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            content = '\n'.join(full_text)
        return content

def replace_with_list_of_lists(dropbox_path, new_data, token):
    dbx = dropbox.Dropbox(token)

    # Convert the new list of lists to text format
    text_content = str(new_data)

    # Upload the new content to replace the existing file
    dbx.files_upload(text_content.encode(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)

def read_list_of_lists(dropbox_path, token):
    dbx = dropbox.Dropbox(token)

    try:
        # Download the file from Dropbox
        _, file_content = dbx.files_download(dropbox_path)
        content = file_content.content.decode()

        # Split the content into lines and convert to a list of lists
        list_of_lists = string_to_list(content)
        
        return list_of_lists
    except dropbox.exceptions.ApiError as e:
        print(f"Error reading file: {e}")
        return None

def add_quiz_log(new_log, token):

    dropbox_path = "/Log.txt"
    dbx = dropbox.Dropbox(token)
    
    _, existing_log = dbx.files_download(dropbox_path)
    current_log = existing_log.content.decode('utf-8')
    updated_log = current_log + '\n' + new_log

    # Upload the new content to append to the existing file
    dbx.files_upload(updated_log.encode('utf-8'), dropbox_path, mode=dropbox.files.WriteMode.overwrite)

def get_quiz_log(token):

    dbx = dropbox.Dropbox(token)

    try:
        # Download the file from Dropbox
        _, file_content = dbx.files_download("/Log.txt")
        logs = file_content.content.decode()
        
        return logs

    except dropbox.exceptions.ApiError as e:
        print(f"Error reading file: {e}")
        return None
