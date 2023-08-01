


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import os
import matplotlib.pyplot as plt
import re
import string
import time
pd.set_option('display.max_rows', 50)

import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords
stop = stopwords.words('english')

from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_validate

from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neural_network import MLPClassifier

import pickle
import joblib


# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123456",
  database="email"
)



def preprocess(x):
    # lowercasing all the words
    x = x.lower()
    
    # remove extra new lines
    x = re.sub(r'\n+', ' ', x)
    
    # removing (replacing with empty spaces actually) all the punctuations
    x = re.sub("["+string.punctuation+"]", " ", x)
    
    # remove extra white spaces
    x = re.sub(r'\s+', ' ', x)
    
    return x


# creating a Flask app
app = Flask(__name__)
  
# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.
@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
  
        data = "hello world"
        return jsonify({'data': data})
  
  
# A simple function to calculate the square of a number
# the number to be squared is sent in the URL when we use GET
# on the terminal type: curl http://127.0.0.1:5000 / home / 10
# this returns 100 (square of 10)
@app.route('/home/<int:num>', methods = ['GET'])
def disp(num):
    X_test_word = """ Phillip,
        Below is the issues & to do list as we go forward with documenting the 
        requirements for consolidated physical/financial positions and transport 
        trade capture. What we need to focus on is the first bullet in Allan's list; 
        the need for a single set of requirements. Although the meeting with Keith, 
        on Wednesday,  was informative the solution of creating a infinitely dynamic 
        consolidated position screen, will be extremely difficult and time 
        consuming.  Throughout the meeting on Wednesday, Keith alluded to the 
        inability to get consensus amongst the traders on the presentation of the 
        consolidated position, so the solution was to make it so that a trader can 
        arrange the position screen to their liking (much like Excel). What needs to 
        happen on Monday from 3 - 5 is a effort to design a desired layout for the 
        consolidated position screen, this is critical. This does not exclude 
        building a capability to create a more flexible position presentation for the 
        future, but in order to create a plan that can be measured we need firm 
        requirements. Also, to reiterate that the goals of this project is a project 
        plan on consolidate physical/financial positions and transport trade capture. 
        The other issues that have been raised will be capture as projects on to 
        themselves, and will need to be prioritised as efforts outside of this 
        project.

        I have been involved in most of the meetings and the discussions have been 
        good. I believe there has been good communication between the teams, but now 
        we need to have focus on the objectives we set out to solve."""


    # Load vectorizer từ file
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer_xtest = pickle.load(f)
    

    loaded_model = joblib.load('linear_svc_model.pkl')



    start = time.time()
    X_test=preprocess(X_test_word)
    # vectorizer_xtest = CountVectorizer(min_df=5, max_features=5000)
    # X_test = vectorizer.fit_transform([X_test])
    X_test = pd.Series([X_test])

    # Encode the Document
    # X_test = vectorizer.transform(X_test)
    X_test = vectorizer_xtest.transform(X_test)


    X_test = X_test.toarray()
    print(X_test)
    print("X.shape: ",X_test.shape)
    end = time.time()
    print("Execution time (sec): ",(end - start))


    # Sử dụng mô hình để dự đoán
    predictions = loaded_model.predict([X_test[0]]   )

    d= {2: 'california', 1: 'calendar', 5: 'logistics', 8: 'tufco', 6: 'management', 4: 'esvl', 9: 'tw-commercial group', 3: 'deal discrepancies', 0: 'bill williams iii', 7: 'schedule crawler'}
    res = d[predictions[0]]
    print(res)

    return jsonify({'data': res})

@app.route('/home/add_csv', methods = ['GET', 'POST'])
def add_csv():
    if(request.method == 'GET'):
        data = pd.read_csv("preprocessed.csv")
        # label = pd.read_csv("label.csv")
        mycursor = mydb.cursor()
        # for i in range(len(label)):
        #     sqlLabel = "INSERT INTO label VALUES ({},'{}')".format(i+1, label.iloc[i][1])
        #     print(sqlLabel)
        #     mycursor.execute(sqlLabel)

        for i in range(len(data)):
            sqlSearchLabelId = "select label.id from label where label.name = ('{}')".format(data.iloc[i][0])
            mycursor.execute(sqlSearchLabelId)
            resultSearch = mycursor.fetchall()
            print("hello cak",resultSearch[0][0])
            sql = "INSERT INTO sample VALUES ({},'{}', {} , {} )".format(i+1, data.iloc[i][1], resultSearch[0][0] ,int(1))
            print("hello have a good time",sql)
            
            mycursor.execute(sql)

        mydb.commit()
        return jsonify({'res': " oke "})


@app.route('/home/display', methods = ['GET', 'POST'])
def display():
    if(request.method == 'GET'):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM dât")
        myresult = mycursor.fetchall()
        res=[]
        for i in myresult:
            res.append(i )

        return jsonify({'res': res })

@app.route('/home/displayLabel', methods = ['GET', 'POST'])
def displayLabel():
    if(request.method == 'GET'):

        # label = pd.read_csv("label.csv")
        mycursor = mydb.cursor()
        # for i in range(len(label)):
        #     sqlLabel = "INSERT INTO label VALUES ({},'{}')".format(i+1, label.iloc[i][0])
        #     print(sqlLabel)
        #     mycursor.execute(sqlLabel)
        # mydb.commit()

        mycursor.execute("SELECT label.id FROM label where label.name = 'california' ")
        myresult = mycursor.fetchall()
        res = myresult[0]
        # res=[]
        # for i in myresult:
        #     res.append(i )

        return jsonify({'res': res })
# driver function
if __name__ == '__main__':
  
    app.run(debug = True)