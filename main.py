from flask import Flask
from flask_restful import Api, Resource, reqparse
import pandas as pd

app = Flask(__name__)
api = Api(app)

class Takimlar(Resource):
    def get(self):
        data = pd.read_csv('takimlar.csv')
        data = data.to_dict('records')
        return {'veri': data}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('takim', required=True , location= 'args')
        parser.add_argument('yil', required=True, location= 'args')
        parser.add_argument('ulke', required=True, location= 'args')
        parser.add_argument('sehir', required=True, location= 'args')
        args = parser.parse_args()

        data = pd.read_csv('takimlar.csv')

        new_data = pd.DataFrame({
            'takim': [args['takim']],
            'yil': [args['yil']],
            'ulke': [args['ulke']],
            'sehir': [args['sehir']]
        })

        data = data.append(new_data, ignore_index = True)
        data.to_csv('takimlar.csv', index=False)
        return {'veri' : new_data.to_dict('records')}, 201

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('takim', required=True, location= 'args')
        args = parser.parse_args()

        data = pd.read_csv('takimlar.csv')

        data = data[data['takim'] != args['takim']]

        data.to_csv('takimlar.csv', index=False)
        return {'mesaj': 'Kayıt başarılı bir şekilde silindi.'}, 200


class Sehirler(Resource):
    def get(self):
        data = pd.read_csv('takimlar.csv', usecols=[3])
        data = data.to_dict('records')
        return {'veri': data}, 200


class Takim(Resource):
    def get(self, takim):
        data = pd.read_csv('takimlar.csv')
        data = data.to_dict('records')
        for entry in data:
            if entry['takim'] == takim:
                return {'data': entry}, 200
        return {'mesaj': 'Bu isimli kayıt bulunamadı !'}, 200


api.add_resource(Takimlar, '/takimlar')
api.add_resource(Sehirler, '/sehirler')
api.add_resource(Takim, '/<string:takim>')

if __name__ == '__main__':
    app.run()