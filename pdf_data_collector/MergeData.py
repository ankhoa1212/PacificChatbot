import json

# Load the JSON data
with open('faqsFromPdf.json', 'r') as json_file:
    json_data = json.load(json_file)

# Read the missing data from the text file
with open('Full_Cleaned_input.txt', 'r',encoding='utf-8') as text_file:
    text_file_content = text_file.read()

import re
import json

def fill_missing_answers(json_data, text_file_content):
    for category, questions_and_answers in json_data.items():
        for qa_pair in questions_and_answers:
            if not qa_pair["answer"].strip():
                question = qa_pair["question"]
                # Find the question in the text file
                question_start = text_file_content.find(question)
                if question_start != -1:
                    # Find the end of the statement following the question
                    statement_end = text_file_content.find('.', question_start + len(question))
                    if statement_end != -1:
                        # Extract the statement as the answer
                        answer_from_text_file = text_file_content[question_start + len(question):statement_end].strip()
                        qa_pair["answer"] = answer_from_text_file if answer_from_text_file else '+'
                    else:
                        # If no period (.) found, set the answer to '+'
                        qa_pair["answer"] = '+'
                else:
                    # If the question is not found, set the answer to '+'
                    qa_pair["answer"] = '+'
                print(f"Question: {question}")
                print(f"Answer from Text: {qa_pair['answer']}")
    return json_data


# Fill missing answers
updated_json_data = fill_missing_answers(json_data, text_file_content)

# Store the updated JSON data in a file
with open('updated_faqs.json', 'w') as updated_json_file:
    json.dump(updated_json_data, updated_json_file, indent=2)

print("Updated JSON data has been saved to 'updated_faqs.json'")
