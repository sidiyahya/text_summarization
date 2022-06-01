import string
import re

# remove punctuation
from pdf_processing.cleaning_pdfs.specific_cleaning_standard import clean_standard_articles


def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

wrong_digits = r'([a-z]+)(\d+)\s'

#references = r'References(?:\:?\n?\s?\d+\.?|\n)'
references = r'References\:?'
#fig = r'(?:Fig\.|Figure)\s?\d+\s?(?:.*\n?)+?\n'
fig = r'(?:Fig\.|Figure)\s?\d+\s?.*\n'
urls = r'(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])'
parenthesis = r'(?:\(.*?\)|\[.*?\])'
single_chars = r'\n\w\n'
single_words = r'(^\w+$\n)'
#chaines de caracteres : cdc
def remove_outliers(text):
    #Enlever les cdc des figures
    text_cleaned_from_figures = re.sub(fig, '', text)
    #Enlever les urls
    text_cleaned_from_urls = re.sub(urls, '', text_cleaned_from_figures)
    #Enlever les cdc entre les ()
    text_cleaned_from_parenthesis = re.sub(parenthesis, '', text_cleaned_from_urls)
    #Enlever les mots seul
    text_cleaned_from_single_words = re.sub(single_words, '', text_cleaned_from_parenthesis)
    #Enlever les ponctuations
    text_without_ponctuation = remove_punctuation(text_cleaned_from_single_words)
    #Enlever les references
    text_without_references = remove_references(text_without_ponctuation, sep="\n")
    #Enlever les chiffres erronés
    text_without_wrong_digits = remove_wrong_digits(wrong_digits, text_without_references)
    #Enlever les caracteres unique
    text_without_single_chars = re.sub(single_chars, '', text_without_wrong_digits)

    text_processed = text_without_single_chars

    return text_processed


def find_matching_line(regex, text, sep):
    text_lines = text.split(sep)
    matched_index = None
    for line_i in range(len(text_lines)):
        if re.match(regex, text_lines[line_i]):
            matched_index = line_i
            break
    return matched_index


def remove_references(text, sep="\n\n"):
    cleaned_text = text
    index = find_matching_line(references, text, sep)
    if(index is not None):
        text_lines = text.split(sep)
        cleaned_text = sep.join(text_lines[:index])

    return cleaned_text

def remove_wrong_digits(regex, text):
    pattern = re.compile(regex)
    for (letters, numbers) in re.findall(pattern, text):
        text = text.replace(letters+numbers, letters)

    return text
