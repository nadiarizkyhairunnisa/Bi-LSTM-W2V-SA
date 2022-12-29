import numpy as np
import pandas as pd

class Processing:

    def label_encoding (data):
        # change rating to 1 & 2 -> 0 and 4 & 5 -> 1 
        data["sentiment"] = np.where((data["rating"] == 4) | (data["rating"] == 5), 1,
                            np.where((data["rating"] == 1) | (data["rating"] == 2), 0, 3))

        return data
    
    def drop_neutral_sentiment(data):
        # drop sentiment with rating 3
        data.drop(data.loc[data["sentiment"] == 3].index, inplace = True)
        data.reset_index(drop = True)
        
        return data
    
    def drop_rating_column(data):
        #drop rating column
        data.drop('rating', axis = 1, inplace = True)

        return data

    def change_column_type(data):
        #change sentiment column type from float into integer
        data["sentiment"] = data["sentiment"].astype('int')
        
        return data
