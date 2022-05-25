import copy
import json
import os
'''
{
[
"authors":
"title":
"data":{
'word':

}
]
}
'''
element_data = {
        "id": "",
        "label": "",
        "title": "",
        "journal": "",
        "authors": "",
        "cited_by": "",
        "n_cites": 0,
        "node_size": 0
      }
dossier_path = os.path.dirname(os.path.abspath(__file__))

def construct_articles_as_topics(articles_list):
    articles_as_topics = {}
    for i in range(len(articles_list)):
        articles_as_topics[i] = ["\""+articles_list[i]+"\""]

    with open(dossier_path+"/topics.json", "w") as outfile:
        json.dump(articles_as_topics, outfile)

def construct_data(articles_list):
    word_n = sum([len(i['data']) for i in articles_list])
    elements_datas = []
    edges_data = []
    id = 0
    for article in articles_list:
        authors = article['authors']
        article_name = article['article']
        for data in article['data']:
            element_data_filled = copy.deepcopy(element_data)
            element_data_filled['title'] = data['word']
            element_data_filled['id'] = str(id)
            element_data_filled['label'] = str(id)
            element_data_filled['journal'] = article_name
            element_data_filled['authors'] = authors
            elements_datas.append()
