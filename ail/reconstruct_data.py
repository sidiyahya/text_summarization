#Add citations
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

def reconstruct_data(df):
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

    return df_reconstructed



if __name__ == '__main__':
    links_filtered = pd.read_csv('links_filtered.csv')
    f = open('positions.json')
    positions = json.load(f)
    df = reconstruct_data(links_filtered)
    df["n_cites"] = df["n_cites"].astype(int)

    df_final = add_x_y(df, positions)
    df.to_csv('df_final.csv', encoding='utf-8', index=False)