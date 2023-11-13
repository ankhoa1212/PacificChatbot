import json
import re

def fill_missing_answers(json_data, text_file_content):
    for category, questions_and_answers in json_data.items():
        for qa_pair in questions_and_answers:
            if not qa_pair["answer"].strip():
                question = qa_pair["question"]

                # Use regex for more flexible matching
                pattern = re.escape(question) + r'(.*?)(?:\n\n|\.)'
                match = re.search(pattern, text_file_content, re.DOTALL | re.IGNORECASE)

                if match:
                    # Extract the statement as the answer
                    answer_from_text_file = match.group(1).strip()
                    qa_pair["answer"] = answer_from_text_file if answer_from_text_file else '+'
                else:
                    # If the question is not found, set the answer to '+'
                    qa_pair["answer"] = '+'

                print(f"Question: {question}")
                print(f"Answer from Text: {qa_pair['answer']}")

    return json_data

# Load the JSON data
with open('faqsFromPdf.json', 'r') as json_file:
    json_data = json.load(json_file)

# Read the missing data from the text file
with open('Full_Cleaned_input.txt', 'r', encoding='utf-8') as text_file:
    text_file_content = text_file.read()

# Fill missing answers
updated_json_data = fill_missing_answers(json_data, text_file_content)

# Store the updated JSON data in a file
with open('updated_faqs.json', 'w') as updated_json_file:
    json.dump(updated_json_data, updated_json_file, indent=2)

print("Updated JSON data has been saved to 'updated_faqs.json'")
