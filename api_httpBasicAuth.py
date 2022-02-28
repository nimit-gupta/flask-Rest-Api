from flask import Flask, jsonify, make_response, request
from flask_restful import Resource,Api
from flask_httpauth import HTTPBasicAuth
import pandas as pd
import pymssql 


app = Flask(__name__)

api = Api(app)

auth = HTTPBasicAuth()

@auth.verify_password
def verify_credentials(username, password):
    if username == 'nimit' and  password == 'nimit':
        return True
    return False

class restful_flask_api_1(Resource):
    def __init__(self):
        pass
    @auth.login_required
    def get(self):
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
        
                      ''')

        df = pd.DataFrame([{name:row[i] for i, name in enumerate([col[0] for col in cursor.description])} for row in cursor.fetchall()])
        result = {}
        for index, row in df.iterrows():
            result[index] = dict(row)
        return jsonify(result)

class restful_flask_api_2(Resource):
    def __init__(self):
        pass
    @auth.login_required
    def get(self):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        return {'Start_date': start_date, 'End_Date': end_date}

api.add_resource(restful_flask_api_1, '/google_ads/')
api.add_resource(restful_flask_api_2,'/query_string_date/')

if __name__ == '__main__':
    app.run(debug = True)