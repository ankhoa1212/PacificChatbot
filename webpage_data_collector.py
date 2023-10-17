import json
import random
import threading
import urllib.request
from datetime import datetime
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup

def url_to_html(url: str, encoding = "utf-8"):
    """returns html code from url input, assuming the page is using utf8 encoding"""
    html = None
    try:
        request = urllib.request.urlopen(url)  # send url request
        bytes = request.read()  # read bytes from url request
        html = bytes.decode(encoding)  # convert bytes to string
    except (HTTPError, URLError, ValueError, TimeoutError, UnicodeDecodeError) as e:
        print(f"An error occurred while trying to retrieve html from {url}: {e}")
        pass
    return html

def url_to_dict(url: str) -> dict:
    """returns dictionary with webpage data from url input"""
    html = url_to_html(url)
    if not html:
        return None
    soup = BeautifulSoup(html, 'html.parser')
    data = {}
    data["url"] = url
    if soup.find("title"):  # html might not have title
        data["title"] = str(soup.find("title").get_text(strip=True))

    # parse body into separate elements
    body_text = []
    if soup.find("body"):  # html might not have body
        for text in soup.find("body").children:
            text = text.get_text(strip=True)
            remove = []
            stack = []
            for i, c in enumerate(text):
                if c == '{':  # c is curly brace
                    stack.append(c) # push curly brace onto stack
                    if not remove:
                        remove.append(i)
                else:           # c is closed curly brace
                    # string is not valid
                    if not stack or \
                        (c == '}' and stack[-1] != '{'):
                        stack = False
                        break
                    stack.pop() # pop open curly brace
                    if len(remove) > 2:
                        remove.pop()
                    remove.append(i+1)
            if not stack and len(remove) > 0:
                text = text[0:remove[0]] + text[remove[1]:]
            if text != "":
                body_text.append(text)
    data["body"] = body_text

    # parse links into a dict: {link_text, link_url}
    links = {}
    for link in soup.find_all("a"):
        url = str(link.get("href"))
        if not (url.startswith("#") or url == ""):
            links[link.get_text().strip()] = url
    data["links"] = links

    return data

def timeout_function():
    raise TimeoutError(f"Timeout has occurred.")

def url_to_list_of_webpage_links(url: str):
    url_list = set()
    exclude_list = ["facebook", "instagram", "google", "messenger", "whatsapp", "oculus"]
    try:
        print(f"sending http request to {url}...")
        timeout_duration = 60
        timer = threading.Timer(timeout_duration, timeout_function)
        try:
            soup = BeautifulSoup(url_to_html(url), 'html.parser')
            timer.cancel()
        except TimeoutError as e:
            raise TimeoutError(f"{e}")
        finally:
            timer.cancel()
        print("html received")
        for link in soup.find_all("a"):
            url = str(link.get("href"))
            print("checking internal link...")
            if not (url.startswith("#") or url == ""):
                if (word not in url for word in exclude_list):
                    url_list.add(url)
    except (ValueError, HTTPError, URLError, TimeoutError, UnicodeDecodeError) as e:
        print(f"An error occurred while trying to retrieve html from {url}: {e}")
        pass
    return url_list

def write_to_file(input_filename = "url_list.txt", output_filename = "data.json"):
    """writes data from webpages and adds it into the output file
    if url data needs to be updated, output file needs to be cleared 
    """
    url_list = []
    with open(input_filename, "r") as input_file:
        url_list = input_file.readlines()
    all_url_data = []
    for url in url_list:
        print(f"getting data from {url}")
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
            if webpage:  # webpage may be None
                for text in webpage["body"]:
                    try:
                        output_file.writelines(text)
                    except UnicodeEncodeError:  # ignore file encoding error
                        pass

def append_url_list(url: str, url_list: set, output_filename: str, tabs=0):
    if tabs > 1:
        return
    with open(output_filename, "a") as output_file:
        temp_list = url_to_list_of_webpage_links(url)
        for temp_url in temp_list:
            print("\t" * tabs + temp_url)
            if temp_url.startswith("http") and temp_url not in url_list:
                url_list.add(temp_url)
                output_file.write(temp_url + "\n")
                append_url_list(temp_url, url_list, output_filename, tabs=tabs+1)
        if url.startswith("http") and url not in url_list and "pacific" in url:
            url_list.add(url)
            output_file.write(url + "\n")

def generate_url_list(input_filename = "url_list.txt", output_filename="master_url_list.txt"):
    """Check each url in input file and check for links recursively until 
    either no more new links are found or a depth layer of 1 has been reached"""
    url_list = set()
    with open(input_filename, "r") as input_file:
        data = input_file.readlines()
        with open(output_filename, "r") as output_file:
            for line in output_file:
                url = line.strip()
                url_list.add(url)
        for line in data:
            url_list.add(line)
            append_url_list(url=line, url_list=url_list, output_filename=output_filename)  # recursive function

def shortened_url_list(input_file: str, output_file: str, num_urls: int):
    """Grabs a number num_urls of urls from the input file and places them into an output file"""
    # Specify the input file path
    file_path = input_file

    # Initialize a list to store the selected lines
    selected_lines = []

    # Open the input_file for reading
    with open(file_path, 'r') as file:
        # Count the total number of lines
        total_lines = sum(1 for _ in file)

        # Reset the file pointer to the beginning of the file
        file.seek(0)

        # Generate num_urls unique random line numbers
        random_line_numbers = random.sample(range(total_lines), num_urls)

        # Read and store the selected lines
        for line_number, line in enumerate(file, start=1):
            if line_number - 1 in random_line_numbers:
                selected_lines.append(line)

    with open(output_file, 'w') as file:
        file.writelines(selected_lines)
    # Now, selected_lines contains num_urls random lines from the file

# print("generating url list...")
# generate_url_list()
# print("generating shortened url list...")
# shortened_url_list("master_url_list.txt", "extra_url_list.txt", 200)
# print("writing to file...")
# write_to_file("extra_url_list.txt", "extra_data.json")
# print("converting json to txt...")
# extract_txt_from_json("extra_data.json", "extra_data.txt")
# print("done")
