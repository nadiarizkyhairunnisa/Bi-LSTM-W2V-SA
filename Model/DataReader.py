import pandas as pd
import glob
import os
import gensim
from pathlib import Path
import pickle

class DataReader:

    def get_dataset_dir (path):
        path = Path(path)
        all_files = [f for f in path.glob('**/*') if f.is_file()]
        dataset = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)

        return dataset

    def get_dataset_folder (path):
        path = Path(path)
        all_files = glob.glob(os.path.join(path , "*.csv"))
        dataset = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)

        return dataset

    def get_data(path):
        data = pd.read_csv(path)

        return data

    def get_slang_dictionary(path):
        slang_dictionary = {} #intialize new dict for our new dictionary
        slang_document = pd.read_csv(path) #read original slang csv file
        for i, row in slang_document.iterrows():
            slang_dictionary[row["slang"]] = row["formal"] #take needed columns only, slang and formal columns

        return slang_dictionary

    def get_tokenizer(path):
        with open(path, 'rb') as handle:
            tokenizer = pickle.load(handle)

        return tokenizer

    def get_w2v_model(path):
        w2v_model = gensim.models.Word2Vec.load(path)

        return w2v_model

    def get_stopword_list(path):
        stopword_file = open(path, "r")
        # reading the file
        stopword_list = stopword_file.read()
        # replacing end splitting the text when newline ('\n') is seen.
        final_stopword_list = stopword_list.split("\n")

        return final_stopword_list