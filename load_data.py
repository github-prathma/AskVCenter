from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
import httpx
from bs4 import BeautifulSoup
import logging
import requests
from langchain.document_loaders import WebBaseLoader

headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS 13_2_1) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9"
    }

urls = [
    "https://developer.visa.com/use-cases/transaction-data-enrichment",
    "https://developer.visa.com/capabilities/card-on-file-data-inquiry/docs-getting-started#section1",
    "https://developer.visa.com/capabilities/card-on-file-data-inquiry/reference#tag/Card-On-File-Data-Service-API/operation/Card-On-File%20Data%20Service_v1%20-%20Latest"
]

def scrape_data():
    # speech_text = ""
    # for url in urls:
    #     response = requests.get(url)
    #     soup = BeautifulSoup(response.text, "html.parser")
    #     # logging.info(soup.prettify)

    #     speech_section = soup.find_all("div")
    #     logging.info(speech_section)
    #     # if speech_section:
    #     #     for x in speech_section:
    #     #         paragraph_tags = x.find_all("p")
    #     #         speech_text = "".join([p.get_text() for p in paragraph_tags])
    # with open("data_doc.txt", "a") as file:
    #     file.write(str(speech_section))
    loader = WebBaseLoader(urls)
    loader.requests_per_second = 1
    data = loader.load()
    # return speech_text.replace("\t", "")
    return data


def loadDataFromUrls():
    loader = UnstructuredURLLoader(urls=urls)
    data = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(data)
    return texts

def getTextsData():
    speech_texts = scrape_data()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    logging.info(text_splitter)
    texts = text_splitter.split_documents(speech_texts)
    return texts