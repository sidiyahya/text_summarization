from pdf_processing.read_files import read_text_file
from sortie_wordcloud import run_wordcloud
from summary_algorithms.text_summerization_orchestre import run_algorithms


def sortis_orchestre(text):
    #run_pdf(text)
    run_wordcloud(text)


if __name__ == '__main__':
    file = input("Entrez le chemin de votre fichier: ")
    text = read_text_file(file)
    summary_nltk, summary_spacy = run_algorithms(text)
    sortis_orchestre(summary_nltk)
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