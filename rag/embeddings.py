from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
import os

load_dotenv()  # Load environment variables from .env file

# Global singleton variable
_embedding_model = None

def load_embedding_model():
    """
    Load the NVIDIA embedding model using the API key from environment variables.
    """
    global _embedding_model
    try:
        if _embedding_model is None:
            _embedding_model = NVIDIAEmbeddings(
                model="nvidia/nemotron-3-embed-1b",
                truncate="END"
            )
            print("NVIDIA Nemotron Embedding Model loaded successfully.")
        return _embedding_model
    except Exception as e:
        print(f"Failed loading NVIDIA Embedding Model: {e}")
        raise e



