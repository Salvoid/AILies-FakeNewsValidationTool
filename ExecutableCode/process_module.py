# [Imports]====================================================================================================
import pandas as pd # For Dataset Manipulation
from sklearn.model_selection import train_test_split # For splitting training and testing dataset
from sklearn.naive_bayes import MultinomialNB # Multinomial Naive Bayes for frequency classification
from sklearn.metrics import accuracy_score # For accuracy rating
import seaborn as sns # Statistical Graphics
from sklearn.metrics import confusion_matrix # Confusion Matrix
import matplotlib.pyplot as plt # For Graphs and Plots
from sklearn.metrics import classification_report # For Performance Evaluation
import numpy as np # For Performance Evaluation
import pickle # For Saving Machine Learning Model
from sklearn.feature_extraction.text import CountVectorizer # For Computing Word Occurence
from sklearn.feature_extraction.text import TfidfTransformer # For Computing Word Frequency and Fitting to Model
import other_module as otherModule # Other needed functions


# [Functions]====================================================================================================
def import_dataset(in_socialMedia):
    if in_socialMedia == "twitter":
        path_dataset_csv = "\\assets\\datasets\\twitter_news_politics_dataset.csv"
    elif in_socialMedia == "facebook":
        path_dataset_csv = "\\assets\\datasets\\facebook_news_politics_dataset.csv"

    # Import Dataset from CSV File
    with open(otherModule.define_relativepath(True,path_dataset_csv), 'r') as file:
        raw_dataset = pd.read_csv(file)

    # Rename Column Headers
    raw_dataset.rename(columns={raw_dataset.columns[0]:'label', raw_dataset.columns[1]:'wordset'}, inplace=True)

    return raw_dataset

def process_dataset_train(in_df_dataset):
    # Word Occurence Method(Document Term Matrix)
    out_cv_countVect = CountVectorizer()
    X_dataset_dtm = out_cv_countVect.fit_transform(in_df_dataset.iloc[:, 1])

    # Word Frequency Method(Skip Redundant Processing)
    out_tf_tfidfTransformer = TfidfTransformer()
    out_X_dataset_tfidf = out_tf_tfidfTransformer.fit_transform(X_dataset_dtm)

    out_y_dataset_values = in_df_dataset.iloc[:, 0]
    
    return out_cv_countVect, out_tf_tfidfTransformer, out_X_dataset_tfidf, out_y_dataset_values

def process_dataset_test(in_cv_countVect, in_tf_tfidfTransformer, in_df_dataset):
    # Word Occurence Method(Document Term Matrix)
    X_dataset_dtm = in_cv_countVect.transform(in_df_dataset.iloc[:, 1])

    # Word Frequency Method
    out_X_dataset_tfidf = in_tf_tfidfTransformer.transform(X_dataset_dtm)

    out_y_dataset_values = in_df_dataset.iloc[:, 0]
    
    return out_X_dataset_tfidf, out_y_dataset_values

def train_model(in_X_dataset_train_tfidf, in_y_dataset_train_values):
    # Create Classifier/Model
    out_model = MultinomialNB()

    # Train Classifier/Model
    out_model.fit(X=in_X_dataset_train_tfidf, y=in_y_dataset_train_values)

    return out_model

def predict_model(in_model, in_X_dataset_test_tfidf):
    # Predict Testing Data using the Classifier/Model
    out_y_dataset_prediction = in_model.predict(X=in_X_dataset_test_tfidf)

    return out_y_dataset_prediction

def save_training(in_model_naivebayes_multinomial, in_cv_countVect, in_tf_tfidfTransformer, in_socialMedia):
    # Save Model to Directory
    f = open(otherModule.define_relativepath(True,"\\assets\\training\\model_naivebayes_multinomial_"+in_socialMedia+".pickle"), 'wb')
    pickle.dump(in_model_naivebayes_multinomial, f)
    f.close()

    # Save Count Vector Object to Directory
    f = open(otherModule.define_relativepath(True,"\\assets\\training\\cv_countVect_"+in_socialMedia+".pickle"), 'wb')
    pickle.dump(in_cv_countVect, f)
    f.close()

    # Save Transformer Object to Directory
    f = open(otherModule.define_relativepath(True,"\\assets\\training\\tf_tfidfTransformer_"+in_socialMedia+".pickle"), 'wb')
    pickle.dump(in_tf_tfidfTransformer, f)
    f.close()

def load_training(in_socialMedia):
    # Load Model to Directory
    f = open(otherModule.define_relativepath(False,"\\assets\\training\\model_naivebayes_multinomial_"+in_socialMedia+".pickle"), 'rb')
    out_model_naivebayes_multinomial = pickle.load(f)
    f.close()

    # Load Count Vector Object to Directory
    f = open(otherModule.define_relativepath(False,"\\assets\\training\\cv_countVect_"+in_socialMedia+".pickle"), 'rb')
    out_cv_countVect = pickle.load(f)
    f.close()

    # Load Transformer Object to Directory
    f = open(otherModule.define_relativepath(False,"\\assets\\training\\tf_tfidfTransformer_"+in_socialMedia+".pickle"), 'rb')
    out_tf_tfidfTransformer = pickle.load(f)
    f.close()

    return out_model_naivebayes_multinomial, out_cv_countVect, out_tf_tfidfTransformer

def compute_accuracy(in_y_dataset_test_values, in_y_dataset_prediction, in_cm_filename):
    # Compute Accuracy of Model Prediction(Using sklearn.metrics)
    model_accuracy = accuracy_score(y_true = in_y_dataset_test_values, y_pred = in_y_dataset_prediction)
    print("==================================================")
    print("NumPy Accuracy: ", model_accuracy)
    print("==================================================")

    # Compute Accuracy of Model Prediction(Using NumPy)
    model_accuracy = np.mean(in_y_dataset_prediction == in_y_dataset_test_values)
    print("Scikit Learn Accuracy: ", model_accuracy)
    print("==================================================")

    # Precision, Recall, F1-Score, Accuracy, Average
    model_report = classification_report(y_true = in_y_dataset_test_values, y_pred = in_y_dataset_prediction)
    print(model_report)
    print("==================================================")

    # Set Confusion Matrix
    cm_prediction = confusion_matrix(y_true = in_y_dataset_test_values, y_pred = in_y_dataset_prediction)
    print("----------")
    print("Confusion Matrix")
    print("----------")
    print(cm_prediction)
    print("----------")
    print("==================================================")
    # Set Confusion Matrix Heatmap
    sns.heatmap(cm_prediction, annot=True, fmt='g', xticklabels = ["Fake","Real"], yticklabels = ["Fake","Real"])
    # Additional Plot Settings
    plt.xlabel("Predicted Values")
    plt.ylabel("True Values")
    # Save Confusion Matrix to Image
    plt.savefig(otherModule.define_relativepath(True,in_cm_filename))
    plt.close()

    # print(in_y_dataset_test_values, "---", in_y_dataset_prediction)
