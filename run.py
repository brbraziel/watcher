import nltk
import csv
import re
import ast
from flask import Flask, escape, request, Response
from flask_cors import CORS

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    payload = request.get_json(force=True)
    url = payload['param']

    with open('treinados.txt', 'r') as treino:
        dados = treino.read()
        treino.close()      

    dados = ast.literal_eval(dados)
    url = re.sub('[^A-Za-z0-9]+', ' ', str(url))

    analise = Analise()
    analise = analise.CalcularScore(url, dados)[0]
    return {analise: analise}

class Analise:
    def __init__(self):
        with open('datasets/benignos.csv') as b:
            benigno = csv.reader(b)
            benigno = list(benigno)
            b.close()

        with open('datasets/malware.csv') as m:
            malware = csv.reader(m)
            malware = list(malware)
            m.close()

        with open('datasets/spam.csv') as s:
            spam = csv.reader(s)
            spam = list(spam)
            s.close()

        with open('datasets/phishing.csv') as p:
            phishing = csv.reader(p)
            phishing = list(phishing)
            p.close()

        benigno, malware, phishing, spam = self.RemoverSimbolos(benigno, malware, phishing, spam)
        treinamento = self.Treinamento(benigno, malware, phishing, spam)
        """dados = self.Aprendizado(treinamento)

        with open('treinados.txt', 'a') as treino:
            treino.write(str(dados))
            treino.close()"""

        with open('treinados.txt', 'r') as treino:
            dados = treino.read()
            treino.close()      

        dados = ast.literal_eval(dados)

    def Tokenize(self, sentence):
        sentence = sentence.lower()
        sentence = nltk.word_tokenize(sentence)
        return sentence

    def RemoverSimbolos(self, b, m, p, s):
        benigno = []
        malware = []
        phishing = []
        spam = []

        for url in b:            
            benigno.append(re.sub('[^A-Za-z0-9]+', ' ', url[0]))
        for url in m:            
            malware.append(re.sub('[^A-Za-z0-9]+', ' ', url[0]))
        for url in p:            
            phishing.append(re.sub('[^A-Za-z0-9]+', ' ', url[0]))
        for url in s:            
            spam.append(re.sub('[^A-Za-z0-9]+', ' ', url[0]))
        
        return benigno, malware, phishing, spam

    def Treinamento(self, benigno, malware, phishing, spam):
        training_data = []
        for url in benigno:
            training_data.append({'classe': 'seguro', 'link': url})
        for url in malware:
            training_data.append({'classe': 'inseguro', 'link': url})
        for url in phishing:
            training_data.append({'classe': 'inseguro', 'link': url})
        for url in spam:
            training_data.append({'classe': 'inseguro', 'link': url})
        
        return training_data

    def Aprendizado(self, treino):
        corpus_words = {}
        for data in treino:
            url = data['link']
            url = self.Tokenize(url)
            class_name = data['classe']
            if class_name not in list(corpus_words.keys()):
                corpus_words[class_name] = {}
            for word in url:
                if word not in list(corpus_words[class_name].keys()):
                    corpus_words[class_name][word] = 1
                else:
                    corpus_words[class_name][word] += 1
            
        return corpus_words

    def CalcularScoreDaClasse(self, sentence, dados, class_name):
        score = 0
        sentence = self.Tokenize(sentence)
        for word in sentence: 
            if word in dados[class_name]:
                score += dados[class_name][word]
        
        return score

    def CalcularScore(self, url, dados):
        high_score = 0
        classname = 'default'
        for classe in dados.keys():
            pontos = 0
            pontos = self.CalcularScoreDaClasse(url, dados, classe)
            if pontos > high_score:
                high_score = pontos
                classname = classe
        
        return classname, high_score

if __name__ == '__main__':
    app.run(debug=True)