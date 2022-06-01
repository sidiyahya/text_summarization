import numpy as np
import umap

from dash_cyto.dash_app import logger


def tsne_to_cyto(tsne_val, scale_factor=40):
    return int(scale_factor * (float(tsne_val)))


def get_node_list(in_df):  # Convert DF data to node list for cytoscape
    return [
        {
            "data": {
                "id": str(i),
                "label": str(i),
                "title": row["title"],
                "journal": row["journal"],
                #"pub_date": row["pub_date"],
                "authors": row["authors"],
                "cited_by": row["cited_by"],
                "n_cites": row["n_cites"],
                "node_size": int(np.sqrt(1 + row["n_cites"]) * 10),
            },
            #"position": {"x": tsne_to_cyto(row["x"]), "y": tsne_to_cyto(row["y"])},
            "classes": row["topic_id"],
            "selectable": True,
            "grabbable": False,
        }
        for i, row in in_df.iterrows()
    ]


def get_node_locs(in_df, dim_red_algo="tsne", tsne_perp=40):
    logger.info(
        f"Starting dimensionality reduction on {len(in_df)} nodes, with {dim_red_algo}"
    )

    if dim_red_algo == "tsne":
        node_locs = TSNE(
            n_components=2,
            perplexity=tsne_perp,
            n_iter=300,
            n_iter_without_progress=100,
            learning_rate=150,
            random_state=23,
        ).fit_transform(in_df[topic_ids].values)
    elif dim_red_algo == "umap":
        reducer = umap.UMAP(n_components=2)
        node_locs = reducer.fit_transform(in_df[topic_ids].values)
    else:
        logger.error(
            f"Dimensionality reduction algorithm {dim_red_algo} is not a valid choice! Something went wrong"
        )
        node_locs = np.zeros([len(in_df), 2])

    logger.info("Finished dimensionality reduction")

    x_list = node_locs[:, 0]
    y_list = node_locs[:, 1]

    return x_list, y_list


default_tsne = 40


def update_node_data(dim_red_algo, tsne_perp, in_df):
    (x_list, y_list) = get_node_locs(in_df, dim_red_algo, tsne_perp=tsne_perp)

    x_range = max(x_list) - min(x_list)
    y_range = max(y_list) - min(y_list)
    # print("Ranges: ", x_range, y_range)

    scale_factor = int(4000 / (x_range + y_range))
    in_df["x"] = x_list
    in_df["y"] = y_list

    tmp_node_list = get_node_list(in_df)
    for i in range(
        len(in_df)
    ):  # Re-scaling to ensure proper canvas scaling vs node sizes
        tmp_node_list[i]["position"]["x"] = tsne_to_cyto(x_list[i], scale_factor)
        tmp_node_list[i]["position"]["y"] = tsne_to_cyto(y_list[i], scale_factor)

    return tmp_node_list


def draw_edges(in_df):
    conn_list_out = list()

    for i, row in in_df.iterrows():
        citations = row["cited_by"]

        print(citations)
        print(type(citations))
        if len(citations) == 0:
            citations_list = []
        else:
            citations_list = citations.split(",")
        for cit in citations_list:
            if int(cit) in in_df.index:
                print(cit)
                tgt_topic = row["topic_id"]
                temp_dict = {
                    "data": {"source": cit, "target": str(i)},
                    "classes": tgt_topic,
                    "tgt_topic": tgt_topic,
                    "src_topic": in_df.loc[int(cit), "topic_id"],
                    "locked": True,
                }
                conn_list_out.append(temp_dict)

    return conn_list_out

def get_startup_elems(network_df, tsne_perp=40, dim_red_algo="tsne", show_edges=True):
    cur_df = network_df
    #cur_node_list = update_node_data(dim_red_algo, tsne_perp, in_df=cur_df)
    conn_list = []
    cur_node_list = get_node_list(network_df)
    if show_edges:
        conn_list = draw_edges(cur_df)

    elm_list = cur_node_list + conn_list

    return elm_list