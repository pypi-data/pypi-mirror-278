import re
import json

def process_contents_to_ipynb(input_strings, output_filename):
    cells = []
    
    # Add the appropriate title based on the number of input strings
    if len(input_strings) > 1:
        title = "MULTI-TURN"
    else:
        title = "SINGLE-TURN"
    
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [title + '\n']
    })

    for idx, input_string in enumerate(input_strings):
        turn_number = idx + 1
        turn_markdown = f"Turn {turn_number}"
        query_data_markdown = f"Query {turn_number}:\n\nData:\n"

        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [turn_markdown + '\n']
        })
        
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [query_data_markdown + '\n']
        })
        
        # Remove text blocks enclosed with triple backticks that start with ```text?code_stdout or ```text?code_stderr
        cleaned_content = re.sub(r'```text\?code_stdout.*?\n.*?\n```', '', input_string, flags=re.DOTALL)
        cleaned_content = re.sub(r'```text\?code_stderr.*?\n.*?\n```', '', cleaned_content, flags=re.DOTALL)

        # Extract code blocks
        code_blocks = re.findall(r'```python\?code.*?\n(.*?)\n```', cleaned_content, flags=re.DOTALL)

        # Remove code block markers but keep the actual code for separate handling
        cleaned_content = re.sub(r'```python\?code.*?\n', 'CODE_BLOCK_START\n', cleaned_content)
        cleaned_content = re.sub(r'\n```', '\nCODE_BLOCK_END', cleaned_content)

        # Split the content by the markers
        split_content = cleaned_content.split('\n')

        # Process the split content to organize text and code blocks
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

    # Create the notebook structure
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

    # Save the notebook content to a .ipynb file
    with open(output_filename, 'w', encoding='utf-8') as file:
        json.dump(notebook_content, file, ensure_ascii=False, indent=2)

def count_code_errors(input_strings):
    # Define the error types to count
    error_types = [
        'AttributeError', 'ValueError', 'ModuleNotFoundError',
        'FileNotFoundError', 'KeyError', 'TypeError',
        'NameError', 'SyntaxError'
    ]

    # Initialize a dictionary to count the errors
    total_error_counts = []
    
    for idx, input_string in enumerate(input_strings):
        error_counts = {error: 0 for error in error_types}
        
        # Find all traceback blocks
        tracebacks = re.findall(r'Traceback \(most recent call last\):.*?(?=\n\n|\Z)', input_string, re.DOTALL)
        
        # Count the occurrences of each error type within the tracebacks
        for traceback in tracebacks:
            for error in error_types:
                if f"{error}:" in traceback:
                    error_counts[error] += 1
        
        total_error_counts.append((f"Turn {idx + 1}", error_counts))
    
    # Display the error counts in an intuitive format
    for turn, counts in total_error_counts:
        print(f"\n{turn} Error Counts:")
        for error, count in counts.items():
            print(f"{error}: {count}")
    
    return total_error_counts