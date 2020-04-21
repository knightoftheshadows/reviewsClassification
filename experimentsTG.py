import pandas as pd
from math import floor
from random import shuffle
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.model_selection import train_test_split
from sklearn import datasets
from sklearn import svm

#load dataset and return dataframes
def load_data():
    df = pd.read_csv('reviews.csv', '¨')
    df = df.drop(['other', 'Star rating', 'Product'], 'columns')
    df['Functional'].replace('x', '_Label_Func', inplace=True)
    df['Performance'].replace('x', '_Label_Perf', inplace=True)
    df['Compatibility'].replace('x', '_Label_Comp', inplace=True)
    df['Usability'].replace('x', '_Label_Usab', inplace=True)
    df.fillna('_Label_Zero', inplace=True)

    functional_df = df.drop(['Compatibility', 'Performance', 'Usability'], 'columns')
    performance_df = df.drop(['Compatibility', 'Functional', 'Usability'], 'columns')
    compatibility_df = df.drop(['Functional', 'Performance', 'Usability'], 'columns')
    usability_df = df.drop(['Compatibility', 'Performance', 'Functional'], 'columns')

    functional_df.rename(columns={'Functional': 'Label',
                    'Performance': 'Label',
                    'Compatibility': 'Label',
                    'Usability': 'Label'},
           inplace=True)
    compatibility_df.rename(columns={'Functional': 'Label',
                    'Performance': 'Label',
                    'Compatibility': 'Label',
                    'Usability': 'Label'},
           inplace=True)
    usability_df.rename(columns={'Functional': 'Label',
                    'Performance': 'Label',
                    'Compatibility': 'Label',
                    'Usability': 'Label'},
           inplace=True)
    performance_df.rename(columns={'Functional': 'Label',
                    'Performance': 'Label',
                    'Compatibility': 'Label',
                    'Usability': 'Label'},
           inplace=True)

    dfs = []
    dfs.append(functional_df)
    dfs.append(performance_df)
    dfs.append(compatibility_df)
    dfs.append(usability_df)
    return dfs

def getIndexes(label_relevants, label_0s):
    shuffle(label_0s)
    shuffle(label_relevants)
    list_of_training_indexes_lists = []
    list_of_testing_indexes_lists = []
    for i in range(10):
        # number of irrelevant features to retrieve from label_0 is 9/10*fold_size because of 10 fold cross validation
        fold_size = floor(len(label_relevants) / 10)
        label_0s_downsample_train = label_0s[:i * fold_size]
        label_0s_downsample_train.extend(label_0s[(i + 1) * fold_size:10 * fold_size])
        label_relevants_train = label_relevants[:i * fold_size]
        label_relevants_train.extend(label_relevants[(i + 1) * fold_size:10 * fold_size])
        training_indexes = label_0s_downsample_train
        training_indexes.extend(label_relevants_train)
        shuffle(training_indexes)
        list_of_training_indexes_lists.append(training_indexes)

        shuffle(label_0s)
        label_0s_test = label_0s[:floor(fold_size / original_ratio)]
        label_relevants_test = label_relevants[i * fold_size:(i + 1) * fold_size]
        testing_indexes = label_relevants_test
        testing_indexes.extend(label_0s_test)
        shuffle(testing_indexes)
        list_of_testing_indexes_lists.append(testing_indexes)

    return list_of_training_indexes_lists, list_of_testing_indexes_lists

dfs = load_data()
for df in dfs:
    label_0s = df.index[df['Label'] == '_Label_Zero'].tolist() #contains indexes which column label matches label_zero
    label_relevants = df.index[df['Label'] != '_Label_Zero'].tolist()
    original_ratio = len(label_relevants)/len(label_0s)
    trainll, testll = getIndexes(label_relevants, label_0s) #contains indexes for testing and training

    corpus = df['Text']
    #Bag of Words
    vectorizer = CountVectorizer()
    bow = vectorizer.fit_transform(corpus)
    bow = bow.toarray()
    bow_names = vectorizer.get_feature_names()

    #Term Frequency - Inverse Document Frequency
    transformer = TfidfTransformer(smooth_idf=False)
    tfidf = transformer.fit_transform(bow)
    tfidf.toarray()
