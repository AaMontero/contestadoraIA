import random
import PIL
import json
import pickle
import numpy as np
import tflearn
import tensorflow as tf
from tensorflow.python.util.nest import is_sequence_or_composite
import nltk
from nltk.stem import WordNetLemmatizer #Para pasar las palabr,,as a su forma raíz
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer() 

nltk.download("punkt")

with open ("intents.json", encoding='utf-8') as archivo: 
    datos = json.load(archivo)
    
try:
    with open ("variables.pickle", "rb") as archivoPickel: 
        palabras, tags, entrenamiento, salida = archivoPickel.load(archivoPickel)
except: 
    palabras = []
    tags = []
    auxX = []
    auxY =[]
    for contenido in datos["intents"]: 
        for patrones in contenido["patterns"]: 
            auxPalabra = nltk.word_tokenize(patrones)
            palabras.extend(auxPalabra)
            auxX.append(auxPalabra)
            auxY.append(contenido["tag"])
            if(contenido["tag"] not in tags): 
                tags.append(contenido["tag"])
                
                
    palabras = [stemmer.stem(w.lower()) for w in palabras if w!="?"]
    palabras = sorted(list(set(palabras)))
    tags = sorted(tags)
    print(tags)
    entrenamiento = []
    salida = []
    salidaVacia = [0 for _ in range (len(tags))]
    for x, documento in enumerate(auxX): 
        cubeta = []
        auxPalabra = [stemmer.stem(w.lower()) for w in documento]
        for w in palabras: 
            if w in auxPalabra:
                cubeta.append(1)
            else: 
                cubeta.append(0)
        filaSalida = salidaVacia[:]   
        filaSalida[tags.index(auxY[x])]= 1
        entrenamiento.append(cubeta)
        salida.append(filaSalida)
    entrenamiento = np.array(entrenamiento)
    salida = np.array(salida)
    with open ("variables.pickle","wb") as archivoPickle:
        pickle.dump((palabras,tags,entrenamiento,salida), archivoPickle)
tf.compat.v1.reset_default_graph()
red = tflearn.input_data(shape=[None, len(entrenamiento[0])])
red = tflearn.fully_connected(red, 10)
red = tflearn.fully_connected(red, 10)
net = tflearn.fully_connected(red, len(salida[0]), activation="softmax")
net = tflearn.regression(net)   
modelo = tflearn.DNN(net)    
try: 
    modelo.load("modelo_fully_connected")
except: 

    modelo.fit(entrenamiento, salida, n_epoch = 1000, batch_size = len(palabras), show_metric = True)
    modelo.save("modelo_fully_connected")
def mainBot(): 
    while True: 
        entrada = input("Tu: ")
        cubeta = [0 for _ in range (len(palabras))]
        entradaProcesada =nltk.word_tokenize(entrada)
        entradaProcesada =[stemmer.stem(palabra.lower()) for palabra in entradaProcesada]
        for palabraIndividual in entradaProcesada: 
            for i,palabra   in enumerate(palabras): 
                if(palabra== palabraIndividual): 
                    cubeta[i] = 1
        resultados = modelo.predict([np.array(cubeta)])
        for indice, resultado in enumerate(resultados[0]):
            if indice < len(tags):
                print(f"Resultado: {resultado}, Tag: {tags[indice]}")
            else:
                print(f"No hay un tag correspondiente para el resultado: {resultado}")
        resultadosIndices = np.argmax(resultados)
        tag = tags[resultadosIndices]
        print("resultado max:", tags[resultadosIndices])
        for tagAux in datos["intents"]: 
            if tagAux["tag"] == tag: 
                respuesta = tagAux ["responses"]
        print("Bot: ", random.choice(respuesta))
mainBot() 