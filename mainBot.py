import nltk
import numpy as np
import random 
from nltk.stem import WordNetLemmatizer #Para pasar las palabras a su forma raíz
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer() 
def mainBot(): 
    while True: 
        entrada = input("Tu: ")
        cubeta = [0 for _ in range len(palabras)]
        entradaProcesada =nltk.word_tokenize(entrada)
        entradaProcesada =[stemmer.stem(palabra.lower()) for palabra in entradaProcesada]
        for palabraIndividual in entradaProcesada: 
            for i,palabra   in enumerate(palabras): 
                if(palabra== palabraIndividual): 
                    cubeta[i] = 1
        resultados = modelo.predict([np.array(cubeta)])
        resultadosIndices = np.argmax(resultados)
        tag = tags[resultadosIndices]
        
        for tagAux in datos["contenido"]: 
            if tagAux["tag"] == tag: 
                respuesta = tagAux ["respuestas"]
        print("Bot: ", random.choice(respuesta))
mainBot()                    