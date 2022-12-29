from flask import Flask, request
from flask_restful import reqparse, Api, Resource
from Controller.Preprocessing import Preprocessing
from Controller.Modeling import Modeling
from Model.DataReader import DataReader
from keras.models import load_model
from flask_cors import CORS

class App:

    app = Flask(__name__)
    CORS(app)

    global first_tokenizer_path, second_tokenizer_path, colloquial_lexicon_path, stopword_list_path, first_model_path, second_model_path, third_model_path
    
    first_tokenizer_path    = "D:/informatics/codes/thesis/Assets/Tokenizer/tokenizer_base_stem.pickle"
    second_tokenizer_path   = "D:/informatics/codes/thesis/Assets/Tokenizer/tokenizer_tuned_stem.pickle"
    colloquial_lexicon_path = "D:/informatics/codes/thesis/Assets/Data/wordlist/colloquial_indonesian_lexicon.csv"
    stopword_list_path      = "D:/informatics/codes/thesis/Assets/Data/wordlist/idn_stopwords.txt"
    first_model_path        = "D:/informatics/codes/thesis/Assets/Model/BiLSTM_best_weights_stem_base.h5"
    second_model_path       = "D:/informatics/codes/thesis/Assets/Model/BiLSTM_best_weights_stem_tuned.h5"
    third_model_path        = "D:/informatics/codes/thesis/Assets/Model/BiLSTM.h5"


    @app.route('/', methods=["GET","POST"])
    def predictSentiment():

        ulasan = request.form.get("ulasan")
        preprocOption = request.form.get("preproc")
        print("PREPROC OPTION VALUES", preprocOption)

        modelOption = request.form.get("model")
        print("MODEL OPTION VALUES", modelOption)

        if preprocOption == "1":
            ulasan = Preprocessing.text_cleaning(ulasan)
            print("masuk text cleaning")
        else:
            ulasan = Preprocessing.text_cleaning(ulasan)
            print("finsihed text cleaning: ", ulasan)

            colloquial_lexicon =  DataReader.get_slang_dictionary(colloquial_lexicon_path)
            ulasan = Preprocessing.word_correction(ulasan, colloquial_lexicon)
            print("finsihed word correction: ", ulasan)

            stopword_list = DataReader.get_stopword_list(stopword_list_path)
            print(stopword_list)
            ulasan = Preprocessing.stopword_removal(ulasan, stopword_list)
            print("finsihed stopword_removal:", ulasan)

            ulasan = Preprocessing.stemming(ulasan)
            print("finshed text stemming:", ulasan)

        model = None
        if modelOption == "1":
            model       = load_model(first_model_path, custom_objects={"f1_m": Modeling.f1_m, "precision_m": Modeling.precision_m, "recall_m": Modeling.recall_m})
            
        else:
            model = load_model(second_model_path, custom_objects={"f1_m": Modeling.f1_m, "precision_m": Modeling.precision_m, "recall_m": Modeling.recall_m})
            

        tokenizer   = DataReader.get_tokenizer(first_tokenizer_path)
        ulasan_seq  = Modeling.get_seq(review = ulasan, tokenizer = tokenizer)
        result      = Modeling.predict_sentiment(model, ulasan_seq)
        print(ulasan)
        print(result)

        return {"ulasan": ulasan,
                "preproc": preprocOption,
                "model": modelOption,
                "result": result} 


    @app.route('/modeling', methods=["GET", "POST"]) 
    def getEvaluationData():
        data_option = request.form.get("data_option")
        print("DATA OPTION VALUES: ", data_option)

        if data_option == "base_clean_train":
            data_path = "../Assets/Data/evaluation/base_clean_train.csv"
        elif data_option == "base_clean_test":
            data_path = "../Assets/Data/evaluation/base_clean_test.csv"
        elif data_option == "base_stem_train":
            data_path = "../Assets/Data/evaluation/base_stem_train.csv"
        elif data_option == "base_stem_test":
            data_path = "../Assets/Data/evaluation/base_stem_test.csv"
        elif data_option == "tuned_clean_train":
            data_path = "../Assets/Data/evaluation/tuned_clean_train.csv"
        elif data_option == "tuned_clean_test":
            data_path = "../Assets/Data/evaluation/tuned_clean_test.csv"
        elif data_option == "tuned_stem_train":
            data_path = "../Assets/Data/evaluation/tuned_stem_train.csv"
        else:
            data_path = "../Assets/Data/evaluation/tuned_stem_test.csv"

        return {"data_path":data_path}

    @app.route('/dataset', methods=["GET", "POST"]) 
    def getSampleData():
        data_option = request.form.get("data_option")
        print("DATA OPTION VALUES: ", data_option)

        if data_option == "data_table":
            data_path = "../Assets/Data/sample/data_clean_sample_final.csv"
        elif data_option == "data_table_2":
            data_path = "../Assets/Data/sample/data_stem_sample_final.csv"
        elif data_option == "stem_train":
            data_path = "../Assets/Data/sample/data_stem_sample_final.csv"
        else:
            data_path = "../Assets/Data/sample/data_stem_sample_final.csv"

        return {"data_path":data_path}


    if __name__ == '__main__':
        app.run(debug=True)


    #---------------------------------------------------------------------------------------------------
    # When Pre-processing options are still checkboxes

    # @app.route('/', methods=["POST"])
    # def SentimentAnalysis():
        # try:
        # ulasan = request.form.get("ulasan")
        # return {"ulasan": ulasan}
    
        # checkbox_value = request.form.getlist("checkbox[]")
        # print("CHECKBOX VALUE: ", checkbox_value)
        # # if request.form.get("textCleaning") == "true":
        # if "1" in request.form.getlist("checkbox[]") :
        #     ulasan = Preprocessing.text_cleaning(ulasan)
        #     print("masuk text cleaning")
        # # if request.form.get("stemming") == "true":
        # if "2" in request.form.getlist("checkbox[]") :
        #     ulasan = Preprocessing.text_cleaning(ulasan)
        #     print("masuk text cleaning")
        #     ulasan = Preprocessing.stemming(ulasan)
        #     print("masuk text stemming")
        #     ulasan = Preprocessing.word_correction(ulasan)
        #     print("masuk word correction")

    #---------------------------------------------------------------------------------------------------


    # from flask import Flask, request
    # from flask_restful import reqparse, Api, Resource
    # from Controller.Preprocessing import Preprocessing
    # from Controller.Modeling import Modeling
    # from keras.models import load_model
    # from flask_cors import CORS

    # app = Flask(__name__)
    # CORS(app)
    # api = Api(app)

    # parser = reqparse.RequestParser()
    # parser.add_argument('nlParam')


    # class SentimentAnalysis(Resource):
    #     def post(self):
    #         # __Ulasan = parser.parse_args()
    #         # result = "Hello World"
    #         ulasan = request.form.get("ulasan")

    #         # if request.form.get("textCleaning") == "true":
    #         if "1" in request.form.get("checkbox") :
    #             ulasan = Preprocessing.text_cleaning(ulasan)
    #             print("masuk text cleaning")

    #         # if request.form.get("stemming") == "true":
    #         if "2" in request.form.get("checkbox") :
    #             print("masuk stemming")
    #             ulasan = Preprocessing.stemming(ulasan)
        
    #         # if request.form.get("wordCorrection") == "true":
    #         if "3" in request.form.get("checkbox") :
    #             print("masuk word correction")
    #             ulasan = Preprocessing.word_correction(ulasan)


    #         modelOption = request.form.get("model")
    #         ulasan = Modeling.get_seq(review = ulasan, NUM = 100000, SENTENCE_LENGTH = 300)

    #         model = None
    #         if modelOption == "1":
    #             model = load_model("ac_model.h5")
    #         elif modelOption == "2":
    #             model = load_model("ac_undersampled_model.h5")
    #         else:
    #             model = load_model("BiLSTM_model.h5")

    #         ulasan = Modeling.predict_sentiment(model, ulasan)

    #         return {"ulasan": ulasan}


    # api.add_resource(SentimentAnalysis, '/')

    # if __name__ == '__main__':
    #     app.run(debug=True)
