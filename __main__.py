from Model.DataReader import DataReader
from Controller.Preprocessing import Preprocessing
from Controller.Processing import Processing
from Controller.Modeling import Modeling
import swifter
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences  #for padding our text

class __main__2:
    tokenizer_path = "D:/informatics/codes/thesis/Assets/Tokenizer/tokenizer_stem.pickle"
    model_path = "D:/informatics/codes/thesis/Assets/Model/BiLSTM_best_weights.h5"
    
    # ulasan = "order"
    # ulasan = "terima kasih realpict ya suka"
    ulasan = "tidak amanah"
    # ulasan = "jualan itu yg amanah mba biar berkah hidupnya mintanya apa krimnya apa minta wrna apa kirimnya wrna apa alhasil tu brg gua buang deh ke tong sampah anggap aja w sedekah sama pengemis nyesell bgt belanja di toko ini bgi yg mau blanja ditoko ini mending jangan deh drpd kecewa"
    # ulasan = ["jelek parah terus lambat ih", "produk bagus banget cepet samppainya kurir juga ramah penjual respon cepat"]

    ulasan = Preprocessing.word_correction(Preprocessing.stemming(Preprocessing.text_cleaning(ulasan)))
    tokenizer = DataReader.get_tokenizer(tokenizer_path)
    ulasan = Modeling.get_seq(review = ulasan, tokenizer = tokenizer)
    model = load_model(model_path, custom_objects={"f1_m": Modeling.f1_m, "precision_m": Modeling.precision_m, "recall_m": Modeling.recall_m})
    ulasan = Modeling.predict_sentiment(model, ulasan)
    print(ulasan)
    