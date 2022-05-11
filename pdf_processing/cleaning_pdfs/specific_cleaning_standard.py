#pattern [from index, [index, max length, regex]*n]

#['form', 'bold', regex]
#['startwith, 'text', list]
import copy
#Format d'entre de la methode : [["line1", "line2"], ["line1", "line2"]]
def clean_standard_articles(text_per_pages, config_per_page):
    text_per_pages = text_per_pages[config_per_page[0]:]
    config_per_page = config_per_page[1:]
    cleaned_text_per_pages = []
    for text_per_page in text_per_pages:
        cleaned_text_per_pages.append(clean_standard_articles_page(text_per_page, config_per_page))

    return cleaned_text_per_pages

def clean_standard_articles_page(text_per_page, config_per_page):
    return clean_specific_text_at_position(text_per_page, config_per_page)


def clean_specific_text_at_position(text_per_page, config_per_page):
    config_per_page_ = copy.deepcopy(find_last(text_per_page, config_per_page))
    indexes_to_remove = []
    for ignored_text in config_per_page_:
        index_to_remove = ignored_text[0]
        if(len(ignored_text)==1):
            indexes_to_remove.append(index_to_remove)
            #del text_per_page[index_to_remove]
        elif(len(ignored_text)==2):
            len_index_to_remove = ignored_text[1]
            if(len(text_per_page[index_to_remove])<len_index_to_remove):
                indexes_to_remove.append(index_to_remove)
                #del text_per_page_cleaned[index_to_remove]

    text_per_page_cleaned = [text_per_page[i] for i in range(len(text_per_page)) if(i not in indexes_to_remove)]
    return text_per_page_cleaned

def find_last(text, per_page):
    per_page_conf = copy.deepcopy(per_page)
    last = len(text)-1
    for i in range(len(per_page_conf)):
        per_page_conf_unit = per_page_conf[i]
        if(isinstance(per_page_conf_unit[0], str)):
            if(per_page_conf_unit[0]=="last"):
                per_page_conf[i][0] = last
    return per_page_conf
