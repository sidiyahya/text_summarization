# I)First step : pdf_processing:
## 1)Layout Analysis (Analyse de la mise en page):
### 1.a) convert text from pdf (using pdfminer)
### 1.b) text reconstruction (ordonner les lignes du pdf) , method : order_pdfminer_text_page()

## 2) Cleaning:
### 2.a) clean standard articles (Nettoyage qui se base de la position du text dans la page), method: clean_standard_articles
### 2.b) removing outliers (enlever certaines chaine de caractere en se basant sur leurs contenu) : remove_outliers