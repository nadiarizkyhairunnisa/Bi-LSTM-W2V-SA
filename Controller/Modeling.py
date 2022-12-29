import numpy as np
import tensorflow as tf
import gensim
import pandas as pd
import pickle

from collections import Counter #to count occurences 
from gensim.models import word2vec
from imblearn.under_sampling import RandomUnderSampler
from keras import backend as K
from keras import metrics
from keras.callbacks import ModelCheckpoint
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences  #for padding our text
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Embedding, LSTM, Bidirectional
from sklearn.model_selection import train_test_split


class Modeling:


    def split_data(data):
        print("run data splitting")
        X = data["review"].astype(str) #review data
        y = data["sentiment"] #label data

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

        print("Jumlah data training: {}".format(len(X_train)))
        print("Jumlah data testing: {}".format(len(X_test)))
        print("Jumlah sentimen positif: {}".format(len(data[data["sentiment"] == 1])))
        print("Jumlah sentimen negatif: {}".format(len(data[data["sentiment"] == 0])))

        return X_train, X_test, y_train, y_test


    def get_sequences(X_train, X_test):
        print("run data tokenizing and padding") 
        tokenizer = Tokenizer(num_words = 100000)
        tokenizer.fit_on_texts(X_train)

        X_train_seq = tokenizer.texts_to_sequences(X_train)
        X_train_seq_pad = pad_sequences(X_train_seq, maxlen = 100)
        
        X_test_seq = tokenizer.texts_to_sequences(X_test)
        X_test_seq_pad = pad_sequences(X_test_seq, maxlen = 100)

        return X_train_seq_pad, X_test_seq_pad, tokenizer

    def get_seq(review, tokenizer):
        print("run data tokenizing and padding") 
        review_seq = tokenizer.texts_to_sequences([review])
        return pad_sequences(review_seq, maxlen = 100)

    def create_embedding_matrix(w2v_model, tokenizer):
        print("run create embedding matrix using Word2Vec")
        DIM = w2v_model.vector_size 
        embedding_matrix = np.zeros((100000, DIM))

        for word, i in tokenizer.word_index.items():
            if i >= 100000:
                break
            if word in w2v_model.wv.key_to_index.keys():
                embedding_matrix[i] = w2v_model.wv[word]
        print("Embedding Matrix Shape:", embedding_matrix.shape)

        return embedding_matrix, DIM


    def undersample_data(X_train, y_train):
        rus = RandomUnderSampler(random_state = 42, sampling_strategy = 0.5)
        X_train_rus, y_train_rus = rus.fit_resample(X_train, y_train)

        print('Original dataset shape:', Counter(y_train))
        print('Resample dataset shape:', Counter(y_train_rus))

        return X_train_rus, y_train_rus

    def recall_m(y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())

        return recall

    def precision_m(y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())

        return precision

    def f1_m(y_true, y_pred):
        precision = precision_m(y_true, y_pred)
        recall = recall_m(y_true, y_pred)

        return 2*((precision*recall)/(precision+recall+K.epsilon()))


    def get_model(DIM, weights):

        #initialize an embedding layer
        embedding_layer = Embedding(input_dim = 100000,
                                    output_dim = DIM,
                                    weights = [weights],
                                    input_length = 100,
                                    trainable = False)
        #initialize a model
        model = Sequential([embedding_layer,
                            Bidirectional(LSTM(64)),
                            Dropout(0.5),
                            Dense(1, activation = 'sigmoid')],
                            name = "Model") 
        #compile model 
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=[
                        metrics.TruePositives(),
                        metrics.TrueNegatives(),
                        metrics.FalsePositives(),
                        metrics.FalseNegatives(),
                        'accuracy',
                        f1_m, 
                        precision_m, 
                        recall_m,
                        ])
    
        print(model.summary())

        return model


    def train_test_model (model, X_train, y_train, X_test, y_test):
        checkpoint = ModelCheckpoint(filepath = "BiLSTM_best_weights.h5", monitor='val_recall_m', verbose=1, save_best_only=True, mode='max')
        early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_recall_m', mode = 'max', patience= 20)
        history = model.fit(X_train, y_train, validation_data=[X_test, y_test], epochs=200, batch_size=128, verbose = 1, callbacks = [checkpoint, early_stopping])
        print(history.history['loss'])
        print(history.history['accuracy']) 
        print(history.history['recall_m'])
        print(history.history['precision_m'])
        print(history.history['f1_m'])

        return history.history
    

    def save_model(model, model_name):
        return model.save("{}.h5".format(model_name))
    

    def save_model_evaluation(model_history):
        # convert the history.history dict to a pandas DataFrame   
        model_evaluation = pd.DataFrame(model_history) 

        # save evaluation result to csv
        path = r'D:\TI 18\codes-vscode\thesis\product-review\evaluation\model_eval.csv'
        print("saving model evaluation result into {}".format(path))
        model_evaluation.to_csv(path) 

        return model_evaluation

    def predict_sentiment(model, review_seq):
        sentiment_seq = model.predict(review_seq)
        print("predict", sentiment_seq)
        print(sentiment_seq.shape)
        sentiment_seq = np.transpose(sentiment_seq)[0]
        print("predict", sentiment_seq)
        print(sentiment_seq.shape)
        print("sentiment seq", sentiment_seq)
        if(sentiment_seq < 0.6 ):
            label = "negatif"
        else:
            label = "positif"
        result = "Ulasan produk bersentimen {} dengan nilai polaritas sebesar {}".format(label, sentiment_seq)

        return result
    



    




        
        