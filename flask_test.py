from flask import Flask, render_template, request, redirect, url_for
from konlpy.tag import Twitter
from collections import Counter
import unicodedata
from khaiii import KhaiiiApi

app = Flask(__name__)

@app.route('/')
# def hello_world():
#     return 'Hello World!'

@app.route('/konlpy')
def main():
    return render_template('main.html')

@app.route('/result', methods=['POST', 'GET'])
def analysis(text=None):
    if request.method == 'POST':
        my_text = request.form['text']
        # result = konply_noun(my_text)
        result = khaiii_noun(my_text)
        # print(result)
    else:
        result = None
    return render_template('result.html', result = result, text = my_text)

def konply_noun(text, ntags = 50):
    nlpy = Twitter()
    text = unicodedata.normalize('NFC', text)
    nouns = nlpy.nouns(text)
    count = Counter(nouns)

    return_list = []
    for n, c in count.most_common(ntags):
        temp = {'tag' : n, 'count' : c}
        return_list.append(temp)

    return return_list

def khaiii_noun(text, ntags=50):
    api = KhaiiiApi()
    result_list = []
    text = unicodedata.normalize('NFC', text)
    for word in api.analyze(text):
        for morph in word.morphs:
            if morph.tag in ['NNG', 'NNP']:
                result_list.append(morph.lex)
    count = Counter(result_list)
    return_list = []
    for n, c in count.most_common(ntags):
        temp = {'tag' : n, 'count' : c}
        return_list.append(temp)
    
    return return_list

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80', debug=True)
