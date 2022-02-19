# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 19:30:03 2021

@author: Marouane
"""

import glob
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import re
import requests
import nltk
import heapq
import pandas as pd

nltk.download('stopwords')
nltk.download('wordnet')

lien='' # On définie le dossier où se trouve les articles
mylist = [f for f in glob.glob(lien+"Articles/*.pdf")] # On detecte tous les fichiers en .pdf

####################
# Extraction du texte
####################

def convert_pdf_to_txt_and_metadata(path):
    
    ## Parametrage de la librairie pdfminer pour transformer le pdf en text et l'enregistre dans une variable
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    #device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    ## Le code qui suit sert à récuperer toutes les pages pour les enregistrer dans un text complet
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    text = retstr.getvalue() # On enregistre le text du pdf en variable text
    fp.close() # On ferme le pdf
    device.close()
    retstr.close()
    ## Fin du paramétrage
    
    ## On récupère les doi en cherchant le lien doi.org suivit d'un code de 10 caractères
    doi_re = re.compile("doi.org/10.(\d)+/([^(\s\>\"\<)])+")
    m = doi_re.search(text)
    try:
        ## On teste la première méthode si cela ne fonctionne pas on passe à d'autres méthodes
        metadata=m.group(0)
    except:
        doi_re = re.compile("10.(\d)+=([^(\s\>\"\<)])+")
        m = doi_re.search(text)
        try:
            metadata= m.group(0)
            metadata = metadata.replace("=","/")
        except:
            doi_re = re.compile("10.(\d)+/([^(\s\>\"\<)])+")
            m = doi_re.search(text)
            metadata= m.group(0)
    metadata = metadata.replace("doi.org/","")
        
    return text, metadata # On retourne les deux variables qui contiennent le texte + DOI

def fonctionresume():
    pdfs=[] # On initialise une liste qui va contenir les textes des fichiers pdf
    metadatas=[] # On initialise une liste qui va contenir les DOI
    
    ## Cette boucle va lancer la première fonction pour récuperer les textes et DOI
    for i in mylist:
        pdf, metadata=convert_pdf_to_txt_and_metadata(i)
        metadatas.append(metadata)
        pdfs.append(pdf)

    pdfs2=[]    # On initialise une liste qui va contenir le texte restructuré 
                # cette étape sert à recoller les phrase

    for i in pdfs:
        txt = i.split("\n") # On split le texte avec tous les retours chariot pour le transformer en liste
        f=""
        
        ## Cette boucle sert à reconstituer les phrases, on recolle toutes les varriables de la liste
        ## Quand on trouve une ponctuation suivie d'un retour chariot, dans ce cas on met un retour chariot dans le texte
        ## Sinon on continuer à coller les variables pour recoller les textes séparés lors de l'extraction
        for i in range(0,len(txt)):
            if len(txt[i])==0:
                txt[i]="\n"
            if txt[i][-1]=="." or txt[i][-1]=="?" or txt[i][-1]=="!" or txt[i][-1]==":" or txt[i][0].isupper()==True:
                f=str(f+"\n"+txt[i])
            else:
                f=str(f+txt[i])
        pdfs2.append(f)
    
    
    ## Dans cette partie on récupère les paragraphes methods et results
    ll1=[] # On initialise la première liste qui va contenir les paragraphes Methods
    ll2=[] # On initialise la deuxième liste qui va contenir les paragraphes Results
    
    ## Cette boucle parcours tous les textes nettoyés et restructurés des pdfs
    for i in pdfs2:   
        text = i
        ## On cherche tous les titres qui contiennent methods et results
        l1=text[text.lower().find("\nmethods\n"):text.lower().find("\nresults\n")]
        if l1=="":
            ## Des fois les articles mettent materials and methods donc on tente une deuxieme fois
            l1=text[text.lower().find("\nmaterials and methods\n"):text.lower().find("\nresults\n")]
        l2=text[text.lower().find("\nresults\n"):text.lower().find("\nconclusion\n")]
        ll1.append(l1)
        ll2.append(l2)
        
    ## Cette fonction sert à communiquer avec l'API pour récuperer les métadatas avec les DOI qu'on a récuperer    
    def doi2bib(doi):
      url = "http://dx.doi.org/" + doi
    
      headers = {"accept": "application/x-bibtex"}
      r = requests.get(url, headers = headers)
    
      return r.text
    
    ## On nettoie ce que l'API nous a retourné pour enlever les {} et autres
    for i in range(0,len(metadatas)):
        l=doi2bib(metadatas[i])
        l=l.replace("	","")
        l=l.replace("{","")
        l=l.replace("}","")
        l=l.split(",\n")
        metadatas[i]=l
       
    ## On retourne les textes pdfs, les paragraphes Methods et paragraphes Results ainsi que les métadatas
    return pdfs2, ll1, ll2, metadatas

PDFs, Methods, Results, Methadatas = fonctionresume()
    
############################
# Résumer du texte
############################

def summarize():
    summethods = []
    for i in Methods:
        
        ## On nettoie le texte des reférences et chiffres
        article_text = i
        article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
        article_text = re.sub(r'\s+', ' ', article_text)
        
        # Removing special characters and digits
        formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
        formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
        
        ## à l'aide de la fonction sent_tokenize on transforme les paragraphes Methods et Results en phrases
        sentence_list = nltk.sent_tokenize(article_text)
        
        ## On retire les stopwords
        stopwords = nltk.corpus.stopwords.words('english')
        
        ## On calcul le score de chaque phrase en transformant les phrases en mots et calculer le poids des mots dans la phrase
        word_frequencies = {}
        for word in nltk.word_tokenize(formatted_article_text):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1
                    
        maximum_frequncy = max(word_frequencies.values())
        
        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
        
        ## Une fois on a le poids des mots on calcule le score de chaque phrase
        sentence_scores = {}
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]
                            
        # On prend les 7 phrases les mieux notées pour construire notre résumé                   
        summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
        
        # On colle les 7 phrases pour construire un texte résumé de notre entrée
        summary = ' '.join(summary_sentences)
        summethods.append(summary)
        
    ## On refait la même chose pour les paragraphes Results
    sumresults = []
    for i in Results:
        article_text = i
        article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
        article_text = re.sub(r'\s+', ' ', article_text)
        
        formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
        formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
        
        
        sentence_list = nltk.sent_tokenize(article_text)
        
        stopwords = nltk.corpus.stopwords.words('english')
        
        word_frequencies = {}
        for word in nltk.word_tokenize(formatted_article_text):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1
                    
        maximum_frequncy = max(word_frequencies.values())
        
        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
            
        sentence_scores = {}
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]
                            
                            
        summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
        
        summary = ' '.join(summary_sentences)
        sumresults.append(summary)
    
    ## On retourne les deux listes constituées de résumé Methods et Results
    return summethods, sumresults

ResumeMethods, ResumeResults = summarize()

## Si on souhaite enregistrer les résultats sous format tableau excel
'''
import pandas as pd

Methadataframe = pd.DataFrame(Methadatas)
Methadataframe.columns = ["Alias","DOI","URL","Year","Month","Publisher","Volume","Number","Pages","Author","Title","Journal"]
Datas = pd.DataFrame(zip(mylist,ResumeMethods,ResumeResults))
Datas.columns = ["Link","Methods","Results"]
Datas=Datas.join(Methadataframe)
Datas.to_excel(str(lien+"output.xlsx"))
'''


## Nuage de mots

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

t1=" ".join(ResumeMethods)
t2=" ".join(ResumeResults)
tf=str(t1+t2)

### Création du nuage de mot
def nuage():
        words = nltk.word_tokenize(tf) # On tokenise tous les mots
        stops = set(stopwords.words('english')) # On enlève les stopwords
        wordsFiltered = []
        
        ## Boucle qui sert à récuperer que les mots qui contiennent plus de 2 caractères
        for w in words:
            if w not in stops:
                if len(w)>2:
                    if w.isalpha()==True:
                        wordsFiltered.append(w)           
          
        lemmatizer = WordNetLemmatizer() # On lemmatise les mots
        
        for w in range(0,len(wordsFiltered)):
            wordsFiltered[w]=lemmatizer.lemmatize(wordsFiltered[w])
        
        text = " ".join(wordsFiltered)
        wordcloud = WordCloud(background_color = 'white', stopwords = stops, max_words = 50,width=1600, height=800).generate(text)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.savefig(str(lien+'nuagearticles.png'),dpi=1500) # Extraction du nuage de mot
        
nuage()


####################
# Création du graph neural
####################

tf = " ".join(PDFs)
tf = tf.replace("barriers","barrier")
all_text = tf.split(".")

def preprocessing(corpus):
    ## On prépare le texte pour la matrice de cooccurrence
    clean_text = []
    for row in corpus:
        # on tokenise le texte
        tokens = nltk.tokenize.word_tokenize(row)
        # on le transforme en miniscule
        tokens = [token.lower() for token in tokens]
        # on récupère que les variables alpha (texte)
        tokens = [token for token in tokens if token.isalpha()]
        clean_sentence = ''
        clean_sentence = ' '.join(token for token in tokens)
        clean_text.append(clean_sentence)
    return clean_text
    
all_text = preprocessing(all_text)

# sklearn countvectorizer
from sklearn.feature_extraction.text import CountVectorizer
# Convert a collection of text documents to a matrix of token counts
cv = CountVectorizer(ngram_range=(1,1), stop_words = 'english')
# matrix of token counts
X = cv.fit_transform(all_text)
Xc = (X.T * X) # matrix manipulation
Xc.setdiag(0) # set the diagonals to be zeroes as it's pointless to be 1

## On transforme la matrice en tableau à 3 colonnes, source, target et poids
names = cv.get_feature_names() # This are the entity names (i.e. keywords)
df = pd.DataFrame(data = Xc.toarray(), columns = names, index = names)

###################
# Creation du graph
###################

import networkx as nx
from fa2 import ForceAtlas2
import numpy as np


v = df
#set 0 to lower triangular matrix
v.values[np.tril(np.ones(v.shape)).astype(np.bool)] = 0

#reshape and filter only count > 0
a = v.stack()
a = a[a >= 1].rename_axis(('source', 'target')).reset_index(name='weight')
a=a.sort_values(by = 'weight',ascending = False)
a=a.reset_index(drop=True)

links_filtered=a.loc[(a['source'] != a['target']) ]
links_filtered=links_filtered[0:200]

G = nx.from_pandas_edgelist(links_filtered,  edge_attr=True)

## On configure le modèle ForceAtlas 2
forceatlas2 = ForceAtlas2(
                        # Behavior alternatives
                        outboundAttractionDistribution=True,  # Dissuade hubs
                        linLogMode=False,  # NOT IMPLEMENTED
                        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
                        edgeWeightInfluence=1.0,

                        # Performance
                        jitterTolerance=1.0,  # Tolerance
                        barnesHutOptimize=True,
                        barnesHutTheta=1.2,
                        multiThreaded=False,  # NOT IMPLEMENTED

                        # Tuning
                        scalingRatio=2.0,
                        strongGravityMode=False,
                        gravity=1.0,

                        # Log
                        verbose=True)

## On met 2000 itérations pour stabiliser les positions des noeuds
positions = forceatlas2.forceatlas2_networkx_layout(G, pos=None, iterations=2000)

#################

import plotly.graph_objects as go

## On construit les liens entre les noeuds en récupérant les positions X et Y des noeuds source et target
edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = positions[edge[0]]
    x1, y1 = positions[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

## On trace les liens
edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

## On rajoute les noeuds dans le graphique en récupérant les positions des noeuds X et Y
node_x = []
node_y = []
for node in G.nodes():
    x, y = positions[node]
    node_x.append(x)
    node_y.append(y)

## On trace les noeuds
node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line_width=2))

node_adjacencies = []
node_text = []
for node, adjacencies in enumerate(G.adjacency()):
    node_adjacencies.append(len(adjacencies[1]))
    #node_text.append('# of connections: '+str(len(adjacencies[1])))

## On rajoute les textes sur les noeuds pour voir le mot lié à chaque noeud
for node in G.nodes():
    node_text.append(str(node))

node_trace.marker.color = node_adjacencies
node_trace.text = node_text

fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                #title='<br>Network graph made with Python',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
## On rajoute les textes sur les noeuds
for i in G.nodes():
    fig.add_annotation(dict(font=dict(color='rgba(0,0,200,0.8)',size=12),
                                        x=positions[i][0],
                                        y=positions[i][1],
                                        showarrow=False,
                                        text=i,
                                        textangle=0,
                                        xanchor='left',
                                        xref="x",
                                        yref="y"))
## On affiche le graphiques
fig.show()
