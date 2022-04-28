import requests

from pdf_tools import convert_pdf_to_txt_and_metadata


def fonctionresume(mylist):
    pdfs = []  # On initialise une liste qui va contenir les textes des fichiers pdf
    metadatas = []  # On initialise une liste qui va contenir les DOI

    ## Cette boucle va lancer la première fonction pour récuperer les textes et DOI
    for i in mylist:
        pdf, metadata = convert_pdf_to_txt_and_metadata(i)
        metadatas.append(metadata)
        pdfs.append(pdf)

    pdfs2 = []  # On initialise une liste qui va contenir le texte restructuré
    # cette étape sert à recoller les phrase

    for i in pdfs:
        txt = i.split("\n")  # On split le texte avec tous les retours chariot pour le transformer en liste
        f = ""

        ## Cette boucle sert à reconstituer les phrases, on recolle toutes les varriables de la liste
        ## Quand on trouve une ponctuation suivie d'un retour chariot, dans ce cas on met un retour chariot dans le texte
        ## Sinon on continuer à coller les variables pour recoller les textes séparés lors de l'extraction
        for i in range(0, len(txt)):
            if len(txt[i]) == 0:
                txt[i] = "\n"
            if txt[i][-1] == "." or txt[i][-1] == "?" or txt[i][-1] == "!" or txt[i][-1] == ":" or txt[i][
                0].isupper() == True:
                f = str(f + "\n" + txt[i])
            else:
                f = str(f + txt[i])
        pdfs2.append(f)

    ## Dans cette partie on récupère les paragraphes methods et results
    ll1 = []  # On initialise la première liste qui va contenir les paragraphes Methods
    ll2 = []  # On initialise la deuxième liste qui va contenir les paragraphes Results

    ## Cette boucle parcours tous les textes nettoyés et restructurés des pdfs
    for i in pdfs2:
        text = i
        ## On cherche tous les titres qui contiennent methods et results
        l1 = text[text.lower().find("\nmethods\n"):text.lower().find("\nresults\n")]
        if l1 == "":
            ## Des fois les articles mettent materials and methods donc on tente une deuxieme fois
            l1 = text[text.lower().find("\nmaterials and methods\n"):text.lower().find("\nresults\n")]
        l2 = text[text.lower().find("\nresults\n"):text.lower().find("\nconclusion\n")]
        ll1.append(l1)
        ll2.append(l2)

    ## Cette fonction sert à communiquer avec l'API pour récuperer les métadatas avec les DOI qu'on a récuperer
    def doi2bib(doi):
        url = "http://dx.doi.org/" + doi

        headers = {"accept": "application/x-bibtex"}
        r = requests.get(url, headers=headers)

        return r.text

    ## On nettoie ce que l'API nous a retourné pour enlever les {} et autres
    for i in range(0, len(metadatas)):
        l = doi2bib(metadatas[i])
        l = l.replace("	", "")
        l = l.replace("{", "")
        l = l.replace("}", "")
        l = l.split(",\n")
        metadatas[i] = l

    ## On retourne les textes pdfs, les paragraphes Methods et paragraphes Results ainsi que les métadatas
    return pdfs2, ll1, ll2, metadatas