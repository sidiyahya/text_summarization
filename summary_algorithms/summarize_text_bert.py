from summarizer import Summarizer

def summarize_text_bert_light(text):
    model = Summarizer()
    result = model(text, min_length=10)
    full = ''.join(result)
    print(full)
    return full

def summarize_text_bert_num_sentences(text):
    model = Summarizer()
    #result = model(text, ratio=0.1, max_length=1)  # Specified with ratio
    result = model(text, num_sentences=10)  # Will return 3 sentences
    return result

def summarize_text_bert_num_ratio(text):
    model = Summarizer()
    result = model(text, ratio=0.03)  # Specified with ratio
    #result = model(text, num_sentences=10)  # Will return 3 sentences
    return result

def summarize_text_k(text):
    model = Summarizer()
    res = model.calculate_optimal_k(text, k_max=10)
    print(res)


if __name__ == '__main__':
    with open("/home/mohamedali/PycharmProjects/text_summarization/pdf_processing/pdf_processing_output/abstract of abstracts.txt", "r", encoding="utf-8") as f:
        text = " ".join(f.readlines())

    print("bert_num_sentences")
    bert_num_sentences = summarize_text_bert_num_sentences(text)
    print(bert_num_sentences)
    print("bert_ratio")
    bert_ratio = summarize_text_bert_num_ratio(text)
    print(bert_ratio)
    print("Bert Light")
    bert_light = summarize_text_bert_light(text)
    print(bert_light)