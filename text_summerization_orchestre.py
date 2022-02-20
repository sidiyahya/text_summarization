
from export_text_as_pdf import export_text_as_pdf
from summerize_text_using_bert import summerize_text_using_bert, summerize_text_using_bert_heavy
from summerize_text_using_nltk import generate_summary
from summerize_text_using_spacy_light import summerize_text_spacy_light

def run_algorithms(text):
    # print("SUMMARY BERT: ")
    # summary_bert = summerize_text_using_bert_heavy(text)
    # print(summary_bert)
    # print("\n")
    print("NLTK: ")
    summary_nltk = generate_summary(text, 30, 3)
    print(summary_nltk)
    print("\n")
    print("SpaCy: ")
    summary_spacy = "\n".join([i.text for i in summerize_text_spacy_light(text)])
    print(summary_spacy)
    return summary_nltk, summary_spacy

    #algorithms_results = [["Nltk", summary_nltk], ["SpaCy", summary_spacy], ["summary_bert", summary_bert]]
    #export_text_as_pdf(algorithms_results)


if __name__ == '__main__':
    file = input("Entrez le chemin de votre fichier: ")
    with open(file, 'r') as f:
        text = f.read()
    print("\n")
    summary_nltk, summary_spacy = run_algorithms(text)