import os
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from uuid import uuid4
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


# Sidebar contents
with st.sidebar:
    st.title("🤗 🗨️ LLM Chat App")
    st.markdown("""
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io)
    - [LangChain](https://www.langchain.com/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM model
    
    """)
    add_vertical_space(5)
    st.write("Made with ❤️ by 南七技校")


def main():
    st.header("Chat with PDF 🗨️")

    # upload a PDF file
    pdf = st.file_uploader("上传你的 PDF 文件", type="pdf")
    if pdf is not None:
        current_dir = os.path.dirname(__file__)
        pdf_file = os.path.join(current_dir, pdf.name)

        file_exists = os.path.exists(pdf_file)

        if not file_exists:
            with open(pdf_file, mode="wb") as f:
                f.write(pdf.getvalue())

        loader = PyPDFLoader(pdf_file)
        pages = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, add_start_index=True
        )
        all_splits = text_splitter.split_documents(pages)

        # embeddings
        embedding_model = OpenAIEmbeddings()

        # Vector Store
        client = QdrantClient(host="localhost", port=6333)

        if not client.collection_exists("demo_collection"):
            client.create_collection(
                collection_name="demo_collection",
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )

        vector_store = QdrantVectorStore(
            client=client,
            collection_name="demo_collection",
            embedding=embedding_model,
        )

        if not file_exists:
            ids = [str(uuid4()) for _ in range(len(all_splits))]
            vector_store.add_documents(documents=all_splits, ids=ids)

        retriever = vector_store.as_retriever(
            search_type="similarity", search_kwargs={"k": 3}
        )

        # Accept user question/query
        query = st.text_input("输入你的问题：")
        if query:
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
            system_prompt = (
                "You are an assistant for question-answering tasks. "
                "Use the following pieces of retrieved context to answer "
                "the question. If you don't know the answer, say that you "
                "don't know. Use three sentences maximum and keep the "
                "answer concise."
                "\n\n"
                "{context}"
            )

            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    ("human", "{input}"),
                ]
            )

            question_answer_chain = create_stuff_documents_chain(llm, prompt)
            rag_chain = create_retrieval_chain(retriever, question_answer_chain)
            response = rag_chain.invoke({"input": f"{query}"})
            st.write(response["answer"])


if __name__ == "__main__":
    main()
