import os

from pdf_processing.cleaning_pdfs.preprocessing_articles_text import remove_outliers
from pdf_processing.cleaning_pdfs.specific_cleaning_standard import clean_standard_articles
from pdf_processing.layout_analysis import layout_analysis
from tools.text_operations import save_text

if __name__ == '__main__':
    repertoire = input("Entrez le repertoire des fichiers: ")
    dossier_path = os.path.join(os.path.dirname(".."), repertoire)
    export_repertoire = "pdf_processing_output"
    for file_path in os.listdir(dossier_path):
        print("---Extracting text from %s ---" % file_path)
        fp = open(dossier_path+"/"+file_path, 'rb')

        ## 1)Layout Analysis (Analyse de la mise en page)
        pages_content_as_lines = layout_analysis(fp, as_list=True)

        ## saving in .txt file
        if (isinstance(pages_content_as_lines, list)):
            text_uncleaned = "".join(["".join(i) for i in pages_content_as_lines])
            save_text("pdf_processing_output/" + file_path[:-4] + "_reconstructed_butUncleaned.txt", text_uncleaned)
        #clean_standard_articles(pages_content_as_lines, config_per_page[1:])
        ### 2.a) clean standard articles (Nettoyage qui se base de la position du text dans la page), method: clean_standard_articles
        #### liste pour configurer l'algorithme pour enlever certains elements en se basant sur leurs position
        #### pattern [from index, [index, max length, regex]*n]
        config_per_page = [1, [0], ["last", 20]]
        lines_cleaned_specifically = clean_standard_articles(pages_content_as_lines, config_per_page)
        if(isinstance(lines_cleaned_specifically, list)):
            lines_cleaned_specifically = "".join(["".join(i) for i in lines_cleaned_specifically])
        #cleaning
        ### 2.b) removing outliers (enlever certaines chaine de caractere en se basant sur leurs contenu)
        text_cleaned = remove_outliers(lines_cleaned_specifically)
        save_text("pdf_processing_output/"+file_path[:-4] + "_cleaned.txt", text_cleaned)
