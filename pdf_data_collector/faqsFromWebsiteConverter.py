import requests
from bs4 import BeautifulSoup
import json

try:
    # Fetch the web page content
    url = 'https://www.pacific.edu/admission/international-students/international-students-faq'
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP errors
    html = response.text

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Locate and extract questions and answers
    faq_data = []
    for question_elem, answer_elem in zip(soup.select('h4'), soup.select('p')):
        question = question_elem.text.strip()
        answer = answer_elem.text.strip()
        faq_data.append({"question": question, "answer": answer})

    if not faq_data:
        
        print("No data was extracted. Check your scraping selectors.")
    else:
        # Convert to JSON
        faq_json = json.dumps(faq_data, indent=4)

        # Save to a JSON file
        with open('faq.json', 'w') as json_file:
            json_file.write(faq_json)

except Exception as e:
    print(f"An error occurred: {str(e)}")
