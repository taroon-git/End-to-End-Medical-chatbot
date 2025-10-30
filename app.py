from flask import Flask, render_template, request
from src.helper import download_hugging_face_embeddings
from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
OPENAI_API_KEY = os.environ.get("OPEN_API_KEY")

# Set environment variables for LangChain/OpenAI
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

embeddings = download_hugging_face_embeddings()

# index_name = "doctorbot"
index_name = "medicalbot"

# Load stored embeddings from Pinecone
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

# Create retriever
retriever = docsearch.as_retriever(search_kwargs={"k": 3})

# retrieved_docs = retriever.invoke("What is Acne?")
# print(retrieved_docs)


# Load Chat model
llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o-mini", temperature=0.4)

# Create prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{question}")
    ]
)

# context = "\n\n".join(doc.page_content for doc in docs)
# response = llm.invoke(prompt.format(context=context, question=question))

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_question = request.form["msg"].strip()

    # Greeting detection
    greetings = ["hi", "hii", "hello", "hey", "hi doctor", "hey doctor", "good morning", "good evening"]
    if user_question.lower() in greetings:
        return "Hii, how can I help you today? 🩺"

    # Retrieve context
    docs = retriever.invoke(user_question)
    context = "\n\n".join(doc.page_content for doc in docs).strip()

    # If context is empty → allow LLM to answer freely
    if not context:
        final_prompt = f"{system_prompt.replace('{context}', '')}\n\nUser Question: {user_question}\nAnswer:"
    else:
        final_prompt = prompt.format(context=context, question=user_question)

    answer = llm.invoke(final_prompt).content.strip()

    return answer



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)