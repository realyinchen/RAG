import os
import textwrap
from dotenv import load_dotenv

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from uuid import uuid4


load_dotenv()

def get_local_embedding_model(model_name: str | None = None) -> HuggingFaceEmbeddings:
    """
    Get embedding model from local path or huggingface.

    Args:
        model_name: embedding model file path or huggingface model id.

    Returns:
       HuggingFace embedding model.
    """
    if not model_name:
        model_name = os.environ.get("EMBEDDING_MODEL")
    model_kwargs = {"device": "cpu"}
    encode_kwargs = {"normalize_embeddings": True}
    return HuggingFaceEmbeddings(
        model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
    )


def replace_t_with_space(list_of_documents: list):
    """
    Replaces all tab characters ('\t') with spaces in the page content of each document

    Args:
        list_of_documents: A list of document objects, each with a 'page_content' attribute.

    Returns:
        The modified list of documents with tab characters replaced by spaces.
    """

    for doc in list_of_documents:
        doc.page_content = doc.page_content.replace(
            "\t", " "
        )  # Replace tabs with spaces
    return list_of_documents


def text_wrap(text, width=120):
    """
    Wraps the input text to the specified width.

    Args:
        text (str): The input text to wrap.
        width (int): The width at which to wrap the text.

    Returns:
        str: The wrapped text.
    """
    return textwrap.fill(text, width=width)


def encode_pdf(
    pdf_path,
    chunk_size=1000,
    chunk_overlap=200,
    host="localhost",
    port=6333,
    collection_name="rag101",
    size=1024,
    distance=Distance.COSINE,
):
    """
    Encodes a PDF book into a vector store using local embeddings.

    Args:
        pdf_path: The path to the PDF file.
        chunk_size: The desired size of each text chunk.
        chunk_overlap: The amount of overlap between consecutive chunks.
        host: The Qdrant vector store server host.
        port: The Qdrant vector store server port.
        collection_name: The collection name of the Qdrant vector store.
        size: Embedding vector size.
        distance: Embedding vector similarity metrics.

    Returns:
        A Qdrant vector store containing the encoded book content.
    """

    # Load PDF documents
    loader = PyMuPDFLoader(
        pdf_path,
        mode="single",
    )
    documents = loader.load()

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len
    )
    texts = text_splitter.split_documents(documents)
    cleaned_texts = replace_t_with_space(texts)

    # Create embeddings and vector store
    embedding_model = get_local_embedding_model()
    client = QdrantClient(host=host, port=port)

    if not client.collection_exists(collection_name=collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=size, distance=distance),
        )

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embedding_model,
    )

    ids = [str(uuid4()) for _ in range(len(cleaned_texts))]
    vector_store.add_documents(documents=cleaned_texts, ids=ids)

    return vector_store
