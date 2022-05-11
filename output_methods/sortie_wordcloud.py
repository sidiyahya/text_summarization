import os

import matplotlib.pyplot as plt
import nltk
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from wordcloud import WordCloud

### Création du nuage de mot
def nuage(text):
    words = nltk.word_tokenize(text)  # On tokenise tous les mots
    stops = set(stopwords.words('english'))  # On enlève les stopwords
    wordsFiltered = []

    ## Boucle qui sert à récuperer que les mots qui contiennent plus de 2 caractères
    for w in words:
        if w not in stops:
            if len(w) > 2:
                if w.isalpha() == True:
                    wordsFiltered.append(w)

    lemmatizer = WordNetLemmatizer()  # On lemmatise les mots

    for w in range(0, len(wordsFiltered)):
        wordsFiltered[w] = lemmatizer.lemmatize(wordsFiltered[w])

    text = " ".join(wordsFiltered)
    wordcloud = WordCloud(background_color='white', stopwords=stops, max_words=50, width=1600, height=800).generate(
        text)
    plt.imshow(wordcloud)
    plt.axis("off")

    plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output_images/nuagearticles.png'), dpi=1500)  # Extraction du nuage de mot
