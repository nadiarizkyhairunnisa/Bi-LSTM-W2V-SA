import csv
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import itertools #to final result
import gensim
from gensim.models import word2vec



#load model
namaFileModel = "idwiki_word2vec_300_new_lower.model"
model = gensim.models.Word2Vec.load(namaFileModel)
my_dict = dict({})
for idx, key in enumerate(model.wv.key_to_index):
    # my_dict[key] = model.wv.key_to_index.keys()
    my_dict[key] = model.wv.word_vec(key)
    # print(my_dict[key])
    # Or my_dict[key] = model.wv.get_vector(key)


