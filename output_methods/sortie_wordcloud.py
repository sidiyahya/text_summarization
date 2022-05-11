import matplotlib.pyplot as plt
from wordcloud import WordCloud

from pdf_processing.read_files import read_text_file

def run_wordcloud(text):
    wc = WordCloud()
    wc.generate(text)

    wc.to_file('output.png')
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()


### Création du nuage de mot
def nuage():
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
    file = input("Entrez le chemin de votre fichier: ")
    text = read_text_file(file)
    run_wordcloud(text)

