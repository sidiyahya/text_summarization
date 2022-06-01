####################
# Création du graph neural
####################
import nltk
import pandas as pd
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop
from spacy.lang.en.stop_words import STOP_WORDS as en_stop


def preprocessing(corpus):
    ## On prépare le texte pour la matrice de cooccurrence
    clean_text = []
    final_stopwords_list = list(fr_stop) + list(en_stop)
    for row in corpus:
        if(row in final_stopwords_list):
            continue
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


def create_graph(summerized_text_and_all_text):

    all_text = preprocessing(summerized_text_and_all_text)
    all_text = [i for i in all_text if(len(i)>3)]
    # sklearn countvectorizer
    from sklearn.feature_extraction.text import CountVectorizer

    # Convert a collection of text documents to a matrix of token counts
    cv = CountVectorizer(ngram_range=(1, 1), stop_words='english')
    # matrix of token counts
    X = cv.fit_transform(all_text)
    Xc = (X.T * X)  # matrix manipulation
    Xc.setdiag(0)  # set the diagonals to be zeroes as it's pointless to be 1

    ## On transforme la matrice en tableau à 3 colonnes, source, target et poids
    names = cv.get_feature_names()  # This are the entity names (i.e. keywords)
    df = pd.DataFrame(data=Xc.toarray(), columns=names, index=names)

    ###################
    # Creation du graph
    ###################

    import networkx as nx
    from fa2 import ForceAtlas2
    import numpy as np

    v = df
    # set 0 to lower triangular matrix
    v.values[np.tril(np.ones(v.shape)).astype(np.bool)] = 0

    # reshape and filter only count > 0
    a = v.stack()
    a = a[a >= 1].rename_axis(('source', 'target')).reset_index(name='weight')
    a = a.sort_values(by='weight', ascending=False)
    a = a.reset_index(drop=True)

    links_filtered = a.loc[(a['source'] != a['target'])]
    links_filtered = links_filtered[0:200]

    G = nx.from_pandas_edgelist(links_filtered, edge_attr=True)

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
        # node_text.append('# of connections: '+str(len(adjacencies[1])))

    ## On rajoute les textes sur les noeuds pour voir le mot lié à chaque noeud
    for node in G.nodes():
        node_text.append(str(node))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        # title='<br>Network graph made with Python',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    ## On rajoute les textes sur les noeuds
    for i in G.nodes():
        fig.add_annotation(dict(font=dict(color='rgba(0,0,200,0.8)', size=12),
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