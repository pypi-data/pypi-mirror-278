import requests
from bs4 import BeautifulSoup
import json
import sys
import logging
import os
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CONFIG_FILE = 'config.txt'

def fetch_conversation_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.info("Successfully fetched data from URL.")
    except requests.RequestException as e:
        logging.error(f"Error fetching data from URL: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.content, 'html.parser')
    script_tag = soup.find('script', id='__NEXT_DATA__')
    if not script_tag:
        logging.error("No conversation data found at the URL.")
        sys.exit(1)

    data_json = script_tag.string
    data = json.loads(data_json)
    conversation = []

    for message_id, message_data in data['props']['pageProps']['serverResponse']['data']['mapping'].items():
        if 'message' not in message_data:
            continue
        message = message_data['message']
        author_role = message['author']['role']
        if author_role.lower() == 'system':
            continue
        content_type = message['content'].get('content_type', 'text')
        if author_role.lower() == 'user':
            content = " ".join(part if isinstance(part, str) else part.get('text', '') for part in message['content']['parts'])
            conversation.append(("user", content))
        elif author_role.lower() == 'assistant':
            if content_type == 'text':
                content = " ".join(part if isinstance(part, str) else part.get('text', '') for part in message['content']['parts'])
            elif content_type == 'code':
                content = f"```python\n{message['content'].get('text', '')}\n```"
            elif content_type == 'image':
                content = "[Image content not displayable]"
            else:
                continue
            conversation.append(("assistant", content))
    logging.info("Successfully parsed conversation data.")
    return conversation[::-1]

def create_gpt_colab_notebook(conversations, output_filename, documents):
    cells = []
    num_queries = sum(1 for role, _ in conversations if role == 'user')
    title = "MULTI-TURN" if num_queries > 1 else "SINGLE-TURN"
    cells.append({"cell_type": "markdown", "metadata": {}, "source": [f"{title}\n"]})
    turn_number = 0
    for role, content in conversations:
        if role == 'user':
            turn_number += 1
            query_header = f"Turn {turn_number}\n\nQuery {turn_number}:\n{content}\n\n"
            for idx, link in enumerate(documents, start=1):
                query_header += f"Data {idx}: {link}\n" if len(documents) > 1 else f"Data: {link}\n"
            cells.append({"cell_type": "markdown", "metadata": {}, "source": [query_header]})
        elif role == 'assistant':
            if content.startswith('```python'):
                cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": [content.replace('```python\n', '').replace('\n```', '')]})
            else:
                cells.append({"cell_type": "markdown", "metadata": {}, "source": [content + "\n"]})
    notebook_content = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.8.5", "mimetype": "text/x-python", "codemirror_mode": {"name": "ipython", "version": 3}, "pygments_lexer": "ipython3", "nbconvert_exporter": "python", "file_extension": ".py"}
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            json.dump(notebook_content, file, ensure_ascii=False, indent=2)
        logging.info(f"Notebook '{output_filename}' has been created successfully.")
    except IOError as e:
        logging.error(f"Error writing notebook file: {e}")
        sys.exit(1)

def get_persisted_raters_id():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as file:
                raters_id = file.readline().strip()
                if raters_id:
                    return raters_id
                else:
                    logging.warning("Rater's ID not found in config file.")
                    return None
        except IOError as e:
            logging.error(f"Error reading config file: {e}")
            return None
    else:
        return None

def save_raters_id(raters_id):
    try:
        with open(CONFIG_FILE, 'w') as file:
            file.write(raters_id)
        logging.info("Rater's ID saved to config file.")
    except IOError as e:
        logging.error(f"Error saving rater's ID: {e}")

def is_valid_conversation_url(url):
    regex = re.compile(r'^https://chatgpt\.com/share/[0-9a-fA-F-]{36}$')
    return re.match(regex, url) is not None

def is_valid_document_url(url):
    return url.startswith('https://')

def get_input(prompt):
    user_input = input(prompt).strip()
    if user_input.lower() == 'exit':
        logging.info("Process exited by user.")
        raise SystemExit(0)
    return user_input

def process_gpt_conversation():
    try:
        while True:
            conversation_url = get_input("Enter the conversation URL (or type 'exit' to quit): ")
            if is_valid_conversation_url(conversation_url):
                break
            else:
                logging.error("Invalid URL. Please enter a valid URL in the format 'https://chatgpt.com/share/{UUID}'.")

        raters_id = get_persisted_raters_id()
        if raters_id:
            use_stored_id = get_input(f"Continue with stored rater's ID '{raters_id}'? (yes/no or type 'exit' to quit): ").strip().lower()
            if use_stored_id == 'no':
                while True:
                    raters_id = get_input("Enter the new rater's ID (numbers only or type 'exit' to quit): ").strip()
                    if raters_id.isdigit():
                        save_raters_id(raters_id)
                        break
                    else:
                        logging.error("Invalid rater's ID. Please enter numbers only.")
        else:
            while True:
                raters_id = get_input("Enter the rater's ID (numbers only or type 'exit' to quit): ").strip()
                if raters_id.isdigit():
                    save_raters_id(raters_id)
                    break
                else:
                    logging.error("Invalid rater's ID. Please enter numbers only.")

        while True:
            row_id = get_input("Enter the row ID (numbers only or type 'exit' to quit): ").strip()
            if row_id.isdigit():
                break
            else:
                logging.error("Invalid row ID. Please enter numbers only.")

        while True:
            try:
                num_documents = int(get_input("Enter the number of documents used (or type 'exit' to quit): "))
                if num_documents > 0:
                    break
                else:
                    logging.error("Number of documents must be a positive integer.")
            except ValueError:
                logging.error("Invalid input. Please enter a positive integer.")

        documents = []
        for i in range(num_documents):
            while True:
                document_link = get_input(f"Enter link for Document {i+1} (must start with 'https://' or type 'exit' to quit): ").strip()
                if is_valid_document_url(document_link):
                    documents.append(document_link)
                    break
                else:
                    logging.error("Invalid document link. Please enter a valid URL starting with 'https://'.")

        output_file = f"GPT_rater_{raters_id}_ID_{row_id}.ipynb"
        logging.info("Fetching conversation data...")
        conversation_data = fetch_conversation_data(conversation_url)

        logging.info("Creating Google Colab notebook...")
        create_gpt_colab_notebook(conversation_data, output_file, documents)

    except SystemExit:
        print("You have exited the process. You can start again later if you wish.")