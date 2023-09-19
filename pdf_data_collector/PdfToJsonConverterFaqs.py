import os
import re
import fitz  
import json
import requests

def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_document = fitz.open(pdf_file)
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text += page.get_text()

    return text

def separate_questions_and_answers(text):
    lines = text.split('\n')
    questions_and_answers = []
    current_question = ""
    current_answer = ""
    for line in lines:
        line = line.strip()
        line = re.sub(r'[\t\r\u00a0]', ' ', line)
        if line.endswith('?'):
            if current_question:
                questions_and_answers.append({
                    "question": current_question,
                    "answer": current_answer
                })
            current_question = line
            current_answer = ""
        else:
            if current_question:
                current_answer += " " + line
    return questions_and_answers



def read_file_names(path):

    if not os.path.exists(path):
        print(f"Directory '{path}' does not exist.")
        return []

    try:
        file_names = [entry.name for entry in os.scandir(path) if entry.is_file()]
        if file_names:
            print("Files found")
        return file_names
    except Exception as e:
        print(f"An error occurred while listing files: {e}")
        return []

def main():
    directory_path = r"T:\DevTools\Semester-3\COMP-293\pdfs"            #Replace with your pdf folder path
    file_names= read_file_names(directory_path)
    data={}
    for file_name in file_names: 
        print("Reading file", file_name)
        extracted_text = extract_text_from_pdf(os.path.join(directory_path, file_name))
    
        if extracted_text:
            faqs = separate_questions_and_answers(extracted_text)
            
            if faqs:
                data [file_name.replace(".pdf", "")] = faqs

            else:
                print("No questions and answers found in the {0} PDF.".format(file_name))
        else:
            print("No text extracted from the {0} PDF.".format(file_name))
        extracted_text=''

    with open("faqsFromPdf.json", "w") as json_file:
        json_file.write(json.dumps(data, indent=2) )

if __name__ == "__main__":
    main()
  