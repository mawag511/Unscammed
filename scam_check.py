import pickle
from training import merged_dataset_training

   
''' loading the Naive-Bayes model and making the prediction '''
def NB_message_classified(submitted_message):
    NBmodel = pickle.load(open("training/NB_scam_detection_model.pkl", "rb"))
    NBvectorizer = pickle.load(open("training/NBvectorizer.pkl", "rb"))
    message = [submitted_message]
    message_count = NBvectorizer.transform(message)
    NBpred = NBmodel.predict(message_count)
    return NBpred[0]
 
''' loading the Logistic Regression model and making the prediction '''
def LG_message_classified(submitted_message):
    LGmodel = pickle.load(open("training/LG_scam_detection_model.pkl", "rb"))
    LGvectorizer = pickle.load(open("training/LGvectorizer.pkl", "rb"))
    message = [submitted_message]
    message_count = LGvectorizer.transform(message)
    LGpred = LGmodel.predict(message_count)
    return LGpred[0]

''' importing the Word Count algorithm and making the prediction, by first pre-processing the input message '''
def WC_message_classified(submitted_message):
    result = merged_dataset_training.predict(merged_dataset_training.pre_process(submitted_message))
    return result


def message_check(input):
    global NB_classification_result 
    global LG_classification_result
    global WC_classification_result

    NB_classification = NB_message_classified(input)
    LG_classification = LG_message_classified(input)
    WC_classification = WC_message_classified(input)
    accuracy = merged_dataset_training.accuracy_export()

    if NB_classification == 0:
        NB_classification_result = "Check via Naive-Bayes Classification \nAlgorithm → Likely not a scam"
    else:
        NB_classification_result = "Check via Naive-Bayes Classification \nAlgorithm → Likely a scam"

    if LG_classification == 0:
        LG_classification_result = "Check via Logistic Regression Classification Algorithm → Likely not a scam"
    else:
        LG_classification_result = "Check via Logistic Regression Classification Algorithm → Likely a scam"

    if WC_classification == 0:
        WC_classification_result = "Check via Word Count Algorithm → With {}% accuracy, likely not a scam".format(accuracy) 
    elif WC_classification == 1:
        WC_classification_result ="Check via Word Count Algorithm → With {}% accuracy, likely a scam".format(accuracy)
    else:
        WC_classification_result = "The Word Count Algorithm has detected mixed results"

    return NB_classification_result + "\n\n" + LG_classification_result + "\n\n" + WC_classification_result
