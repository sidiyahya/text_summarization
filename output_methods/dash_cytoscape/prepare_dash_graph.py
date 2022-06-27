import pandas as pd

from output_methods.dash_cytoscape.reconstruct_data import reconstruct_data, add_x_y
from output_methods.sortie_graph import preprocessing


def prepare_dash_graph(list_summerized_text, metadatas):
    ###First STEP create data set of words relationship

    all_text = preprocessing(list_summerized_text)
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
    #Filtrer le nombre de mots selon l'ordre de pertinance
    links_filtered = links_filtered[0:500]

    ###Enrich the datasets with other data (article , author , cited_by_other_articles)
    df, metadatas = reconstruct_data(links_filtered, list_summerized_text, metadatas)
    df["n_cites"] = df["n_cites"].astype(int)

    #df_final = add_x_y(df, positions)
    return df, metadatas