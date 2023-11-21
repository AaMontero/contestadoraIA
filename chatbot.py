import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

lemmatizer = WordNetLemmatizer()

class ChatBot:
    def __init__(self):
        # Importamos los archivos generados en el código anterior
        self.intents = json.loads(open('intents.json').read())
        self.words = pickle.load(open('words.pkl', 'rb'))
        self.classes = pickle.load(open('classes.pkl', 'rb'))
        self.model = load_model('chatbot_model.h5')

    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
        return sentence_words

    def bag_of_words(self, sentence):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(self.words)
        for w in sentence_words:
            for i, word in enumerate(self.words):
                if word == w:
                    bag[i] = 1
        return np.array(bag)

    def predict_class(self, sentence):
        bow = self.bag_of_words(sentence)
        res = self.model.predict(np.array([bow]))[0]
        max_index = np.where(res == np.max(res))[0][0]
        category = self.classes[max_index]
        return category

    def get_response(self, tag):
        list_of_intents = self.intents['intents']
        result = ""
        for i in list_of_intents:
            if i["tag"] == tag:
                result = random.choice(i['responses'])
                break
        return result

    def chat_loop(self, transcriber_result):
        ints = self.predict_class(transcriber_result)
        res = self.get_response(ints)
        print(res)
        return res

