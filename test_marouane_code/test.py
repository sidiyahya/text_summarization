## Si on souhaite enregistrer les résultats sous format tableau excel
'''
import pandas as pd

Methadataframe = pd.DataFrame(Methadatas)
Methadataframe.columns = ["Alias","DOI","URL","Year","Month","Publisher","Volume","Number","Pages","Author","Title","Journal"]
Datas = pd.DataFrame(zip(mylist,ResumeMethods,ResumeResults))
Datas.columns = ["Link","Methods","Results"]
Datas=Datas.join(Methadataframe)
Datas.to_excel(str(lien+"output.xlsx"))
'''

## Nuage de mots
import os

import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from test_marouane_code.output_graph import create_graph

lien = ''

### Création du nuage de mot
def nuage(tf):
    words = nltk.word_tokenize(tf)  # On tokenise tous les mots
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
    plt.savefig(str(lien + 'nuagearticles.png'), dpi=1500)  # Extraction du nuage de mot

if __name__ == '__main__':
    repertoire = input("Entrez le repertoire des fichiers: ")
    dossier_path = os.path.join(os.path.dirname(".."), repertoire)
    for file_path in os.listdir(dossier_path):
        with open(os.path.join(dossier_path, file_path), 'r') as f:
            text = f.read()
        ### Création du nuage de mot
        create_graph(text.split("\n"))
        nuage(text)
        ####################
        # Création du graph neural
        ####################
        create_graph(text.split("\n"))