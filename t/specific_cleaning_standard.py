#pattern [from, [index, length, regex]*n]
def clean_standard_articles(text_per_page):
    per_page_standard = [1, [0], ["last", 20]]
    return clean_specific_text_at_position(text_per_page, per_page_standard)


def clean_specific_text_at_position(text_per_page, per_page):
    per_page_ = per_page[:1] + find_last(text_per_page, per_page[1:])
    cleaned_text = [text_per_page[0]] if(per_page_[0]==1) else []
    for i in range(per_page_[0], len(text_per_page) - 1):
        text = text_per_page[i]
        for ignored_text in per_page_[1:]:
            index_to_remove = ignored_text[0]
            if(len(ignored_text)==1):
                del text[index_to_remove]
            elif(len(ignored_text)==2):
                len_index_to_remove = ignored_text[1]
                if(len(text[index_to_remove])<len_index_to_remove):
                    del text[index_to_remove]

        cleaned_text.append(text)

    return cleaned_text

def find_last(text, per_page):
    last = len(text)-1
    for i in range(len(per_page)):
        per_page_unit = per_page[i]
        if(isinstance(per_page_unit[0], str)):
            if(per_page_unit[0]=="last"):
                per_page[i][0] = last
    return per_page
