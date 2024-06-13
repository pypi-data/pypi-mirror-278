import os
import json
import logging
import numpy as np
from joblib import dump, load
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TextIteratorStreamer,
    GenerationConfig,
)
from sentence_transformers import SentenceTransformer
import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Download required NLTK data
nltk.download('punkt', download_dir='./nltk_data', quiet=True)
nltk.download('stopwords', download_dir='./nltk_data', quiet=True)

# Set the NLTK data path to the local directory
nltk.data.path.append('./nltk_data')

def save_model(model, model_path):
    model.save_pretrained(model_path)
    return model_path

def load_model(model_path):
    return AutoModelForCausalLM.from_pretrained(model_path)

def save_tokenizer(tokenizer, tokenizer_path):
    tokenizer.save_pretrained(tokenizer_path)
    return tokenizer_path

def load_tokenizer(tokenizer_path):
    return AutoTokenizer.from_pretrained(tokenizer_path)

def load_chat_history(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return an empty list if the file does not exist

def save_chat_history(chat_history, file_path):
    with open(file_path, 'w') as file:
        json.dump(chat_history, file, indent=4)

def update_system_message(chat_history, new_system_content):
    # Find the last 'system' message in the chat history
    system_message_found = False
    for message in reversed(chat_history):
        if message['role'] == 'system':
            message['content'] = new_system_content  # Update the content of the last 'system' message
            system_message_found = True
            break
    if not system_message_found:
        chat_history.append({"role": "system", "content": new_system_content})  # Add a new 'system' message if none exists

def relevant_history(chat_history, question):
    # Initialize the sentence transformer model for embeddings
    embedder = SentenceTransformer('all-MiniLM-L6-v2')

    # Function to preprocess and return embeddings for given texts
    def get_embeddings(texts):
        print(f"Texts to encode: {texts}")  # Debugging line
        return embedder.encode(texts)

    if len(chat_history) == 0:
        return []

    system_prompt = chat_history[0]
    # Assuming pairs are structured as consecutive user and assistant messages
    chat_pairs = chat_history[1:]

    # Prepare texts for embedding
    # Concatenate user and assistant messages for pairs to keep their context
    pair_texts = [chat_pairs[i]['content'] + " " + chat_pairs[i+1]['content']
                  for i in range(0, len(chat_pairs), 2) if i+1 < len(chat_pairs)]

    print(f"Pair texts: {pair_texts}")  # Debugging line

    if not pair_texts:
        return [system_prompt]

    # Get embeddings for each pair and the query
    pair_embeddings = get_embeddings(pair_texts)
    query_embedding = get_embeddings([question])[0]

    # Compute cosine similarity between query and each pair
    cos_similarities = np.dot(pair_embeddings, query_embedding) / (
        np.linalg.norm(pair_embeddings, axis=1) * np.linalg.norm(query_embedding)
    )

    # Get indices of the top 3 most similar pairs
    top_indices = np.argsort(cos_similarities)[-3:][::-1]

    # Re-rank the chat pairs based on these indices
    reranked_pairs = []
    for index in top_indices:
        reranked_pairs.extend(chat_pairs[index*2:index*2+2])  # Each pair has two messages

    # Reintegrate the system prompt at the beginning
    reranked_chat = [system_prompt] + reranked_pairs

    return reranked_chat

# Function to load and process PDFs
def load_pdfs(directory):
    import PyPDF2
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    documents = []
    for pdf_file in pdf_files:
        pdf_path = os.path.join(directory, pdf_file)
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
            documents.append(text)
    return documents


def text_tagger(document):
    """
    Extract relevant text from a document or a file path.

    Args:
        document (str): Text of the document or path to the document.

    Returns:
        dict: A dictionary containing relevant sentences from the document.
    """
    # Read the document
    if os.path.isfile(document):
        with open(document, 'r') as file:
            document = file.read()
    else:
        document = document

    # Tokenize the document into sentences
    sentences = sent_tokenize(document)

    # Remove stop words and tokenize each sentence
    relevant_sentences = {}
    stop_words = set(stopwords.words('english'))
    for sentence in sentences:
        words = [word.lower() for word in word_tokenize(sentence) if word.lower() not in stop_words]
        if words:
            sentence_text = ' '.join(words)
            for word in words:
                relevant_sentences.setdefault(word, []).append(sentence_text)

    return relevant_sentences
