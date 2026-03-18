import os
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from jenkins_chatbot_backend.config import settings

JENKINS_DOC_URLS = [
    "https://www.jenkins.io/doc/book/pipeline/",
    "https://www.jenkins.io/doc/book/pipeline/syntax/",
    "https://www.jenkins.io/doc/book/pipeline/jenkinsfile/",
    "https://plugins.jenkins.io/"
]

JENKINSFILE_EXAMPLES = [
    {
        "content": "pipeline {\n    agent any\n    stages {\n        stage('Install') { steps { sh 'npm install' } }\n        stage('Test') { steps { sh 'npm test' } }\n        stage('Build') { steps { sh 'npm run build' } }\n        stage('Docker Build') { steps { sh 'docker build -t myapp:latest .' } }\n    }\n}",
        "source": "Node.js Jenkinsfile example"
    },
    {
        "content": "pipeline {\n    agent any\n    stages {\n        stage('Install') { steps { sh 'pip install -r requirements.txt' } }\n        stage('Test') { steps { sh 'pytest tests/' } }\n        stage('Build') { steps { sh 'python setup.py build' } }\n    }\n}",
        "source": "Python Jenkinsfile example"
    },
    {
        "content": "pipeline {\n    agent any\n    stages {\n        stage('Build') { steps { sh 'mvn clean package' } }\n        stage('Test') { steps { sh 'mvn test' } }\n        stage('Deploy') { steps { sh 'mvn deploy' } }\n    }\n}",
        "source": "Maven Jenkinsfile example"
    }
]

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

model = SentenceTransformer("all-MiniLM-L6-v2")


def scrape_url(url):
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        texts = [t.get_text() for t in soup.find_all(['p', 'li', 'pre', 'code'])]
        content = "\n".join(texts)
        return content
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return ""

def chunk_text(text):
    tokens = text.split()
    chunks = []
    for i in range(0, len(tokens), CHUNK_SIZE - CHUNK_OVERLAP):
        chunk = " ".join(tokens[i:i+CHUNK_SIZE])
        chunks.append(chunk)
    return chunks

def main():
    docs = []
    for url in JENKINS_DOC_URLS:
        print(f"Scraping {url}...")
        content = scrape_url(url)
        if content:
            for chunk in chunk_text(content):
                docs.append({"content": chunk, "source": url})
    for example in JENKINSFILE_EXAMPLES:
        for chunk in chunk_text(example["content"]):
            docs.append({"content": chunk, "source": example["source"]})
    print(f"Total chunks: {len(docs)}")
    embeddings = model.encode([doc["content"] for doc in docs])
    index = faiss.IndexFlatL2(model.get_sentence_embedding_dimension())
    index.add(np.array(embeddings, dtype=np.float32))
    os.makedirs(os.path.dirname(settings.faiss_index_path), exist_ok=True)
    faiss.write_index(index, settings.faiss_index_path)
    np.save(settings.faiss_index_path + "_docs.npy", np.array([doc["content"] for doc in docs], dtype=object))
    np.save(settings.faiss_index_path + "_sources.npy", np.array([doc["source"] for doc in docs], dtype=object))
    print("FAISS index created and saved.")

if __name__ == "__main__":
    main()
