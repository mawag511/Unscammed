''' importing libraries and reading the dataset '''
import pandas as pd
import string
import nltk
nltk.download('stopwords')
nltk.download('punkt')
stopwords = nltk.corpus.stopwords.words('english')
punctuation = string.punctuation

data = pd.read_csv('training/TotalSpamCollection.txt', sep = '\t', header=None, names=["Category", "Message"])

''' pre-processing the above dataset by slicing and tokenizing the sentences, removing stopwords and making everything in lowercase
    then, adding the output to an additional "Processed" column
'''
def pre_process(message):
    remove_punct = "".join([word.lower() for word in message if word not in punctuation])
    tokenize = nltk.tokenize.word_tokenize(remove_punct)
    remove_stopwords = [word for word in tokenize if word not in stopwords]
    return remove_stopwords

data['Processed'] = data['Message'].apply(lambda x: pre_process(x))

''' dividing all the words into typical spam words and typical ham words based on the dataset's results '''
def word_categorization():
    spam_words = []
    ham_words = []
   
    for message in data['Processed'][data['Category'] == '1']:
        for word in message:
            spam_words.append(word)
    
    for message in data['Processed'][data['Category'] == '0']:
        for word in message:
            ham_words.append(word)

    return spam_words, ham_words

spam_words, ham_words = word_categorization()

''' predicting whether a message is a spam or ham message based on the amount of ham/spam words in it '''
accuracy = 0
def predict(message):
    spam_counter = 0
    ham_counter = 0
    global accuracy
    
    for word in message:
        spam_counter += spam_words.count(word)
        ham_counter += ham_words.count(word)
    
    if ham_counter > spam_counter:
        accuracy = round((ham_counter / (ham_counter + spam_counter) * 100))
        return 0  
    elif ham_counter == spam_counter:
        return 0.5  
    else:
        accuracy = round((spam_counter / (ham_counter + spam_counter)* 100))
        return  1

''' exporting the accuracy from the above function '''
def accuracy_export():
    return accuracy
