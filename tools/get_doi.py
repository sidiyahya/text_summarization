import re

import requests


def get_doi_from_text(text):
    doi = ""
    ## On récupère les doi en cherchant le lien doi.org suivit d'un code de 10 caractères
    doi_re = re.compile("doi.org/10.(\d)+/([^(\s\>\"\<)])+")
    m = doi_re.search(text)
    try:
        ## On teste la première méthode si cela ne fonctionne pas on passe à d'autres méthodes
        metadata = m.group(0)
    except:
        doi_re = re.compile("10.(\d)+=([^(\s\>\"\<)])+")
        m = doi_re.search(text)
        try:
            metadata = m.group(0)
            metadata = metadata.replace("=", "/")
        except:
            doi_re = re.compile("10.(\d)+/([^(\s\>\"\<)])+")
            m = doi_re.search(text)
            metadata = m.group(0)
    metadata = metadata.replace("doi.org/", "")

    if(len(metadata)):
        doi = doi2bib(metadata)

    return doi

    ## Cette fonction sert à communiquer avec l'API pour récuperer les métadatas avec les DOI qu'on a récuperer
def doi2bib(doi):
    url = "http://dx.doi.org/" + doi

    headers = {"accept": "application/x-bibtex"}
    r = requests.get(url, headers=headers)

    return parse_data(r.text)

def parse_data(l):
    l = l.replace("	", "")
    l = l.replace("{", "")
    l = l.replace("}", "")
    l = l.split(",\n")
    return l
