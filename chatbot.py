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
        self.confirmoIdentidad = self.ofrecioPromocion = self.estadoCivilBoolean = self.DireccionHorariosBoolean = self.agendoCitaBoolean = self.DocumentosNBoolean = False 
        self.preguntasTarjeta = 2; 
        self.intents = json.loads(open('intents.json').read())
        self.words = pickle.load(open('words.pkl', 'rb'))
        self.classes = pickle.load(open('classes.pkl', 'rb'))
        self.model = load_model('chatbot_modelo.h5')

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
        
    def obtenerIndices(self,arreglo, etiquetas):
        indices = []
        for i, elemento in enumerate(arreglo):
            if elemento in etiquetas:
                indices.append(i)
        return indices 
    
    def modificarLista(self, lista, etiquetas, multiplica):
        print(etiquetas)
        indices = self.obtenerIndices(self.classes, etiquetas)
        for indice in indices: 
            lista[indice] *= multiplica   
        return lista
    
    def predict_class(self, sentence):
        
        bow = self.bag_of_words(sentence)
        res = self.model.predict(np.array([bow]))[0]
        clasesIdentidad = {"confirmaIdentidad","negacionIdentidad","noSeEncuentra"}
        estadoCivilEtiq = {"estadoCivilCasado","estadoCivilSoltero"}
        preguntasEtiq = {"plazoTarjetaGift","razonesGiftCard","queEsGiftCard","activacionRecarga","utilizarTarjeta", "plazoTarjetaGift", "CostosGiftcard", "activacionGift"}
        direccionHorariosEtiq = {"HorarioAgencia", "direccionRepetir", "direccion y horarios"}
        documentosEtiq = {"utilizarTarjeta"}
        beneficiosFamilia = {"beneficiosFamilia"}
        
        if(self.confirmoIdentidad == False):
            res = self.modificarLista(res, clasesIdentidad, 2)
            self.confirmoIdentidad = True
        elif(self.confirmoIdentidad and not (self.ofrecioPromocion and self.DireccionHorariosBoolean and not self.estadoCivilBoolean)):
            res = self.modificarLista(res, preguntasEtiq, 1.5)
            if(self.preguntasTarjeta<=1):
                self.ofrecioPromoción = True 
        elif(self.confirmoIdentidad and self.ofrecioPromocion==False): 
            res = self.modificarLista(res, direccionHorariosEtiq, 2) 
            self.DireccionHorariosBoolean = True 
        elif(self.confirmoIdentidad and self.ofrecioPromocion and self.DireccionHorariosBoolean): 
            res = self.modificarLista(res, self.estadoCivilBoolean, 2)
            self.estadoCivilBoolean = True
        elif(self.confirmoIdentidad and self.ofrecioPromocion and self.DireccionHorariosBoolean and not self.estadoCivilBoolean): 
            res = self.modificarLista(res, estadoCivilEtiq, 2)
            res = self.modificarLista(res, beneficiosFamilia, 2)
        elif(self.confirmoIdentidad and self.ofrecioPromocion and self.DireccionHorariosBoolean and not self.DocumentosNBoolean): 
            res = self.modificarLista(res, documentosEtiq, 2)
            self.DocumentosNBoolean = True 
        max_index = np.where(res == np.max(res))[0][0]
        category = self.classes[max_index]
        for index, respuesta in enumerate (res):
            print(self.classes[index], respuesta) 
        return category,res 

    def get_response(self, tag):
        list_of_intents = self.intents['intents']
        result = ""
        for i in list_of_intents:
            if i["tag"] == tag:
                result = random.choice(i['responses'])
                break
        return result

    def chat_loop(self, transcriber_result):
        ints, resValUno = self.predict_class(transcriber_result) #Regresa la categoria
        if(ints == "Despedida"): 
            return "Muy amable, hasta luego"
        res = self.get_response(ints)
        return res, resValUno
    
def mainBot(): 
    chatBot = ChatBot()
    while True: 
        entrada = input("Tu: ")
        respuesta = chatBot.chat_loop(entrada)
        print("Bot: " ,respuesta)
        if(respuesta == "Muy amable, hasta luego"):
            break

#mainBot()

