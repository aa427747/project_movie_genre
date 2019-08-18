# Name:          Movie Genre Prediction Application
# Created by:    Ryan Gfeller,  Claudia Gomez-Beltran
# Created date:  June 23, 2019
# Description:  This is the Genre prediction model that has been saved.  
#               The Fit / Train / Test / Predict is contained in the GenrePrection.ipynb and 
#               Genre_Call_Run_Preduction_v2.ipnyb.     

import pandas as pd
import numpy as np
import json
import nltk
import re
import csv
import matplotlib.pyplot as plt 
import seaborn as sns
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import f1_score
from sklearn.preprocessing import MultiLabelBinarizer
from nltk.corpus import stopwords

# function for text cleaning 
def clean_text(text):
    # remove backslash-apostrophe 
    text = re.sub("\'", "", text) 
    # remove everything except alphabets 
    text = re.sub("[^a-zA-Z]"," ",text) 
    # remove whitespaces 
    text = ' '.join(text.split()) 
    # convert text to lowercase 
    text = text.lower() 
    
    return text

# nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# function to remove stopwords
def remove_stopwords(text):
    no_stopword_text = [w for w in text.split() if not w in stop_words]
    return ' '.join(no_stopword_text)


# load the model from disk
modelname = 'movie_genrepredict.sav'
clf = pickle.load(open(modelname, 'rb'))

transformname = 'movie_genretranformpredict.sav'
tfidf_vectorizer = pickle.load(open(transformname, 'rb'))

multiname = 'movie_genreyvaluepredict.sav'
multilabel_binarizer = pickle.load(open(multiname, 'rb'))

def infer_tags_prob(q, t=0.3):
    q = clean_text(q) ## Defined function for clean
    q = remove_stopwords(q) ## Defined function for removing stop words
    q_vec = tfidf_vectorizer.transform([q]) ##create TF-IDF features 
    q_pred = clf.predict_proba(q_vec) ## The models predict.
    q_pred_new = (q_pred >= t).astype(int)
    return multilabel_binarizer.inverse_transform(q_pred_new)


movie_plot = "This food was absolutely the worst thing I have ever eaten, stomach thought I was eating Taco Bell and tongue thought I was eating dirt."
# print("Predicted genre: ", infer_tags_prob(movie_plot))
print("Predicted genre: ", ', '.join(infer_tags_prob(movie_plot)[0]))
