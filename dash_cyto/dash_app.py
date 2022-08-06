# ========== (c) JP Hwang 2020-04-02  ==========

import logging

# ===== START LOGGER =====

logger = logging.getLogger(__name__)
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
sh.setFormatter(formatter)
root_logger.addHandler(sh)

import pandas as pd
import numpy as np
import plotly.express as px
import dash
import dash_cytoscape as cyto
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
import json

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

# network_df = pd.read_csv('outputs/network_df.csv', index_col=0)  # ~8300 nodes
#network_df = pd.read_csv("outputs/network_df_sm.csv", index_col=0)  # ~4700 nodes
#network_df = pd.read_csv("outputs/df_final0 - df_final.csv")  # ~4700 nodes
network_df = pd.read_csv("outputs/network_df.csv")  # ~4700 nodes

# Prep data / fill NAs
#network_df["citations"] = network_df["citations"].fillna("")
network_df["cited_by"] = network_df["cited_by"].fillna("")
network_df['topic_id'].replace('', np.nan, inplace=True)
network_df.dropna(subset=['topic_id'], inplace=True)
network_df["topic_id"] = network_df["topic_id"].astype(int)
network_df["topic_id"] = network_df["topic_id"].astype(str)
network_df['title'].replace('', np.nan, inplace=True)
network_df.dropna(subset=['title'], inplace=True)
topic_ids = [str(i) for i in range(len(network_df["topic_id"].unique()))]
# lda_val_arr = network_df[topic_ids].values
with open("outputs/metadatas.json", "r") as f:
    metadatas = json.load(f)
topics_txt = [i['title'].replace("title", "").strip() for i in metadatas]

#journal_ser = network_df.groupby("journal")["0"].count().sort_values(ascending=False)


def tsne_to_cyto(tsne_val, scale_factor=40):
    return int(scale_factor * (float(tsne_val)))


def get_node_list(in_df):  # Convert DF data to node list for cytoscape
    return [
        {
            "data": {
                "id": str(i),
                "label": row["source"],
                "article_title": row["title"],
                "cited_by_other_articles": row["cited_by_other_articles"],
                "word": row["source"],
                "journal": row["journal"],
                #"pub_date": row["pub_date"],
                "author": row["author"],
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



default_tsne = 40



def draw_edges(in_df=network_df):
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

#with open("outputs/startup_elms.json", "r") as f:
#    startup_elms = json.load(f)
#startup_elms01 = get_startup_elems(network_df)
#network_df.rename(columns={'title.1': 'title'}, inplace=True)

startup_elms = get_startup_elems(network_df)

#startup_n_cites = startup_elms["n_cites"]
startup_n_cites = 1
#startup_journals = startup_elms["journals"]
startup_journals =  [
    "PLoS One",
    "Viruses",
    "PLoS Pathog"
  ]
#startup_elm_list = startup_elms["elm_list"]
startup_elm_list = startup_elms


col_swatch = px.colors.qualitative.Dark24
def_stylesheet = [
    {
        "selector": "." + str(i),
        "style": {"background-color": col_swatch[i], "line-color": col_swatch[i]},
    }
    for i in range(len(network_df["topic_id"].unique()))
]
def_stylesheet += [
    {
        "selector": "node",
        "style": {"width": "data(node_size)", "height": "data(node_size)"},
    },
    {"selector": "edge", "style": {"width": 1, "curve-style": "bezier"}},
]

def_stylesheet+=[
        # Group selectors
        {
            'selector': 'node',
            'style': {
                'content': 'data(label)',
                'text-halign':'center',
                'text-valign':'center',
            }
        }]

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(
            dbc.NavLink(
                "Article",
                href="https://medium.com/plotly/exploring-and-investigating-network-relationships-with-plotlys-dash-and-dash-cytoscape-ec625ef63c59?source=friends_link&sk=e70d7561578c54f35681dfba3a132dd5",
            )
        ),
        dbc.NavItem(
            dbc.NavLink(
                "Source Code",
                href="https://github.com/plotly/dash-sample-apps/tree/master/apps/dash-cytoscape-lda",
            )
        ),
    ],
    brand="ASD articles text analysis and words relation ",
    brand_href="#",
    color="red",
    dark=True,
)

topics_html = list()
for topic_html in [
    html.Span([str(i) + ": " + topics_txt[i]], style={"color": col_swatch[i]})
    for i in range(len(topics_txt))
]:
    topics_html.append(topic_html)
    topics_html.append(html.Br())

body_layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown(
                            f"""
               -----
                ##### Data:
                -----
                For this demonstration, {len(network_df)} words from articles retrieved from pubmed using a search equation, categorised into
                {len(metadatas)} articles.

                Each Article is shown in different color on the citation map, as shown on the right.
                """
                        )
                    ],
                    sm=12,
                    md=4,
                ),
                dbc.Col(
                    [
                        dcc.Markdown(
                            """
                -----
                ##### Topics:
                -----
                """
                        ),
                        html.Div(
                            topics_html,
                            style={
                                "fontSize": 11,
                                "height": "100px",
                                "overflow": "auto",
                            },
                        ),
                    ],
                    sm=12,
                    md=8,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                cyto.Cytoscape(
                                    id="core_19_cytoscape",
                                    layout={"name": "random"},
                                    style={"width": "100%", "height": "400px"},
                                    elements=startup_elm_list,
                                    stylesheet=def_stylesheet,
                                    minZoom=0.06,
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Alert(
                                    id="node-data",
                                    children="Click on a node to see its details here",
                                    color="secondary",
                                )
                            ]
                        ),
                    ],
                    sm=12,
                    md=8,
                ),
            ]
        )
    ],
    style={"marginTop": 20},
)

app.layout = html.Div([navbar, body_layout])



@app.callback(
    Output("node-data", "children"), [Input("core_19_cytoscape", "selectedNodeData")]
)
def display_nodedata(datalist):
    contents = "Click on a node to see its details here"
    if datalist is not None:
        if len(datalist) > 0:
            data = datalist[-1]
            contents = []
            contents.append(html.H5("The word: " + data["word"].title()))
            contents.append(
                html.P(
                    "Article Title: "
                    + data["article_title"].title()
                    # + ", Published: "
                    # + data["pub_date"]
                )
            )
            contents.append(
                html.P(
                    "Journal: "
                    + data["journal"].title()
                    #+ ", Published: "
                    #+ data["pub_date"]
                )
            )
            contents.append(
                html.P(
                    "Author(s): "
                    + str(data["author"])
                    + ", Citations: "
                    + str(data["n_cites"])
                )
            )
            contents.append(
                html.P(
                    "Cited by other articles: "
                    + str(get_cited_by_other_articles(data["cited_by_other_articles"]))
                )
            )

    return contents


def get_cited_by_other_articles(indexes):
    cited_by_articles = None
    try:
        if(indexes is not None):
            cited_by_articles = ""
            evaluated_index = eval(indexes[:-1])
            if(isinstance(evaluated_index, int)):
                cited_by_articles = topics_txt[evaluated_index]
            else:
                for i in eval(indexes[:-1]):
                    cited_by_articles += topics_txt[i]+", "
                cited_by_articles.replace("\\textemdash", "")
    except:
        pass
    return cited_by_articles

if __name__ == "__main__":
    app.run_server(debug=False)