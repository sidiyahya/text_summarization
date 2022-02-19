import re

from summarizer import Summarizer
from tqdm import tqdm


def summerize_text_uzing_bert(text):

    model = Summarizer()
    bert_predicted_summary = []
    k = 0
    for i in tqdm(text):
        if k < 10:
            x = model(str(i))
            bert_predicted_summary.append(x)
            k += 1

    return bert_predicted_summary


def summerize_text_using_bert_heavy(text):
    model = Summarizer()
    optimal_number_sentences = model.calculate_optimal_k(text, k_max=10)
    result = model(text, num_sentences=optimal_number_sentences)
    return result

def summerize_text_using_bert(text):
    model = Summarizer()
    summerize_text = model(text)
    return summerize_text

if __name__ == '__main__':
    with open('text_articles/test_algo.txt', 'r') as f:
        file_data = f.read()

    summary = summerize_text_using_bert(file_data)
    print(summary)

    summary = summerize_text_using_bert_heavy(file_data)
    print(summary)