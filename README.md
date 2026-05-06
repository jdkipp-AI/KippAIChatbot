\# KippAI Chatbot - Closed-Domain RAG Chatbot



A fully local, closed-domain Retrieval-Augmented Generation (RAG)

chatbot built with LangChain, ChromaDB, and Ollama. The chatbot

answers questions strictly based on four Wikipedia-sourced PDF

documents. It will not hallucinate or answer questions outside

of its knowledge base.



!\[Chatbot Demo](assets/demo\_screenshot.png)



\---



\## Knowledge Base



This chatbot is built on the following four Wikipedia articles

(first 4 pages each):



\- aztecs.pdf - Aztec Culture and Civilization

\- french\_and\_indian\_war.pdf - The French and Indian War

\- american\_black\_bear.pdf - The American Black Bear

\- huskiesfb.pdf - University of Washington Huskies Football



\---



\## How It Works



This project uses a Closed-Domain RAG (Retrieval-Augmented

Generation) pipeline:



1\. Ingest - PDF documents are loaded and split into chunks

2\. Embed - Each chunk is converted into a vector embedding

&#x20;  using mxbai-embed-large

3\. Store - Embeddings are stored in a local ChromaDB vector

&#x20;  database

4\. Retrieve - User queries are matched against the most

&#x20;  relevant chunks (k=10)

5\. Generate - llama3.2 generates an answer strictly based

&#x20;  on the retrieved context

6\. Log - Every query and response is logged to a CSV file

&#x20;  with response timing



If the answer is not found in the documents, the chatbot

responds with "I do not know" - no hallucinations.



\---



\## Tech Stack



\- Framework: LangChain 1.2.10

\- LLM: Ollama - llama3.2

\- Embeddings: Ollama - mxbai-embed-large

\- Vector Store: ChromaDB 1.5.5 (local, persistent)

\- PDF Loader: PyPDF 6.9.0

\- Environment: Conda (langchain\_env)

\- Language: Python 3.11



\---



\## Project Structure

KippAIChatbot/

│

├── docs/

│ ├── aztecs.pdf

│ ├── french\_and\_indian\_war.pdf

│ ├── american\_black\_bear.pdf

│ └── huskiesfb.pdf

│

├── chroma\_db/

│

├── assets/

│ └── demo\_screenshot.png

│

├── run\_chatbot.py

├── diag.py

│

├── chatbot\_performance.csv

├── environment.yml

├── requirements.txt

├── .gitignore

└── README.md

text



\---



\## Setup and Installation



Prerequisites:

\- Miniconda or Anaconda installed

\- Ollama installed and running



Step 1 - Clone the Repository:

```bash

git clone https://github.com/YOUR\_USERNAME/KippAIChatbot.git

cd KippAIChatbot

Step 2 - Create and Activate Conda Environment:

bash

conda env create -f environment.yml

conda activate langchain\_env

Step 3 - Install Dependencies:

bash

pip install -r requirements.txt

Step 4 - Pull Required Ollama Models:

bash

ollama pull llama3.2

ollama pull mxbai-embed-large

Step 5 - Verify Ollama is Running:

bash

ollama list

You should see both llama3.2 and mxbai-embed-large listed.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Running the Chatbot

Step 1 - Inspect Your PDFs (Optional but Recommended):

bash

python diag.py

This confirms all PDFs are loading correctly before indexing.

Step 2 - Launch the Chatbot:

bash

python run\_chatbot.py

•	On first run, PDFs are indexed and saved to chroma\_db/

•	On subsequent runs, the existing vector store loads instantly

Step 3 - Ask Questions:

text

Ask: How many national championships does Washington claim?

AI Response (142.28s): Washington claims two national

championships in college football: 1960 and 1991.



Ask: When did the French and Indian War begin?

AI Response (115.15s): The French and Indian War began

on May 28, 1754.



Ask: What is the American Black Bear's diet?

AI Response (120.0s): The American Black Bear is an

omnivore, with a diet varying greatly depending on

season and location...



Ask: What is another name for the Aztec Culture?

AI Response (110.37s): The term "Nahua" is sometimes

used to refer to the Aztec culture...

Type 'exit' to quit the chatbot.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Performance Logging

Every query is automatically logged to chatbot\_performance.csv

with the following fields:

•	Timestamp - Date and time of query

•	Query - The question asked

•	Response - The AI answer (truncated to 200 characters)

•	Duration\_Seconds - How long the response took

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Performance Note

This project runs fully locally via Ollama with no API keys

or internet connection required.

•	CPU only (current setup): 110-150 seconds per response

•	NVIDIA GPU (8GB+ VRAM): 3-10 seconds per response

Running on an NVIDIA GPU with CUDA support would provide

approximately 20-50x faster response times. Ollama

automatically detects and uses NVIDIA GPUs via CUDA.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Closed-Domain Design

This chatbot is intentionally restricted to its knowledge base:

•	Answers questions found in the 4 PDF documents

•	Provides source grounding via retrieved context

•	Refuses to answer questions outside the knowledge base

•	Does not use the LLM's general training knowledge

•	Responds with "I do not know" when the answer is not found

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Configuration

Key settings in run\_chatbot.py:

•	FORCE\_REBUILD = False (Set True to re-index PDFs after changes)

•	chunk\_size = 800 (Text chunk size for splitting)

•	chunk\_overlap = 200 (Overlap between chunks)

•	k = 10 (Number of chunks retrieved per query)

•	temperature = 0 (0 = strictly factual, no creativity)

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Dependencies

•	langchain 1.2.10

•	langchain-community 0.4.1

•	langchain-chroma 1.1.0

•	langchain-ollama 1.0.1

•	langchain-classic 1.0.1

•	langchain-core

•	langchain-text-splitters

•	chromadb 1.5.5

•	pypdf 6.9.0

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Author

JDKip

Built as part of the Outlier AI Model Playground project series.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

License

This project is for educational purposes only.

PDF content sourced from Wikipedia under the

Creative Commons Attribution-ShareAlike License.

https://creativecommons.org/licenses/by-sa/4.0/

text



\---





