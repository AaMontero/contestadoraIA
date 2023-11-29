import random
import json
import pickle
import numpy as np
import tflearn
import tensorflow as tf
import nltk
from nltk.stem import WordNetLemmatizer #Para pasar las palabras a su forma raíz

#Para crear la red neuronal
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('intents.json','r', encoding='utf-8').read())

#nltk.download('punkt')
#nltk.download('wordnet')
#nltk.download('omw-1.4')

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '¿', '.', ',']

#Clasifica los patrones y las categorías
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern, language='spanish', preserve_line=True)
        words.extend(word_list)
        documents.append((word_list, intent["tag"]))
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

words = [lemmatizer.lemmatize(word, pos ='v') for word in words if word not in ignore_letters]
words = sorted(set(words))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

#Pasa la información a unos y ceros según las palabras presentes en cada categoría para hacer el entrenamiento
training = []
output_empty = [0]*len(classes)
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])
random.shuffle(training)
training = np.asarray(training, dtype="object") 
print(training) 

#Reparte los datos para pasarlos a la red
train_x = list(training[:,0])
train_y = list(training[:,1])


tf.compat.v1.reset_default_graph()
net = tflearn.input_data(shape=[None, len(training[0])])
net_h1 = tflearn.fully_connected(net, 8)
net_h2 = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0], activation="softmax"))
net = tflearn.regression(net)
model = tflearn.DNN(net)
#Creamos la red neuronal
'''
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

#Creamos el optimizador y lo compilamos
sgd = SGD(learning_rate=0.01,
    momentum=0.0,
    nesterov=False
    )
model.compile(loss='categorical_crossentropy', optimizer = sgd, metrics = ['accuracy'])
'''
model.fit(training,output_empty, n_epochs ="1000", batch_size =10, metrics = True)
#Entrenamos el modelo y lo guardamos
#train_process = model.fit(np.array(train_x), np.array(train_y), epochs=100, batch_size=5, verbose=1)
#model.save("chatbot_model.h5", train_process)
model.save("chatbot_model")