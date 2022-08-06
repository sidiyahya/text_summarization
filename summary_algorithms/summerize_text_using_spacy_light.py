#%%
#Extractive approach to auto -summarize the article
#%%
#Step 1 - Install Spacy and Scikit-learn libraries
#%%
import spacy as spacy

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import CountVectorizer
import en_core_web_sm
nlp = en_core_web_sm.load()

def summerize_text_spacy_light(text):
    #%%
    doc = nlp(text)
    #%%
    # Step 3 -The next step is to remove the stop words and create a dictionary of words and their respective frequencies
    #%%
    corpus = [sent.text.lower() for sent in doc.sents]
    cv = CountVectorizer(stop_words=list(STOP_WORDS))
    cv_fit=cv.fit_transform(corpus)
    word_list = cv.get_feature_names()
    count_list = cv_fit.toarray().sum(axis=0)
    word_frequency = dict(zip(word_list,count_list))
    #%%
    # Step 4 -compute the relative frequency of each word - I am doing this to determing the relevance of sentences based on the
    # cumulative frequency of their words
    #%%
    val=sorted(word_frequency.values())
    higher_word_frequencies = [word for word,freq in word_frequency.items() if freq in val[-3:]]
    print("\nWords with higher frequencies: ", higher_word_frequencies)
    # gets relative frequency of words
    higher_frequency = val[-1]
    for word in word_frequency.keys():
        word_frequency[word] = (word_frequency[word]/higher_frequency)
    #%%
    # Step 5- Creating a ordered list (ascending order) of most important sentences
    #%%
    sentence_rank={}
    for sent in doc.sents:
        for word in sent :
            if word.text.lower() in word_frequency.keys():
                if sent in sentence_rank.keys():
                    sentence_rank[sent]+=word_frequency[word.text.lower()]
                else:
                    sentence_rank[sent]=word_frequency[word.text.lower()]
    top_sentences=(sorted(sentence_rank.values())[::-1])
    top_sent=top_sentences[:3]
    #%%
    # Step 6- Extracting the top 3 sentences
    #%%
    summary=[]
    for sent,strength in sentence_rank.items():
        if strength in top_sent:
            summary.append(sent)
        else:
            continue
    return summary


if __name__ == '__main__':
    with open("/home/mohamedali/PycharmProjects/text_summarization/pdf_processing/pdf_processing_output/abstract of abstracts.txt", "r", encoding="utf-8") as f:
        text = " ".join(f.readlines())

    summary = summerize_text_spacy_light(text)
    for i in summary:
        print(i,end="")
