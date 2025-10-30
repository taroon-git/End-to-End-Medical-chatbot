
from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from pinecone.grpc import PineconeGRPC
from pinecone import ServerlessSpec
from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os





load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
OPEN_API_KEY = os.environ.get('OPEN_API_KEY')


extracted_data = load_pdf_file(data='Data/')
text_chunks=text_split(extracted_data)
embeddings = download_hugging_face_embeddings()




# Make sure your API key is available
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "doctorbot"

# Create index only if it doesn't already exist
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,  # Must match your embeddings (MiniLM = 384)
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# Connect to the index
index = pc.Index(index_name)

print("✅ Pinecone index ready:", index_name)



docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings,
)