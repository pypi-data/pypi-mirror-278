"""Inverted Index Tool."""

from collections import defaultdict
import logging
from .cosmic_utils import text_tagger, load_pdfs

def inverted_index(files_or_dir):
    """
    Create a general inverted index from the relevant text in documents.

    Args:
        files_or_dir (str or list): A list of file paths or a directory path.

    Returns:
        defaultdict: Inverted index with words as keys and names of documents that contain the words as values.
    """
    inv_index = defaultdict(list)
    documents = load_pdfs(files_or_dir)

    for document in documents:
        try:
            relevant_sentences = text_tagger(document)
            for word, sentences in relevant_sentences.items():
                for sentence in sentences:
                    if document not in inv_index[word]:
                        inv_index[word].append(document)
        except Exception as e:
            logging.error(f"Error processing document: {e}")
            continue

    return inv_index