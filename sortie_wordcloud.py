import matplotlib.pyplot as plt
from wordcloud import WordCloud

from read_files import read_text_file

def run_wordcloud(text):
    wc = WordCloud()
    wc.generate(text)

    wc.to_file('output.png')
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()



if __name__ == '__main__':
    file = input("Entrez le chemin de votre fichier: ")
    text = read_text_file(file)
    run_wordcloud(text)

