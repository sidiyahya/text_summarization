#Add citations
import copy
import json

import numpy as np
import pandas as pd


def add_x_y(df, positions):
    df["x"] = np.nan
    df["y"] = np.nan
    for index, row in df.iterrows():
        df.at[index, "x"] = positions[row['source']][0]
        df.at[index, "y"] = positions[row['source']][1]

    return df

def reconstruct_data(df, list_summerized_text, metadatas):
    metadatas_adapted = []
    tiles_indexes = []
    metadata_json = {
        'author': "",
        'title': "",
        'journal': "",
        'year': ""
    }
    for i in metadatas:
        metadata_adapted = copy.deepcopy(metadata_json)
        for j in i:
            for k in metadata_json:
                if(k in j):
                    metadata_adapted[k] = j.replace("=", "").strip()
        metadatas_adapted.append(metadata_adapted)

    titles = [[i[j].replace("title = ", "").strip()] for i, j in zip(metadatas, tiles_indexes)]
    data_reconstructed = {}
    for index, row in df.iterrows():
        source = row['source']
        target = row['target']
        weight = row['weight']
        if(source in data_reconstructed):
            data_reconstructed[source][0] += [target]
            data_reconstructed[source][1] += [weight]
        else:
            data_reconstructed.update({source: [[target], [weight]]})

    data_reconstructed_list = [[i] + list(j) for i, j in zip(tuple(data_reconstructed.keys()), tuple(data_reconstructed.values()))]
    df_reconstructed = pd.DataFrame(data=data_reconstructed_list, columns=['source', 'targets', 'weights'])
    df_reconstructed["n_cites"] = pd.Series(dtype='int')
    df_reconstructed["cited_by"] = ""
    df_reconstructed["author"] = ""
    df_reconstructed["journal"] = ""
    df_reconstructed["title"] = ""
    df_reconstructed["topic_id"] = ""
    df_reconstructed["cited_by_other_articles"] = ""

    for index, row in df_reconstructed.iterrows():
        targets = row['targets']
        targets_id = ""
        n_cites = 0
        for target in targets:
            if(df_reconstructed.index[df_reconstructed['source'] == target].tolist()):
                id = df_reconstructed.index[df_reconstructed['source'] == target].tolist()[0]
                targets_id += str(id) if(len(targets_id)==0) else ","+str(id)
                n_cites+=1

        df_reconstructed.at[index, "cited_by"] = targets_id
        df_reconstructed.at[index, "n_cites"] = int(n_cites)

    all_words = df_reconstructed['source'].tolist()
    ####################
    for metadata_i, summerized_text in zip(range(len(metadatas_adapted)), list_summerized_text):
        article_summerized_text = [i.strip() for i in summerized_text.split()]
        common_words = list(set(article_summerized_text).intersection(all_words))
        for common_word in common_words:
            index = df_reconstructed.index[df_reconstructed['source'] == common_word].to_list()[0]
            current_article_value = df_reconstructed.at[index, 'title']
            if(len(current_article_value)):
                df_reconstructed.at[index, "cited_by_other_articles"] += str(metadata_i)+","

            else:
                current_metadata = metadatas_adapted[metadata_i]
                for key in current_metadata:
                    df_reconstructed.at[index, key] = current_metadata[key].replace(key, "").replace("=", "").strip()
                df_reconstructed.at[index, 'topic_id'] = str(metadata_i)

    return df_reconstructed, metadatas_adapted



if __name__ == '__main__':
    links_filtered = pd.read_csv('links_filtered.csv')
    f = open('positions.json')
    positions = json.load(f)
    df = reconstruct_data(links_filtered)
    df["n_cites"] = df["n_cites"].astype(int)

    df_final = add_x_y(df, positions)
    df.to_csv('network_df.csv', encoding='utf-8', index=False)