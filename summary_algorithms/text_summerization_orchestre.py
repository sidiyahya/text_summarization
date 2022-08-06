import os.path

#from summary_algorithms.summerize_text_using_bert import summerize_text_using_bert_heavy
#from summary_algorithms.summerize_text_using_nltk import generate_summary
from summary_algorithms.summerize_text_using_spacy_light import summerize_text_spacy_light
from tools.text_operations import save_text


def run_algorithms(text):
    # print("\n")
    print("NLTK: ")
    summary_nltk = generate_summary(text, 30, 3)
    print(summary_nltk)
    print("\n")
    print("SpaCy: ")
    print("summary_nltk ")
    summary_spacy = "\n".join([i.text for i in summerize_text_spacy_light(text)])
    print(summary_spacy)


    print("SUMMARY BERT: ")
    summary_bert = summerize_text_using_bert_heavy(text)
    print(summary_bert)
    return summary_spacy

    #algorithms_results = [["Nltk", summary_nltk], ["SpaCy", summary_spacy], ["summary_bert", summary_bert]]
    #export_text_as_pdf(algorithms_results)


if __name__ == '__main__':
    repertoire = input("Entrez le repertoire des fichiers: ")
    dossier_path = os.path.join(os.path.dirname(".."), repertoire)
    export_repertoire = "summerized_text"
    all_texts = ""
    for file_path in os.listdir(dossier_path):
        if(file_path.endswith("_cleaned.txt")):
            with open(os.path.join(dossier_path, file_path), 'r') as f:
                text = f.read()
                all_texts+="\n"+text
    summary_spacy= run_algorithms(all_texts)
    TEXT = "SUMMARY SPACY \n"+"\n\n\n"+summary_spacy+"\n\n"+"----------------FIN------------------"
    #TEXT = "SUMMARY NTLK \n"+summary_nltk+"\n\n\n"+"SUMMARY SPACY \n"+"\n\n\n"+"SUMMARY BERT \n"+summary_bert+"\n\n"+"----------------FIN------------------"
    save_text(os.path.join(os.path.dirname(os.path.realpath(__file__))+"/"+export_repertoire, "all_articles_SUMMERIZED.txt"), TEXT)