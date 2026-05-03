
import os
import re
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()

class BISRagEngine:
    def __init__(self, data_path="data/"):
        self.data_path = data_path
        self.embeddings = OpenAIEmbeddings()
        self.vector_db = self._initialize_engine()

    def _initialize_engine(self):
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
            
        loader = DirectoryLoader(self.data_path, glob="./*.pdf", loader_cls=PyPDFLoader)
        docs = loader.load()
        
        # Optimized chunking for regulatory documents
        splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
        chunks = splitter.split_documents(docs)
        
        return FAISS.from_documents(chunks, self.embeddings)

    def extract_ids(self, text):
        """Extracts IS codes (e.g., IS 456) for the evaluation script."""
        pattern = r"IS\s\d+(?::\d+)?"
        ids = re.findall(pattern, text)
        return list(dict.fromkeys(ids))[:5]

    def get_recommendations(self, query: str):
        prompt_template = """
        Context: {context}
        Product: {question}

        Strictly use the context above. Identify top 3-5 BIS Standards.
        For each, provide the 'IS Number' and a short 'Rationale'.
        Do not hallucinate standards not found in the context.
        """
        
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        
        chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model="gpt-4o-mini", temperature=0), # mini for < 5s latency
            chain_type="stuff",
            retriever=self.vector_db.as_retriever(search_kwargs={"k": 5}),
            chain_type_kwargs={"prompt": PROMPT}
        )
        
        result_text = chain.invoke(query)["result"]
        return {
            "text": result_text,
            "ids": self.extract_ids(result_text)
        }