# I)First step : pdf_processing:
#=> Entre : PDF , le chemin des pdfs

## 1)Layout Analysis (Analyse de la mise en page):
### 1.a) convert text from pdf (using pdfminer)
### 1.b) text reconstruction (ordonner les lignes du pdf) , method : order_pdfminer_text_page()

## 2) Cleaning:
### 2.a) clean standard articles (Nettoyage qui se base de la position du text dans la page), method: clean_standard_articles
### 2.b) removing outliers (enlever certaines chaine de caractere en se basant sur leurs contenu) : remove_outliers

#<= Sortie : Variable qui contient le texte/une liste de textes par pdf

# II)Second Step: summary
#=> Entre : un texte nettoye
## 1) Run summary algorithms on text (nltk, spacy, bert)

#<= Sortie : Un texte resume

# III) Third Step: Output
#=> Entre : Un texte resume
## 1) wordcloud
## 2) graphe
## 3) pdf
## 4) .txt
## 5) csv

#<= Sortie : les sortis (wordcloud, graphe, csv, pdf, .txt)

import os

from output_methods.dash_cytoscape.prepare_dash_graph import create_dash_graph
from output_methods.sortie_graph import create_graph
from output_methods.sortie_wordcloud import nuage
from pdf_processing.cleaning_pdfs.preprocessing_articles_text import remove_outliers
from pdf_processing.cleaning_pdfs.specific_cleaning_standard import clean_standard_articles
from pdf_processing.layout_analysis import layout_analysis
from summary_algorithms.text_summerization_orchestre import run_algorithms

if __name__ == '__main__':
    repertoire = input("Entrez le repertoire des fichiers: ")
    dossier_path = os.path.join(os.path.dirname(".."), repertoire)
    export_repertoire = "pdf_processing_output"
    for file_path in os.listdir(dossier_path):
        print("---Extracting text from %s ---" % file_path)
        fp = open(dossier_path+"/"+file_path, 'rb')

        # I)First step : pdf_processing
        ## Layout Analysis
        pages_content_as_lines = layout_analysis(fp, as_list=True)
        ### 2.a) clean standard articles
        config_per_page = [1, [0], ["last", 20]]
        lines_cleaned_specifically = clean_standard_articles(pages_content_as_lines, config_per_page)
        if (isinstance(lines_cleaned_specifically, list)):
            lines_cleaned_specifically = "".join(["".join(i) for i in lines_cleaned_specifically])
        ### 2.b) removing outliers
        text_cleaned = remove_outliers(lines_cleaned_specifically)

        # II)Second Step: summary
        #summary_nltk, summary_spacy, summary_bert = run_algorithms(text_cleaned)
        summary_spacy = run_algorithms(text_cleaned)
        summary = [summary_spacy]

        # III) Third Step: Output
        for summerized_text in summary:
            if(len(summerized_text)!=0):
                ## Wordcloud
                ### Création du nuage de mot
                nuage(text_cleaned)
                ####################
                # Création du graph neural
                ####################
                create_graph(text_cleaned.split("\n"))

        ## 3) Dash cytoscape
        create_dash_graph(summary[1].split("\n"))