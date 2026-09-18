from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from rag.metadata_and_datapaths import DOCUMENT_METADATA, DATA_DIR

# load documents and add metadata
def load_documents_with_metadata(data_dir, metadata_list):
    all_docs = []
    for i, file_path in enumerate(data_dir):
        loader = TextLoader(file_path, encoding="utf-8")
        docs = loader.load()
        docs[0].metadata = metadata_list[i]
        all_docs.extend(docs)
    return all_docs

# split documents into chunks
def split_documents(docs, chunk_size=400, chunk_overlap=60):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    return text_splitter.split_documents(docs)

# Global singleton variable
_chunks = None

def get_chunks():
    global _chunks
    try:
        if _chunks is None:
            docs = load_documents_with_metadata(DATA_DIR,DOCUMENT_METADATA)
            chunks = split_documents(docs)
            print("chunks Created")
        return chunks
    except Exception as e:
        print(f"Exception occured while creating the chunks : {e}")
        raise e


