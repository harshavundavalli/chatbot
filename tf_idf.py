from sklearn.feature_extraction.text import TfidfVectorizer
import os
import nltk
from nltk.tokenize import sent_tokenize
from collections import defaultdict
import string
import pickle
import json



def create_knowledge_base(important_terms, directory):
    knowledge_base = defaultdict(list)

    for term in important_terms:
        
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read().lower()
                    sentences = sent_tokenize(content)
                    for sentence in sentences:
                        if term in sentence:
                            knowledge_base[term].append(sentence)
    return knowledge_base

def extract_important_terms(files_directory, num_terms):
    file_contents = []
    for filename in os.listdir(files_directory):
        with open(os.path.join(files_directory, filename), 'r', encoding='utf-8', errors = "ignore") as file:
            content = file.read()
            file_contents.append(content)

    # Preprocess text
    preprocessed_texts = [text for text in file_contents]
    
    # Calculate TF-IDF scores
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(preprocessed_texts)
    feature_names = vectorizer.get_feature_names_out()
    
    # Summarize and extract top terms
    total_tfidf_scores = tfidf_matrix.sum(axis=0)
    total_tfidf_scores = total_tfidf_scores.tolist()[0]
    term_scores = [(term, score) for term, score in zip(feature_names, total_tfidf_scores)]
    term_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Extract top terms
    important_terms = [term for term, _ in term_scores[:num_terms]]
    
    return important_terms

directory='cleaned_texts_NTR'
scraped_directory='scraped_texts_NTR'
# Extract important terms using TF-IDF
important_terms = extract_important_terms(directory, 15)

unwanted={'rao','rama','garu','peace','rest'}
keywords={'NTR','kalyan ram','lakshmi pranathi','nandamuri taraka rama rao'}
imp_terms=[term for term in important_terms if term not in unwanted]


imp_terms+=keywords
print(imp_terms)
knowledge_base = create_knowledge_base(imp_terms, scraped_directory)

with open('knowledge_base.pickle','wb') as f:
    pickle.dump(knowledge_base,f)

