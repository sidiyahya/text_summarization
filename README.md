# Text Summerization

## Pipeline du projet:

I) Les entres : 
a) Importation des articles pdfs via le chemin de fichier
b) Extration de texte en utilisant la librairie PDFMINER
c) Transformer/Corriger les defauts de representation du texte 
d) Nettoyer le text pour enlever les bruits (texte non pertinent) : 2 methodes soit generique ou par type de fichier
e) Une methode generique pour enlever le bruit commmun ou courant ou facile a identifier en utilisant le ML et/ou PR
f) Une methode specifique pour enlever le bruit par type d'article :
ff) Une methode pour identifier le type de l'articles (quelles sont les informations qui permettent d'identifier un type d'article) : ML ou PR
fff) La mathode qui enleve le bruit par type d'article

II) Les algorithmes :
a) NLTK
b) Spacy
c) Bert
d) un preprocessing de la sortie de chaque algorithme

II) les sorties :
a) Sortie PDF
b) Sortie CSV
c) Sortie wordcloud
e) Graphe de liaison
f) ... Autre type de sortie