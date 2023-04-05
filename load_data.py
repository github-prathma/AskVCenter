from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter


urls = [
    "https://developer.visa.com/capabilities/card-on-file-data-inquiry/docs-getting-started#section1",
    "https://developer.visa.com/capabilities/card-on-file-data-inquiry/reference#tag/Card-On-File-Data-Service-API/operation/Card-On-File%20Data%20Service_v1%20-%20Latest"
]

def loadDataFromUrls():
    loader = UnstructuredURLLoader(urls=urls)
    data = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(data)
    return texts

