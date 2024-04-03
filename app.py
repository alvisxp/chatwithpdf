import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS

def get_pdf_text(pdf_docs):
    text = " "
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    # embeddings = OpenAIEmbeddings()
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore




def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with PDFs", page_icon = ":books:")

    st.header("Chat with PDFs :books:")
    st.text_input("Ask me anything about your PDFs:")

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):

                raw_text = get_pdf_text(pdf_docs)

                text_chunks = get_text_chunks(raw_text)
                
                # Vector Store
                vectorstore = get_vectorstore(text_chunks)
                print(vectorstore) 



                 


if __name__ == "__main__":
    main()