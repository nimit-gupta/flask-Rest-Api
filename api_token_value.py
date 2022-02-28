#! /usr/bin/env python310
#coding:utf-8

from flask import Flask, request, jsonify, make_response
from flask_httpauth import HTTPTokenAuth
from IPython.core.display import display
import pandas as pd
import pymssql

app = Flask(__name__)

auth = HTTPTokenAuth(scheme='Bearer')

verify_token = ['1q2w3e4r5t6y7u8i9o0p', '1q2w3e4r5t6y7u8i9oWE', '1q2w3e4r5t6y7u8i9oXX']

@auth.verify_token
def verify_tokens(token):
    if token in verify_token:
        return True
    else:
        return None

@app.route('/')
@app.route('/google_ads')
@auth.login_required
def google_ads():
    connect = pymssql.connect( host = r'217.174.248.77',
                               port = 3689,
                               user = r'DevUser3',
                               password = r'flgT!9585',
                               database = r'feelgood.reports')


    cursor = connect.cursor()

    cursor.execute('''
                        SELECT 
                             * 
                        FROM 
                            fgc_all_gads
                        ORDER BY 
                            GDATE
                        
    
                    ''')

    df = pd.DataFrame([{name:row[i] for i, name in enumerate([col[0] for col in cursor.description])} for row in cursor.fetchall()])
    '''
    result = {}
    for index, row in df.iterrows():
        result[index] = dict(row)      
    return jsonify(result)
    '''

    data_dict = dict()
    for col in df.columns:
        data_dict[col] = df[col].values.tolist()
    return jsonify(data_dict)

if __name__ == '__main__':
    app.run(debug = True)

