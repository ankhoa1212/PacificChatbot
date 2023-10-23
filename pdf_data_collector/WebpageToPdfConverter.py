import os
import re
import pdfkit
import requests
from bs4 import BeautifulSoup

# Set the path to the wkhtmltopdf executable
pdfkit_config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')  # Replace with the actual path
# Configure pdfkit options (you can customize these as needed)
options = {
    'page-size': 'Letter',
    'margin-top': '0mm',
    'margin-right': '0mm',
    'margin-bottom': '0mm',
    'margin-left': '0mm',
    'encoding': 'UTF-8',
    'no-outline': None
}

url_list=[]
# Open the file in read mode
with open('faq_urls_list.txt', 'r') as file:
    # Iterate through each line in the file
    for line in file:
        # Remove leading and trailing whitespaces and add the URL to the list
        url = line.strip()
        url_list.append(url)

# Create a directory named "pdfs" if it doesn't exist
pdfs_folder = "pdfs"
if not os.path.exists(pdfs_folder):
    os.makedirs(pdfs_folder)

for url in url_list:

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the web page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the title of the web page
    web_page_title = soup.title.string.strip()
    # Split the title at "FAQ" or "Frequently Asked Questions"
    title_parts = re.split(r'FAQ|Frequently Asked Questions', web_page_title)

    # Check if the first part is non-empty, and if not, use the second part
    if not title_parts[0].strip():
        web_page_title = title_parts[1].strip()
    else:
        web_page_title = title_parts[0].strip()

    # Remove invalid characters (except hyphens)
    web_page_title = re.sub(r'[^a-zA-Z0-9\s]', '', web_page_title)
    web_page_title=web_page_title.replace(" ", "-")
    print(web_page_title)

    # Define the full path to the output PDF file in the "pdfs" folder
    output_pdf = os.path.join(pdfs_folder, f'{web_page_title}.pdf')


    # Check if the file already exists, and if it does, skip conversion
    if not os.path.exists(output_pdf):
        # Convert the web page to PDF
        pdfkit.from_url(url, output_pdf, options=options, configuration=pdfkit_config)
        print(f'PDF saved to {output_pdf}')
    else:
        print(f'PDF already exists at {output_pdf}. Skipping conversion.')

        # print(f'PDF saved to {output_pdf}')
