import re
import PyPDF2
import pdfplumber
import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.snowball import SnowballStemmer
import heapq
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Download required NLTK resources. This only needs to be done once.
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('punkt_tab')

# The first step is to get the URL and its id to get the transcript.
def get_pdf_from_url(url_link, file_path):
    response = requests.get(url_link)
    with open(file_path, 'wb') as file:
        file.write(response.content)
def get_text_from_pdf(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
        return text
    except:
        print("Error in getting text from PDF")
        return None
# Now that we got the id and the transcript, the second step is to summarize it.
def summarize_text(text):
    stopwords = nltk.corpus.stopwords.words('english')
    sentence_list = text.split("\n")
    stemmer = SnowballStemmer("english", ignore_stopwords=True)
    # print(sentence_list)
    # Frequency of words to scores dictionary.
    word_frequency = {}
    word_list = nltk.word_tokenize(text) # Tokenize based on each word.
    for word in word_list:
        if word not in stopwords:
            if stemmer.stem(word) not in word_frequency:
                word_frequency[stemmer.stem(word)] = 1
            else:
                word_frequency[stemmer.stem(word)] += 1
    max_freq = max(word_frequency.values())
    # print(word_frequency)
    for word in word_frequency:
        word_frequency[word] = word_frequency[word] / max_freq
    
    # Now we will get the scores of the sentences based on the words.
    sentence_frequency = {}
    for sentence in sentence_list:
        for word in word_list:
            if stemmer.stem(word) in word_frequency and word in sentence:
                if sentence not in sentence_frequency:
                    sentence_frequency[sentence] = word_frequency[stemmer.stem(word)]
                else:
                    sentence_frequency[sentence] += word_frequency[stemmer.stem(word)]
    summary_length = int(len(sentence_frequency) * 0.2)
    summary = heapq.nlargest(summary_length, sentence_frequency, key=sentence_frequency.get)
    return summary
def summary_text2(text):
    sentence_list = text.split("\n")
    sentences_count = int(len(sentence_list) * 0.2)
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count)
    return summary
def main(input_link):
    # 'https://stmarysguntur.com/wp-content/uploads/2019/07/UNIT-1-converted-converted.pdf'
    url_link = input_link
    get_pdf_from_url(url_link, '/Users/sophiajacob/Downloads/SummarizePDFProject/file.pdf')
    text = get_text_from_pdf('/Users/sophiajacob/Downloads/SummarizePDFProject/file.pdf')
    result = ""
    if text != None:
        summary = summarize_text(text)
        result += "<h1>Summary: </h1><br>"
        # print("Summary: ")
        for i in summary:
            #print(i)
            result += str(i)
            result += "<br>"
        summary = summary_text2(text)
        result += "<br>"
        result += "<br>"
       # print()
       # print()
        result += "<h1>Second Summary: </h1><br>"
        # print("Second Summary: ")
        for i in summary:
            #print(i)
            result += str(i)
            result += "<br>"
    return result
    
#main()