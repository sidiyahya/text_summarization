# ========== (c) JP Hwang 2020-04-02  ==========

import logging

# ===== START LOGGER =====
from output_methods.dash_cytoscape.dash_tools import get_startup_elems, draw_edges, update_node_data

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
from sklearn.manifold import TSNE
import umap
import json

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

# network_df = pd.read_csv('outputs/network_df.csv', index_col=0)  # ~8300 nodes
#network_df = pd.read_csv("outputs/network_df_sm.csv", index_col=0)  # ~4700 nodes
network_df = pd.read_csv("outputs/df_final0 - df_final.csv")  # ~4700 nodes

# Prep data / fill NAs
#network_df["citations"] = network_df["citations"].fillna("")
network_df["cited_by"] = network_df["cited_by"].fillna("")
network_df["topic_id"] = network_df["topic_id"].astype(str)
topic_ids = [str(i) for i in range(len(network_df["topic_id"].unique()))]
# lda_val_arr = network_df[topic_ids].values
with open("outputs/lda_topics.json", "r") as f:
    lda_topics = json.load(f)
topics_txt = [lda_topics[str(i)] for i in range(len(lda_topics))]
topics_txt = [[j.split("*")[1].replace('"', "") for j in i] for i in topics_txt]
topics_txt = ["; ".join(i) for i in topics_txt]

#journal_ser = network_df.groupby("journal")["0"].count().sort_values(ascending=False)

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
    brand="Plotly dash-cytoscape demo - CORD-19 LDA analysis output",
    brand_href="#",
    color="dark",
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
                {len(network_df.topic_id.unique())} articles.

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
                dcc.Markdown(
                    """
            -----
            ##### Filter / Explore node data
            Node size indicates number of citations from this collection, and color indicates its
            article.

            Use these filters to highlight papers with:
            * certain numbers of citations from this collection, and
            * by journal title

            Try showing or hiding citation connections with the toggle button, and explore different visualisation options.

            -----
            """
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
                dbc.Col(
                    [
                        dbc.Badge(
                            "Minimum citation(s):", color="info", className="mr-1"
                        ),
                        dbc.FormGroup(
                            [
                                dcc.Dropdown(
                                    id="n_cites_dropdown",
                                    options=[
                                        {"label": k, "value": k} for k in range(1, 21)
                                    ],
                                    clearable=False,
                                    value=startup_n_cites,
                                    style={"width": "50px"},
                                )
                            ]
                        ),
                        dbc.Badge(
                            "Journal(s) published:", color="info", className="mr-1"
                        ),
                        dbc.Badge("Citation network:", color="info", className="mr-1"),
                        dbc.FormGroup(
                            [
                                dbc.Container(
                                    [
                                        dbc.Checkbox(
                                            id="show_edges_radio",
                                            className="form-check-input",
                                            checked=True,
                                        ),
                                        dbc.Label(
                                            "Show citation connections",
                                            html_for="show_edges_radio",
                                            className="form-check-label",
                                            style={
                                                "color": "DarkSlateGray",
                                                "fontSize": 12,
                                            },
                                        ),
                                    ]
                                )
                            ]
                        ),
                    ],
                    sm=12,
                    md=4,
                ),
            ]
        ),
    ],
    style={"marginTop": 20},
)

app.layout = html.Div([navbar, body_layout])



@app.callback(
    Output("core_19_cytoscape", "elements"),
    [
        Input("n_cites_dropdown", "value"),
        #Input("journals_dropdown", "value"),
        Input("show_edges_radio", "checked"),
    ],
)
def filter_nodes(usr_min_cites, show_edges, dim_red_algo):
    # print(usr_min_cites, usr_journals_list, show_edges, dim_red_algo, tsne_perp)
    # Use pre-calculated nodes/edges if default values are used
    if (
        usr_min_cites == startup_n_cites
        and show_edges == True
        and dim_red_algo == "tsne"
    ):
        logger.info("Using the default element list")
        return startup_elm_list

    else:
        # Generate node list
        cur_df = network_df[(network_df.n_cites >= usr_min_cites)]

        cur_node_list = update_node_data(dim_red_algo, tsne_perp, in_df=cur_df)
        conn_list = []

        if show_edges:
            conn_list = draw_edges(cur_df)

        elm_list = cur_node_list + conn_list

    return elm_list


@app.callback(
    Output("node-data", "children"), [Input("core_19_cytoscape", "selectedNodeData")]
)
def display_nodedata(datalist):
    contents = "Click on a node to see its details here"
    if datalist is not None:
        if len(datalist) > 0:
            data = datalist[-1]
            contents = []
            contents.append(html.H5("Title: " + data["title"].title()))
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
                    + str(data["authors"])
                    + ", Citations: "
                    + str(data["n_cites"])
                )
            )

    return contents

if __name__ == "__main__":
    app.run_server(debug=False)