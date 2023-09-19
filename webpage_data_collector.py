import json
import urllib.request
from bs4 import BeautifulSoup

def url_to_html(url: str, encoding = "utf-8"):
    """returns html code from url input, assuming the page is using utf8 encoding"""
    request = urllib.request.urlopen(url)  # send url request
    bytes = request.read()  # read bytes from url request
    html = bytes.decode(encoding)  # convert bytes to string
    return html

def url_to_dict(url: str) -> dict:
    """returns dictionary with webpage data from url input"""
    soup = BeautifulSoup(url_to_html(url), 'html.parser')
    data = {}
    data["url"] = url
    data["title"] = str(soup.find("title").get_text(strip=True))

    # parse body into separate elements
    body_text = []
    for text in soup.find("body").children:
        text = text.get_text(strip=True)
        if text != "":
            body_text.append(text)
    data["body"] = body_text

    # parse links into a dict: {link_text, link_url}
    links = {}
    for link in soup.find_all("a"):
        url = str(link.get("href"))
        if not (url.startswith("#") or url == ""):
            links[link.get_text()] = url
    data["links"] = links

    return data

def write_to_file(input_filename = "url_list.txt", output_filename = "data.json"):
    """writes data from webpages and adds it into the output file
    if url data needs to be updated, output file needs to be cleared 
    """
    url_list = []
    with open(input_filename, "r") as input_file:
        url_list = input_file.readlines()
    all_url_data = []
    for url in url_list:
        url_data = url_to_dict(url.strip())
        all_url_data.append(url_data)
    with open(output_filename, "a") as output_file:
        json.dump(all_url_data, output_file, indent=4)

def extract_txt_from_json(input_filename = "data.json", output_filename = "data.txt"):
    """extracts text from input json file to output txt file"""
    with open(input_filename, "r", encoding="utf-8") as input_file:
        data = json.load(input_file)
    with open(output_filename, "a") as output_file:
        for webpage in data:
            for text in webpage["body"]:
                try:
                    output_file.writelines(text)
                except UnicodeEncodeError:  # ignore file encoding error
                    pass


write_to_file()
