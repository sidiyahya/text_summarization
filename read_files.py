def read_text_file(path):
    with open(path, encoding='utf-8') as f:
        txt = ''.join(f.readline())
    return txt