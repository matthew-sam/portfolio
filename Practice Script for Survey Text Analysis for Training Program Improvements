import pandas as pd
import re
import nltk
from nltk.corpus import words
from nltk.corpus import stopwords 
from nltk.tokenize import TweetTokenizer
import csv
import spacy

# nltk.download('words')
# nltk.download('punkt')
# nltk.download('stopwords')

# Get the list of English words from NLTK
english_words = set(words.words())

# Remove words less than 3 letters
english_words = {word for word in english_words if len(word) >= 3}

# Add a set of additional words
additional_words = {"software", "Sandra", "Ziebel", "Jon", "Scarpa", "Jennifer", "Perez", "Patrick", "Trujillo", "Eddie", "Gonzales", "Mat", "Dove", "Elias", 
                    "a", "I", "an", "as", "at", "be", "by", "do", "go", "if", "in", "is", "it", "me", "my", "no", "of", "on", "or", "so", "to", "up", "us"}
english_words.update(additional_words)


# Remove words from the dictionary
words_to_remove = {"rick", "scarp", "gers", "ers", "king", "chang", "ked", "ted"}  

for word in words_to_remove:
   english_words.discard(word)

# Load the spaCy English language model
nlp = spacy.load("en_core_web_sm")

# Function to split concatenated words carefully, retaining contractions
def split_concatenated_word_carefully(word, word_list):
    # Helper function to check if a word is in the English word list
    def is_valid_word(w):
        return w.lower() in word_list

    # Check if the word is a contraction with an apostrophe
    if "'" in word and word.lower() not in word_list:
        return word, ''

    # Split the word only if it has a minimum length of 6 characters
    if len(word) >= 6:
        # Iterate through possible splits
        for i in range(1, len(word)):
            left_subword = word[:i]
            right_subword = word[i:]

            if is_valid_word(left_subword) and is_valid_word(right_subword):
                return left_subword, right_subword

    # If no valid split is found or the word is too short, return the original word
    return word, ''

# Function to correct a sentence
def correct_sentence(sentence, word_list):
    words = sentence.split()
    corrected_words = []

    for word in words:
        if word.lower() not in word_list:
            # Attempt to split the word into valid subwords
            left_part, right_part = split_concatenated_word_carefully(word, word_list)
            
            if right_part:
                # If a valid split is found, add both subwords
                corrected_words.extend([left_part, right_part])
            else:
                # If no valid split is found, add the original word
                corrected_words.append(left_part)
        else:
            # If the word is already valid, add it as is
            corrected_words.append(word)

    # Reconstruct the corrected sentence
    corrected_sentence = ' '.join(corrected_words)
    return corrected_sentence

# Function to lemmatize a list of words using spaCy
def lemmatize_words(word_list):
    lemmatized_words = []
    for word in word_list:
        # Customize lemmatization for "i'm" 
        if word.lower() == "i'm":
            lemmatized_word = "i am"
        else:
            doc = nlp(word)
            lemmatized_tokens = [token.lemma_ for token in doc]
            lemmatized_word = " ".join(lemmatized_tokens)
                
        lemmatized_words.append(lemmatized_word)

    return lemmatized_words

# Function to remove punctuation marks
def clean_text(text):
    if isinstance(text, str):
        # Use a regular expression to remove characters that are not letters, numbers, single quotes ('), or specific punctuation marks
        cleaned_text = re.sub(r"[^a-zA-Z0-9' ]", '', text)
        return cleaned_text
    else:
        return str(text)  # Convert non-string values to strings

# Function to process phrases and remove stopwords while also lemmatizing
def process_phrases(phrases, word_list):
    # Load NLTK's English stopwords
    stop_words = set(stopwords.words("english"))

    # Words you want to remove from the stop_words set
    words_to_remove = {"no", "not", "sub", "very"}

    # Remove the specified words from the stop_words set
    stop_words.difference_update(words_to_remove)

    # Initialize the TweetTokenizer
    tokenizer = TweetTokenizer()

    # Initialize a list to store the filtered phrases
    filtered_phrases = []

    for phrase in phrases:
        # Clean the phrase by removing unwanted characters
        cleaned_phrase = clean_text(phrase)

        # Correct the phrase using the correct_sentence function
        corrected_phrase = correct_sentence(cleaned_phrase, word_list)

        # Tokenize the corrected phrase using TweetTokenizer
        tokens = tokenizer.tokenize(corrected_phrase)

        # Lemmatize the tokens
        lemmatized_tokens = lemmatize_words(tokens)

        # Remove stopwords
        filtered_tokens = [word for word in lemmatized_tokens if word.lower() not in stop_words]

        # Join the filtered tokens back into a phrase
        filtered_phrase = " ".join(filtered_tokens)
        
        while True:
            if " ing" in filtered_phrase:
                # Get the index of " ing" in the filtered_phrase
                index = filtered_phrase.find(" ing")
                # Check if the next character after " ing" is not a letter
                if index + 3 >= len(filtered_phrase) or not filtered_phrase[index + 3].isspace():
                    filtered_phrase = filtered_phrase.replace(" ing", "")
                else:
                    break
            elif " es" in filtered_phrase:
                # Get the index of " es" in the filtered_phrase
                index = filtered_phrase.find(" es")
                # Check if the next character after " es" is not a letter
                if index + 3 >= len(filtered_phrase) or not filtered_phrase[index + 3].isspace():
                    filtered_phrase = filtered_phrase.replace(" es", "")
                else:
                    break
            elif "'s" in filtered_phrase:
                filtered_phrase = filtered_phrase.replace("'s", "")
            elif "'ve" in filtered_phrase:
                filtered_phrase = filtered_phrase.replace("'ve", "")
            else:
                break  # Exit the loop if no more replacements are needed

        # Add the filtered phrase to the list
        filtered_phrases.append(filtered_phrase)

    return filtered_phrases

# Define a custom tokenization function
def custom_tokenize(text):
    if isinstance(text, str):
        # Tokenize by splitting at white spaces
        tokens = text.split()
        return tokens
    else:
        return []  # Return an empty list for non-string data

# Example inputs
inputs = ["let's go to thepark asking rabies i'd", "i'm walking into the wall", "the shogws must go on", "soft@ware input isgreat for ERP I was running and walked", 
          "as he train's result's processes", "jumping jumped jumps leader teacher trainer happily would've couldn't", "managers Patrick Sandra Scarpa chang changes",
          "I do. Some information changes as tickets go in for so many problems we are having with SAGE. Because of that it is hard to follow all of the changes and retain them because they are constantly changing.",
          "allotted started lacked created wanted assisted"]

# Process the phrases and print the filtered results
filtered_results = process_phrases(inputs, english_words)

# Tokenize the filtered results using custom_tokenize
finalized_tokens = [custom_tokenize(filtered_phrase) for filtered_phrase in filtered_results]

for filtered_phrase in filtered_results:
    print(filtered_phrase)

for tokens in finalized_tokens:
    print(tokens)




