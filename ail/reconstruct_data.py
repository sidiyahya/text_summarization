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
    return df_reconstructed



if __name__ == '__main__':
    links_filtered = pd.read_csv('links_filtered.csv')
    f = open('positions.json')
    positions = json.load(f)
    df = reconstruct_data(links_filtered)
    df_final = add_x_y(df, positions)
    df.to_csv('df_final.csv', encoding='utf-8', index=False)