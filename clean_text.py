import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.stem import WordNetLemmatizer
import string


def clean_text_files(input_dir, output_dir):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    for file_name in os.listdir(input_dir):
        if file_name.endswith('.txt'):
            with open(os.path.join(input_dir, file_name), 'r', encoding='utf-8') as f:
                text = f.read().lower()  # Read the text from the file and convert to lowercase
                # Tokenize the text
                tokens = word_tokenize(text)
                # Remove punctuation and stop words, and lemmatize tokens
                tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in string.punctuation and token not in stop_words]
                cleaned_text = '  '.join(tokens)  # Join the cleaned tokens back into a string

                # Write the cleaned text to an output file
                output_file = os.path.join(output_dir, file_name)
                with open(output_file, 'w',encoding='utf-8') as f_out:
                    f_out.write(cleaned_text)


# Create a directory to store cleaned text files
cleaned_dir = 'cleaned_texts_NTR'
if not os.path.exists(cleaned_dir):
    os.makedirs(cleaned_dir)
input_dir='scraped_texts_NTR'

# Clean text files
clean_text_files(input_dir, cleaned_dir)
print("Text files cleaned successfully.")


