import re
import json
import logging
import sys
import os
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CONFIG_FILE = 'config.txt'

def process_contents_to_ipynb(input_strings, queries, output_filename, documents):
    cells = []
    title = "MULTI-TURN" if len(input_strings) > 1 else "SINGLE-TURN"
    cells.append({"cell_type": "markdown", "metadata": {}, "source": [title + '\n']})

    for idx, (input_string, query) in enumerate(zip(input_strings, queries)):
        turn_number = idx + 1
        turn_markdown = f"Turn {turn_number}\n\nQuery {turn_number}: {query}\n\n"
        query_data_markdown = ""
        for i, link in enumerate(documents):
            query_data_markdown += f"Data {i+1}: {link}\n" if len(documents) > 1 else f"Data: {link}\n"

        cells.append({"cell_type": "markdown", "metadata": {}, "source": [turn_markdown + query_data_markdown]})

        cleaned_content = re.sub(r'```text\?code_stdout.*?\n.*?\n```', '', input_string, flags=re.DOTALL)
        cleaned_content = re.sub(r'```text\?code_stderr.*?\n.*?\n```', '', cleaned_content, flags=re.DOTALL)
        code_blocks = re.findall(r'```python\?code.*?\n(.*?)\n```', cleaned_content, flags=re.DOTALL)
        cleaned_content = re.sub(r'```python\?code.*?\n', 'CODE_BLOCK_START\n', cleaned_content)
        cleaned_content = re.sub(r'\n```', '\nCODE_BLOCK_END', cleaned_content)
        split_content = cleaned_content.split('\n')
        code_block_index = 0
        inside_code_block = False
        markdown_content = ""
        for line in split_content:
            if line == "CODE_BLOCK_START":
                if markdown_content.strip():
                    cells.append({
                        "cell_type": "markdown",
                        "metadata": {},
                        "source": [line + '\n' for line in markdown_content.strip().split('\n')]
                    })
                    markdown_content = ""
                inside_code_block = True
                code_content = ""
            elif line == "CODE_BLOCK_END":
                inside_code_block = False
                if code_block_index < len(code_blocks):
                    code_content = code_blocks[code_block_index]
                    cells.append({
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {},
                        "outputs": [],
                        "source": [line + '\n' for line in code_content.strip().split('\n')]
                    })
                    code_block_index += 1
            else:
                if inside_code_block:
                    code_content += line + "\n"
                else:
                    markdown_content += line + "\n"

        if markdown_content.strip():
            cells.append({
                "cell_type": "markdown",
                "metadata": {},
                "source": [line + '\n' for line in markdown_content.strip().split('\n')]
            })

    notebook_content = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.8.5",
                "mimetype": "text/x-python",
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "pygments_lexer": "ipython3",
                "nbconvert_exporter": "python",
                "file_extension": ".py"
            }
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

def count_code_errors(input_strings):
    error_types = [
        'AttributeError', 'ValueError', 'ModuleNotFoundError',
        'FileNotFoundError', 'KeyError', 'TypeError',
        'NameError', 'SyntaxError'
    ]

    total_error_counts = {error: 0 for error in error_types}
    turn_error_counts = []

    for idx, input_string in enumerate(input_strings):
        error_counts = {error: 0 for error in error_types}
        tracebacks = re.findall(r'Traceback \(most recent call last\):.*?(?=\n\n|\Z)', input_string, re.DOTALL)

        for traceback in tracebacks:
            for error in error_types:
                if f"{error}:" in traceback:
                    error_counts[error] += 1
                    total_error_counts[error] += 1

        turn_error_counts.append((f"Turn {idx + 1}", error_counts))

    error_title = "Error Counts Across {} Turn{}".format(len(input_strings), "s" if len(input_strings) > 1 else "")
    error_table = pd.DataFrame(
        {error: [turn_error_counts[i][1][error] for i in range(len(input_strings))] for error in error_types},
        index=[f"Turn {i+1}" for i in range(len(input_strings))]
    ).T
    error_table_md = error_table.to_markdown(index=True, numalign="left", stralign="left")

    print(f"\n{error_title}")
    print("-" * len(error_title))
    print(error_table_md)

    if all(count == 0 for count in total_error_counts.values()):
        summary = "\nNo errors found across all turns.\n"
    else:
        summary = "\nSummary of Total Error Counts\n" + "-" * 30 + "\n"
        summary += "\n".join([f"- {error}: {count}" for error, count in total_error_counts.items() if count > 0])

    print(summary)

    return total_error_counts

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

def get_input(prompt):
    user_input = input(prompt).strip()
    if user_input.lower() == 'exit':
        logging.info("Process exited by user.")
        raise SystemExit(0)
    return user_input

def process_gemini_conversation(input_strings):
    try:
        raters_id = get_persisted_raters_id()
        if raters_id:
            use_stored_id = get_input(f"Continue with stored rater's ID '{raters_id}'? (yes/no or type 'exit' to quit): ").strip().lower()
            if use_stored_id == 'no':
                raters_id = None

        while not raters_id:
            rater_id = get_input("Enter the rater's ID (numbers only or type 'exit' to quit): ")
            if rater_id.isdigit():
                save_raters_id(rater_id)
                raters_id = rater_id
            else:
                logging.error("Invalid rater's ID. Please enter numbers only.")

        while True:
            row_id = get_input("Enter the row ID (numbers only or type 'exit' to quit): ")
            if row_id.isdigit():
                break
            else:
                logging.error("Invalid row ID. Please enter numbers only.")

        num_turns = len(input_strings)
        logging.info(f"Number of conversation turns is {num_turns} based on input strings.")

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
                document_link = get_input(f"Enter link for Document {i+1} (must start with 'https://' or type 'exit' to quit): ")
                if document_link.startswith('https://'):
                    documents.append(document_link)
                    break
                else:
                    logging.error("Invalid document link. Please enter a valid URL starting with 'https://'.")

        queries = []
        for i in range(num_turns):
            query = get_input(f"Enter query for Turn {i+1} (or type 'exit' to quit): ")
            queries.append(query)

        output_file = f"Gemini_rater_{raters_id}_ID_{row_id}.ipynb"
        process_contents_to_ipynb(input_strings, queries, output_file, documents)
        
        logging.info("\n")
        count_code_errors(input_strings)

    except SystemExit:
        print("You have exited the process. You can start again later if you wish.")