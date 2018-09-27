from flask import Flask, request
import json
import re

app = Flask(__name__)

@app.route("/words/avg_len", methods=['POST'])
def average_word_length():
    words = extract_words_from_input_text(request.get_json())
    # get the total length of all the words within the text
    sum_of_lengths = sum([len(word) for word in words])
    # find the average by dividing the total sum by the number of words in text
    avg_length = float(sum_of_lengths) / float(len(words))
    average_word_length = {'average_word_length': avg_length}
    return json_response(average_word_length)

@app.route("/words/most_com", methods=['POST'])
def most_common_word():
    words = extract_words_from_input_text(request.get_json())
    freq = {}
    # create a hashmap with keys as words and values as word frequency
    for word in words:
        if word in freq:
            freq[word] += 1
        else:
            freq[word] = 1
    # grab the values(counts of each word) from the freq hashmap
    counts_of_each_word = freq.values()
    # iterate over the hashmap's key/value pairs and grab the word with the highest count
    most_common_word = [word for word, count in freq.items() if count == max(counts_of_each_word)]
    # in the case of a tie, sort the array of common words alphabetically and convert to hashmap
    most_common_word = dict(most_common_word=sorted(most_common_word)[0])
    return json_response(most_common_word)

@app.route("/words/median", methods=['POST'])
def median_word():
    words = extract_words_from_input_text(request.get_json())
    freq = {}
    for word in words:
        if word not in freq:
            freq[word] = 1
        else:
            freq[word] += 1

    # grab the values(counts of each word) from the freq hashmap
    counts_of_each_word = sorted(freq.values())
    mid = len(counts_of_each_word) // 2

    # if even number of frequency distributions, grab the middle item and it's preceding item
    if len(counts_of_each_word) % 2 == 0:
        median_count = [counts_of_each_word[mid], counts_of_each_word[mid - 1]]
    else:
        median_count = [counts_of_each_word[mid]]

    # iterate over the hashmap's key/value pairs and grab the word(s) within the median distribution
    median = [word for word, ct in freq.items() if ct in median_count]
    # convert median array to hashmap
    median = dict(median=median)
    return json_response(median)

@app.route("/sentences/avg_len", methods=['POST'])
def average_sentence_length():
    sentences = extract_sentences_from_input_text(request.get_json())
    # get the total length of all the sentences within the text
    sum_of_lengths = sum([len(sentence) for sentence in sentences])
    # find the average by dividing the total sum by the number of sentences in text
    avg_length = float(sum_of_lengths) / float(len(sentences))
    average_sentence_length = {'average_sentence_length': avg_length}
    return json_response(average_sentence_length)

@app.route("/phones", methods=['POST'])
def find_all_phone_numbers():
    phone_numbers = extract_phone_numbers_from_input_text(request.get_json())
    return json_response(phone_numbers)

def extract_words_from_input_text(input):
    text = input['text']
    text = text.lower()
    """
        1) use regular expression to find all occurrences of words (pieces of input string with > 1 alphabet char AND containing only alphabet chars) 
        
        2) split into array containing just words
        
        3) concatenate array into single string with spaces separating each word
    """
    words = " ".join(re.findall("[a-zA-Z]+", text))
    words = words.split()
    return words

def extract_sentences_from_input_text(input):
    text = input['text']
    text = text.lower()
    """
        1) sentences are defined as a grouping of alphanumeric chars separated by '.', '?', or '!'
        1) use regular expression to split text on '.', '?', and '!' -- these act as delimiters between sentences
    """
    sentences = re.split(r"[\.|\?|\!]+", text)
    return sentences

def extract_phone_numbers_from_input_text(input):
    text = input['text']

    """
        1) phone numbers are defined as a group of 10 digits separated by dashes
        2) dashes separate the phone number into a 3-3-4 combination -- 1st three numbers separated by a dash followed by another 3 numbers separated by a dash and lastly the last 4 numbers
        
        3) use regex to find a grouping of numbers in the above 3-3-4 combination
    
    """

    phone_numbers = re.findall(r'\d{3}-\d{3}-\d{4}', text)
    return phone_numbers

def json_response(data):
    response = app.response_class(
        response=json.dumps(data) + '\n',
        status=200,
        mimetype='application/json'
    )

    return response

if __name__=='__main__':
    app.run(host='0.0.0.0')
