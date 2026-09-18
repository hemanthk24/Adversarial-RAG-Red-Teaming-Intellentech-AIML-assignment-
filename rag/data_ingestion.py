from dotenv import load_dotenv
from rag.embeddings import load_embedding_model
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from rag.data_loader import get_chunks


load_dotenv()

def data_ingestion_to_pinecone(splits, embedding_model, index_name="basiccare-guidelines"):
    # Initialize Pinecone
    pc = Pinecone()
    
    # Create a serverless index if it doesn't exist
    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=2048,
            metric="cosine",
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
    docsearch = PineconeVectorStore.from_documents(
        documents=splits,
        index_name=index_name,
        embedding=embedding_model
    )
    
    print("Data is successfully ingested")
    
    
if __name__ == "__main__":
    chunks = get_chunks()
    embedding = load_embedding_model()
    data_ingestion_to_pinecone(splits=chunks, embedding_model=embedding)