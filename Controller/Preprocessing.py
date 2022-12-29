from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Model.DataReader import DataReader
import re


class Preprocessing:
    
    def remove_duplicates (data, data_subset):
        print ("run duplicate data removal")
        data.drop_duplicates(subset = data_subset, keep = 'last', inplace = True)
        data.reset_index(drop = True, inplace = True)

        return data

    def text_cleaning(text):
        print("run text cleaning")
        #remove @username 
        text = re.sub('@[^\s]+',' ', str(text))
        #remove #hastag
        text = re.sub('#[^\s]+',' ', str(text))
        #remove URLs
        text = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', str(text))
        #remove punctuations
        text = re.sub(r'[^\w]|_',' ',str(text))
        #remove digit from string
        text = re.sub(r"\d+", "", text)
        #remove digit or numbers
        text = re.sub(r"\b\d+\b", " ", str(text))
        #to lowercase/case-folding
        text = text.lower()
        #Remove additional white spaces
        text = re.sub('[\s]+', ' ', str(text))
        # print("finsihed text cleaning")

        return text

    def word_correction(text, slang_dictionary):
        print("run word correction")
        word = [word.replace(word, slang_dictionary[word]) if word in slang_dictionary else word for word in text.split() ]
        text = ' '.join(word)
        # print("finished word correction")

        return text
    
    def stemming(text):
        print("run stemming")
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        word = [stemmer.stem(word) for word in text.split()]
        result = ' '.join(word)
        # print("finished stemming")

        return result

    def stopword_removal(text, stopword_list):
        print("run stopwords removal")
        word = [word for word in text.split() if word not in stopword_list]
        result = ' '.join(word)
        # print("finished stopwords removal")

        return result
        

    # def apply_function (self, data, column, function_name):
    #     #apply function with swifter library to speed up the process
    #     data[column] = data[column].swifter.apply(function_name)

    #     return data

    # def run(data, column_name):
    #     print("run text preprocessing")

    #     # text = data[column_name]

    #     result = text_cleaning(text = remove_duplicates(data = data, data_subset = column_name))

    #     return result    
        
        

  