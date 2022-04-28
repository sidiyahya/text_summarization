import re

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

def convert_pdf_to_txt_and_metadata(path):
    ## Parametrage de la librairie pdfminer pour transformer le pdf en text et l'enregistre dans une variable
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    ## Le code qui suit sert à récuperer toutes les pages pour les enregistrer dans un text complet
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)
    text = retstr.getvalue()  # On enregistre le text du pdf en variable text
    fp.close()  # On ferme le pdf
    device.close()
    retstr.close()
    ## Fin du paramétrage

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

    return text, metadata  # On retourne les deux variables qui contiennent le texte + DOI