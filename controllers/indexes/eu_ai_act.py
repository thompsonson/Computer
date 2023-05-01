""" beginnings of an Index Controller for the EU AI Act"""

from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

import requests
from bs4 import BeautifulSoup


def extract_member_urls(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch the URL: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    member_list = soup.find("div", {"class": "erpl_member-list"})

    if not member_list:
        return []

    member_urls = []

    for member in member_list.find_all("a", {"class": "erpl_member-list-item-content"}):  # type: ignore
        member_url = member["href"]
        member_urls.append(member_url)

    return member_urls


url = "https://www.europarl.europa.eu/meps/en/search/advanced?name=&countryCode=FR"
member_urls = extract_member_urls(url)

loader = UnstructuredURLLoader(urls=member_urls)
data = loader.load()

social_media = [
    "Facebook",
    "Twitter",
    "Flickr",
    "LinkedIn",
    "YouTube",
    "Instagram",
    "Pinterest",
    "Snapchat",
    "Reddit",
]

for entry in data:
    entry.page_content = entry.page_content.replace("\t", ".")
    entry.page_content = entry.page_content.replace("\n\n", ".")
    entry.page_content = entry.page_content.replace("\r\n", ".")
    entry.page_content = entry.page_content.replace(".\n", ".")
    for x in range(1, 11):
        entry.page_content = entry.page_content.replace(".\n", ".")
        entry.page_content = entry.page_content.replace("  ", " ")
        entry.page_content = entry.page_content.replace("..", ".")
    for social in social_media:
        entry.page_content = entry.page_content.replace(
            f"Check out Parliament on {social}.", ""
        )

print(data)


embeddings = OpenAIEmbeddings()  # type: ignore

docsearch = Chroma.from_documents(data, embeddings)

query = "Who is on the EU AI committe"
docs = docsearch.similarity_search(query)

for doc in docs:
    print("______________________________________________________")
    print(doc.metadata)
    print("______________________________________________________")


#from llama_index import Document

#text_list = [text1, text2, ...]
#documents = [Document(t) for t in text_list]
