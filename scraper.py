import requests
from bs4 import BeautifulSoup


def get_content(url):
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    return soup


def clean_content(soup):
    for tag in soup(["script", "style"]):
        tag.extract()
    cleaned_content = soup.get_text()
    return cleaned_content
