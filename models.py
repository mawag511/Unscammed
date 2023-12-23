import pickle
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

NBmodel = pickle.load(open("training/NB_model.pkl", "rb"))
NBvectorizer = pickle.load(open("training/NB_vectorizer.pkl", "rb"))

LGmodel = pickle.load(open("training/LG_model.pkl", "rb"))
LGvectorizer = pickle.load(open("training/LG_vectorizer.pkl", "rb"))

SVMmodel = pickle.load(open("training/SVM_model.pkl", "rb"))
SVMvectorizer = pickle.load(open("training/SVM_vectorizer.pkl", "rb"))