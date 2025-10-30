# End-to-End-Medical-chatbot

How to run (Linux):

```bash
git clone https://github.com/taroon-git/End-to-End-Medical-chatbot.git
cd End-to-End-Medical-chatbot

python3 -m venv llmapp
source llmapp/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
```

- Need to run store_index.py  for the first time to store the data into pinecone db.