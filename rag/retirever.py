from langchain_pinecone import PineconeVectorStore
from rag.embeddings import load_embedding_model
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from rag.data_loader import get_chunks


# vectorstore
def vectordb(index_name,embedding_model):
    vector_store = PineconeVectorStore(
        index_name=index_name,
        embedding=embedding_model
    )
    return vector_store

embedding_model = load_embedding_model()
chunks = get_chunks()


# retriever
def create_retriever(chunks, index_name, search_type="mmr", search_kwargs=None):
    vector_store = vectordb(index_name,embedding_model=embedding_model)
    pinecone_retriever = vector_store.as_retriever(
        search_type=search_type,
        search_kwargs=search_kwargs
    )
    # bm25
    bm25_retriever = BM25Retriever.from_documents(chunks)
    
    bm25_retriever.k = 3
      
    # hybrid retiever
    hybrid_retiever = EnsembleRetriever(
        retrievers=[pinecone_retriever,bm25_retriever],
        weights=[0.8,0.2]
    )
    
    return hybrid_retiever


_retriever = None

def get_retriever():
    global _retriever
    try:
        if _retriever is None:
            _retriever = create_retriever(chunks=chunks,index_name="basiccare-guidelines", search_type="mmr", search_kwargs={"k": 3, "fetch_k":8, "lambda_mult":0.5})
            print("Intialized the retriever")
        return _retriever
    except Exception as e:
        print(f"Failed Loading the Retriever: {e}")
        raise e