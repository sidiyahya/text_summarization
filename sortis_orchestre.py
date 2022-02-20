from read_files import read_text_file
from sortie_pdf import run_pdf
from sortie_wordcloud import run_wordcloud
from text_summerization_orchestre import run_algorithms


def sortis_orchestre(text):
    #run_pdf(text)
    run_wordcloud(text)


if __name__ == '__main__':
    file = input("Entrez le chemin de votre fichier: ")
    text = read_text_file(file)
    summary_nltk, summary_spacy = run_algorithms(text)
    sortis_orchestre(summary_nltk)
