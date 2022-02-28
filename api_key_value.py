#! /usr/bin/env python310
#coding:utf-8

from flask import Flask, request, jsonify, make_response,abort
from flask_httpauth import HTTPTokenAuth
from IPython.core.display import display
from functools import wraps
import pandas as pd
import pymssql

app = Flask(__name__)

def login_required(Oauth):

    @wraps(Oauth)

    def wrap(*args, **kwargs):
        
        if request.headers.get('nimit')  and request.headers.get('nimit') == '123abc':

            return Oauth(*args, **kwargs)

        else:
            
            abort(401)

    return wrap
   

@app.route('/')
@app.route('/google_ads/', methods = ['GET'])
@login_required
def google_ads():

    date = request.json['date']

    connect = pymssql.connect( host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.reports')

    cursor = connect.cursor()

    cursor.execute('''
                        SELECT 
                             * 
                        FROM 
                            fgc_all_gads
                        WHERE 
                            GDATE = '%s'
                        ORDER BY 
                            GDATE
                        
    
                    '''%(date))

    df = pd.DataFrame([{name:row[i] for i, name in enumerate([col[0] for col in cursor.description])} for row in cursor.fetchall()])

    result = {}
    for index, row in df.iterrows():
        result[index] = dict(row)      
    return jsonify(result)
    

    '''
    data_dict = dict()
    for col in df.columns:
        data_dict[col] = df[col].values.tolist()
    return jsonify(data_dict)
    '''

if __name__ == '__main__':
    app.run(debug = True)

