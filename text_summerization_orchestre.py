import os.path

from export_text_as_pdf import export_text_as_pdf
from summerize_text_using_bert import summerize_text_using_bert, summerize_text_using_bert_heavy
from summerize_text_using_nltk import generate_summary
from summerize_text_using_spacy_light import summerize_text_spacy_light
from tools.text_operations import save_text


def run_algorithms(text):
    # print("\n")
    print("NLTK: ")
    summary_nltk = generate_summary(text, 30, 3)
    print(summary_nltk)
    print("\n")
    print("SpaCy: ")
    summary_spacy = "\n".join([i.text for i in summerize_text_spacy_light(text)])
    print(summary_spacy)
    print("SUMMARY BERT: ")
    summary_bert = summerize_text_using_bert_heavy(text)
    print(summary_bert)
    return summary_nltk, summary_spacy, summary_bert

    #algorithms_results = [["Nltk", summary_nltk], ["SpaCy", summary_spacy], ["summary_bert", summary_bert]]
    #export_text_as_pdf(algorithms_results)


if __name__ == '__main__':
    repertoire = input("Entrez le repertoire des fichiers: ")
    dossier_path = os.path.join(os.path.dirname("."), repertoire)
    export_repertoire = "summerized_text"
    for file_path in os.listdir(dossier_path):
        if(file_path.endswith(".txt")):
            with open(os.path.join(dossier_path, file_path), 'r') as f:
                text = f.read()
        summary_nltk, summary_spacy, summary_bert = run_algorithms(text)
        TEXT = "SUMMARY NTLK \n"+summary_nltk+"\n\n\n"+"SUMMARY SPACY \n"+"\n\n\n"+"SUMMARY BERT \n"+summary_bert+"\n\n"+"----------------FIN------------------"
        save_text(os.path.join(export_repertoire, file_path[:-4]+"_SUMMERIZED.txt"), TEXT)