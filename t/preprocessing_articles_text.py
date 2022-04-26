import string
import re

# remove punctuation
from t.specific_cleaning_standard import clean_standard_articles


def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

wrong_digits = r'([a-z]+)(\d+)\s'

references = r'References\:?\n?\s?\d+\.?'
fig = r'(?:Fig\.|Figure)\s?\d+\s?(?:.*\n?)+?\n\n'
urls = r'(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])'
parenthesis = r'(?:\(.*?\)|\[.*?\])'
single_chars = r'\n\w\n'

def remove_outliers(text):
    text_cleaned_from_figures = re.sub(fig, '', text)
    text_cleaned_from_urls = re.sub(urls, '', text_cleaned_from_figures)
    text_cleaned_from_parenthesis = re.sub(parenthesis, '', text_cleaned_from_urls)
    #single_chars = re.sub(parenthesis, '', text_cleaned_from_parenthesis)
    text_without_ponctuation = remove_punctuation(text_cleaned_from_parenthesis)
    text_without_references = remove_references(text_without_ponctuation)
    text_without_wrong_digits = remove_wrong_digits(wrong_digits, text_without_references)
    text_without_single_chars = re.sub(single_chars, '', text_without_wrong_digits)
    text_processed = clean_standard_articles(text_without_single_chars)

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
