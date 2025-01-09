import re
from youtube_transcript_api import YouTubeTranscriptApi
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import heapq

# Download required NLTK resources. This only needs to be done once.
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('punkt_tab')

# The first step is to get the URL and its id to get the transcript.
def get_id_of_video(url_link):
    video_id_regex = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(video_id_regex, url_link)
    try:
        if match:
            return match.group(1)
        else:
            raise KeyError
    except:
        print("Error in getting ID")
        return None
def get_transcript_of_video(url_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(url_id)
        return transcript
    except:
        print("Error in getting transcript")
        return None
# Now that we got the id and the transcript, the second step is to summarize it.
def transcript_to_text(transcript):
    text_list = [transcript[i]['text'] for i in range(len(transcript))]
    transcript_text = '\n'.join(text_list)
    return transcript_text
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
    summary = heapq.nlargest(20, sentence_frequency, key=sentence_frequency.get)
    return summary
def main():
    url_link = 'https://www.youtube.com/watch?v=H14bBuluwB8'
    url_id = get_id_of_video(url_link)
    if url_id != None:
        transcript = get_transcript_of_video(url_id)
        if transcript != None:
            text = transcript_to_text(transcript)
            summary = summarize_text(text)
            print("Summary: ")
            for i in summary:
                print(i)
main()