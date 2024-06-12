#!/usr/bin/env python3

import argparse
import os
import torch
import pickle
import warnings
from threading import Thread
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TextIteratorStreamer,
    GenerationConfig,
    BitsAndBytesConfig
)
import sys
import json
import logging
import tensorflow as tf
from .cosmic_utils import (
    save_model, load_model, save_tokenizer, load_tokenizer,
    load_chat_history, save_chat_history, update_system_message,
    relevant_history, text_tagger
)
from .inverted_index import inverted_index
from nltk.tokenize import word_tokenize

# Suppress TensorFlow warnings
tf.get_logger().setLevel('ERROR')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Suppress specific Transformers warnings
warnings.filterwarnings("ignore", category=UserWarning, message="You passed `quantization_config` or equivalent parameters")
warnings.filterwarnings("ignore", category=FutureWarning, message="`resume_download` is deprecated")

parent_dir_path = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(description="Cosmic Counsel CLI")
parser.add_argument("-q", "--question", type=str, help="The user's question")
parser.add_argument("-d", "--directory", type=str, help="Directory containing PDF files to use as context")
args = parser.parse_args()

# Initialize the system message
SYSTEM_PROMPT = "Welcome to Cosmic Counsel! How can I help you today?"

# Load the model and tokenizer
model_id = "HuggingFaceH4/zephyr-7b-beta"
offload_folder = os.path.join(parent_dir_path, 'models')
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)

# Ensure the offload folder exists
os.makedirs(offload_folder, exist_ok=True)

# Check if model and tokenizer already exist
model_path = os.path.join(offload_folder, model_id.replace('/', '_'))
tokenizer_path = os.path.join(offload_folder, model_id.replace('/', '_') + '_tokenizer')

if not os.path.exists(model_path):
    print("Downloading and saving the model...")
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto",
        token='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',
        trust_remote_code=True,
        low_cpu_mem_usage=True,
        torch_dtype=torch.float16,
        offload_folder=offload_folder,
        offload_state_dict=True,
        cache_dir=offload_folder
    )
    model.save_pretrained(model_path)
else:
    print("Loading model from cache...")
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
        low_cpu_mem_usage=True,
        torch_dtype=torch.float16,
        offload_folder=offload_folder,
        offload_state_dict=True,
        cache_dir=offload_folder
    )

if not os.path.exists(tokenizer_path):
    print("Downloading and saving the tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_id, token='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',)
    tokenizer.save_pretrained(tokenizer_path)
else:
    print("Loading tokenizer from cache...")
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, cache_dir=offload_folder)

# Load the chat history
chat_history_path = os.path.join(parent_dir_path, 'data', 'chat_history.json')
chat_history = load_chat_history(chat_history_path)

# Update the system message in the chat history
update_system_message(chat_history, SYSTEM_PROMPT)

# Save the updated chat history
save_chat_history(chat_history, chat_history_path)

# Define the main function
def main():
    if args.directory:
        inverted_index_data = inverted_index(args.directory)
        with open(os.path.join(parent_dir_path, 'data', 'context_index.pkl'), 'wb') as f:
            pickle.dump(inverted_index_data, f)
        print("Context index created and saved. You can now ask questions.")
        sys.exit(0)

    if args.question:
        with open(os.path.join(parent_dir_path, 'data', 'context_index.pkl'), 'rb') as f:
            inverted_index_data = pickle.load(f)

        question = args.question

        # Load existing chat history
        chat_history_path = f"{parent_dir_path}/chat_history.json"
        chat_history = load_chat_history(chat_history_path)

        # Update or add a new 'system' message
        new_system_content = SYSTEM_PROMPT
        update_system_message(chat_history, new_system_content)

        import time
        start_time = time.time()

        generation_config = GenerationConfig(
            num_beams=1,
            early_stopping=False,
            decoder_start_token_id=0,
            eos_token_id=model.config.eos_token_id,
            pad_token_id=50256,
            temperature=0.01,
            do_sample=True
        )

        streamer = TextIteratorStreamer(
            tokenizer, skip_prompt=True, skip_special_tokens=True
        )

        generation_kwargs = {
            "streamer": streamer,
            "generation_config": generation_config,
            "max_new_tokens": 200,
        }

        relevant_hist = relevant_history(chat_history, question)

        # Find relevant documents using the inverted index
        relevant_docs = []
        question_words = set(word.lower() for word in word_tokenize(question))
        for word in question_words:
            if word in inverted_index_data:
                relevant_docs.extend(inverted_index_data[word])
        
        # Extract relevant sentences from the relevant documents
        relevant_sentences = []
        for doc in set(relevant_docs):
            relevant_sentences.extend(text_tagger(doc))
        
        # Combine relevant sentences into a single context string
        context = ' '.join(relevant_sentences)
        # Assume we're adding a new user question
        new_user_message = {"role": "user", "content": question}

        relevant_hist.append(new_user_message)

        chat_history.append(new_user_message)

        save_chat_history(relevant_hist, f"{parent_dir_path}/relevant_history.json")

        # Prepend the context to the question for input to the model
        question_with_context = f"Context: {context}\nQuestion: {question}"
        inputs = tokenizer.apply_chat_template(
            [{"role": "system", "content": "You are a helpful AI assistant."}, {"role": "user", "content": question_with_context}],
            tokenize=True, add_generation_prompt=False, return_tensors="pt"
        ).to(model.device)

        thread = Thread(target=model.generate, args=(inputs,), kwargs=generation_kwargs)
        thread.start()

        gen_text = ""
        for new_text in streamer:
            gen_text += new_text.split("\n")[-1]
            sys.stdout.write(new_text.split("\n")[-1])
            sys.stdout.flush()

        # Append the generated response to the chat history
        chat_history.append({"role": "assistant", "content": gen_text})
        # Save the updated chat history back to the JSON file
        save_chat_history(chat_history, chat_history_path)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"\nExecution time: {execution_time} seconds")

if __name__ == "__main__":
    main()
