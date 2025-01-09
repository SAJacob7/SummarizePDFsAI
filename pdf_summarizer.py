import re
import PyPDF2
import pdfplumber
import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import heapq

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
    # print(sentence_list)
    # Frequency of words to scores dictionary.
    word_frequency = {}
    word_list = nltk.word_tokenize(text) # Tokenize based on each word.
    for word in word_list:
        if word not in stopwords:
            if word not in word_frequency:
                word_frequency[word] = 1
            else:
                word_frequency[word] += 1
    max_freq = max(word_frequency.values())
    # print(word_frequency)
    for word in word_frequency:
        word_frequency[word] = word_frequency[word] / max_freq
    
    # Now we will get the scores of the sentences based on the words.
    sentence_frequency = {}
    for sentence in sentence_list:
        for word in word_list:
            if word in word_frequency and len(sentence.split(' ')) < 35 and word in sentence:
                if sentence not in sentence_frequency:
                    sentence_frequency[sentence] = word_frequency[word]
                else:
                    sentence_frequency[sentence] += word_frequency[word]
    summary = heapq.nlargest(30, sentence_frequency, key=sentence_frequency.get)
    return summary
def main():
    url_link = 'https://www.whitehouse.gov/wp-content/uploads/2022/12/TTC-EC-CEA-AI-Report-12052022-1.pdf'
    get_pdf_from_url(url_link, '/Users/sophiajacob/Downloads/SummarizePDFProject/file.pdf')
    text = get_text_from_pdf('/Users/sophiajacob/Downloads/SummarizePDFProject/file.pdf')
    if text != None:
        summary = summarize_text(text)
        print("Summary: ")
        for i in summary:
            print(i)
main()