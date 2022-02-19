# Natural Language Tool Kit (NLTK)
import nltk
nltk.download('stopwords')
nltk.download('punkt')

# Regular Expression for text preprocessing
import re

# Heap (priority) queue algorithm to get the top sentences
import heapq

# NumPy for numerical computing
import numpy as np

# pandas for creating DataFrames
import pandas as pd

# matplotlib for plot
from matplotlib import pyplot as plt


def plot_top_words(word_count_dict, show_top_n=20):
    """
    Plot top words

    INPUT:
    word_count_dict - dict. word count housed in a dictionary
    show_top_n - int. top n words to display (default 20)

    OUTPUT:
    Plot with top n words

    """
    word_count_table = pd.DataFrame.from_dict(word_count_dict, orient='index').rename(columns={0: 'score'})
    word_count_table.sort_values(by='score').tail(show_top_n).plot(kind='barh', figsize=(10, 10))
    plt.show()

def summerize_text_nltk(text):
    text = re.sub(r'\[[0-9]*\]', ' ', text)  # replace reference number i.e. [1], [10], [20] with empty space, if any..
    text = re.sub(r'\s+', ' ', text)  # replace one or more spaces with single space
    print(text)

    # generate clean text
    clean_text = text.lower()  # convert all uppercase characters into lowercase characters

    # replace characters other than [a-zA-Z0-9], digits & one or more spaces with single space
    regex_patterns = [r'\W', r'\d', r'\s+']
    for regex in regex_patterns:
        clean_text = re.sub(regex, ' ', clean_text)

    print(clean_text)

    # split (tokenize) the sentences
    sentences = nltk.sent_tokenize(text)
    print(sentences)
    # %% md
    ## Remove stop words
    # get stop words list
    stop_words = nltk.corpus.stopwords.words('english')
    print(stop_words)
    # %% md
    ## Build word histogram
    # %% md
    # create an empty dictionary to house the word count
    word_count = {}

    # loop through tokenized words, remove stop words and save word count to dictionary
    for word in nltk.word_tokenize(clean_text):
        # remove stop words
        if word not in stop_words:
            # save word count to dictionary
            if word not in word_count.keys():
                word_count[word] = 1
            else:
                word_count[word] += 1

    plot_top_words(word_count, 20)

    return word_count, sentences



def summerize_text_using_nltk(word_count, sentences):
    # create empty dictionary to house sentence score
    sentence_score = {}

    # loop through tokenized sentence, only take sentences that have less than 30 words, then add word score to form sentence score
    for sentence in sentences:
        # check if word in sentence is in word_count dictionary
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word_count.keys():
                # only take sentence that has less than 30 words
                if len(sentence.split(' ')) < 30:
                    # add word score to sentence score
                    if sentence not in sentence_score.keys():
                        sentence_score[sentence] = word_count[word]
                    else:
                        sentence_score[sentence] += word_count[word]

    df_sentence_score = pd.DataFrame.from_dict(sentence_score, orient='index').rename(columns={0: 'score'})
    df_sentence_score.sort_values(by='score', ascending=False)

    # %%
    # get the best 3 sentences for summary
    best_sentences = heapq.nlargest(3, sentence_score, key=sentence_score.get)

    return best_sentences

if __name__ == "__main__":
    with open('../text_articles/mahfoudh article.txt', 'r') as f:
        file_data = f.read()

    word_count, sentences = summerize_text_nltk(file_data)
    print('SUMMARY')
    print('------------------------')
    best_sentences = summerize_text_using_nltk(word_count, sentences)
    # display top sentences based on their sentence sequence in the original text
    for sentence in sentences:
        if sentence in best_sentences:
            print(sentence)