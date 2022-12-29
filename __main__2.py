from Model.DataReader import DataReader
from Controller.Preprocessing import Preprocessing
from Controller.Processing import Processing
from Controller.Modeling import Modeling


import swifter


class __main__2:
    data_path = ("D:/TI 18/codes-vscode/thesis/product-review/dataset/air purifier")
    word2vec_path = "word2vec/idwiki_word2vec_300_new_lower.model"
    data = DataReader.get_dataset_folder(path = data_path)
    word2vec_model = DataReader.get_w2v_model(path = word2vec_path) 

    #Preprocessing
    data["review"] = (Preprocessing.remove_duplicates(data = data, data_subset = 'review')["review"].swifter.apply(
                        Preprocessing.text_cleaning)).swifter.apply(
                            Preprocessing.stemming).swifter.apply(
                                Preprocessing.word_correction)


    #Processing                        
    data = Processing.change_column_type(data=
                Processing.drop_rating_column(data = 
                    Processing.drop_neutral_sentiment(data = 
                        Processing.label_encoding(data = data))))

    #Modeling

    # Split dataset into training and testing data and label
    X_train, X_test, y_train, y_test = Modeling.split_data(data = data)
    # Tokenizing and padding dataset
    X_train, X_test, tokenizer = Modeling.get_sequences(X_train = X_train, X_test = X_test) 
    # Create embedding matrix using Word2Vec
    embedding_matrix, DIM = Modeling.create_embedding_matrix(w2v_model = word2vec_model, tokenizer = tokenizer)
    # Undersample dataset to make it balance
    X_train, y_train = Modeling.undersample_data(X_train, y_train)
    # Create model Bi-LSTM
    BiLSTM_model = Modeling.get_model(DIM = DIM, weights = embedding_matrix) 
    # Training and testing model to dataset
    history_BiLSTM_model = Modeling.train_test_model(model = BiLSTM_model, X_train = X_train, y_train = y_train, X_test = X_test, y_test = y_test)
    # Save model performance
    BiLSTM_model_eval = Modeling.save_model_evaluation(history_BiLSTM_model)
    # Save model
    Modeling.save_model(model = BiLSTM_model, model_name = "BiLSTM_W2V_model")




    # data.to_csv(r'D:\TI 18\codes-vscode\thesis\product-review\py\data_air_py_encoding.csv')

