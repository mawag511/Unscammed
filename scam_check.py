from models import *

''' loading the Naive-Bayes model and making the prediction '''
def NB_message_classified(submitted_message):
    message = [submitted_message]
    message_count = NBvectorizer.transform(message)
    NBpred = NBmodel.predict(message_count)
    return NBpred[0]
 
''' loading the Logistic Regression model and making the prediction '''
def LG_message_classified(submitted_message):
    message = [submitted_message]
    message_count = LGvectorizer.transform(message)
    LGpred = LGmodel.predict(message_count)
    return LGpred[0]

''' importing the Word Count algorithm and making the prediction, by first pre-processing the input message '''
def SVM_message_classified(submitted_message):
    message = [submitted_message]
    message_count = SVMvectorizer.transform(message)
    SVMpred = SVMmodel.predict(message_count)
    return SVMpred[0]

def message_check(input):
    NB_classification = NB_message_classified(input)
    LG_classification = LG_message_classified(input)
    SVM_classification = SVM_message_classified(input)

    if NB_classification == 0:
        NB_classification_result = "Check via Naive-Bayes Classification Algorithm → Likely not a scam"
    else:
        NB_classification_result = "Check via Naive-Bayes Classification Algorithm → Likely a scam"

    if LG_classification == 0:
        LG_classification_result = "Check via Logistic Regression Classification Algorithm → Likely not a scam"
    else:
        LG_classification_result = "Check via Logistic Regression Classification Algorithm → Likely a scam"

    if SVM_classification == 0:
        SVM_classification_result = "Check via Support Vector Machine Classification Algorithm → Likely not a scam"
    else:
        SVM_classification_result = "Check via Support Vector Machine Classification Algorithm → Likely a scam"
      
    return  NB_classification_result + "\n\n" + LG_classification_result + "\n\n" + SVM_classification_result
