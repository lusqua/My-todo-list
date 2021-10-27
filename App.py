from flask_restful import Resource, Api, reqparse
from datetime import datetime
from flask import Flask
import json


app = Flask(__name__)
api = Api(app)


with open('data.json', 'r', encoding='UTF-8') as json_file:
    todos = json.load(json_file)


class Todo(Resource):
    def get(self):
        with open('data.json', 'r', encoding='UTF-8') as json_file:
            todos = json.load(json_file)
        return todos

    def post(self):
        try:
            parser = reqparse.RequestParser()

            parser.add_argument('Title', required=True,
                                help="Obrigatório definir um título")
            parser.add_argument('Description', required=True,
                                help="Obrigatorio definir uma descricao")
            parser.add_argument('Data')
            args = parser.parse_args()

            if args['Title'] in todos:
                return {'Title': args['Title'], 'Status': 'Já adicionado. Utilize PUT para editar.'}

            todos[args['Title']] = {
                'Description': args['Description'],
                'Data': args['Data']
            }

            with open('data.json', 'w') as json_file:
                json.dump(todos, json_file)

            return {'Title': args['Title'], 'Description': args['Description'], 'Data': f'''{args['Data']}''', 'Status': 'Adicionado!'}
        except:
            return {'Status': 'A operação falhou!'}

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Title', required=True,
                            help="Obrigatório definir um título")
        args = parser.parse_args()
        del todos[args['Title']]
        with open('data.json', 'w') as json_file:
            json.dump(todos, json_file)
        return {'Removido': f"{args['Title']}", 'Status': 'Deletado!'}

    def put(self):
        try:
            parser = reqparse.RequestParser()

            parser.add_argument('Title', required=True,
                                help="Obrigatório definir um título")
            parser.add_argument('Description', required=True,
                                help="Obrigatorio definir uma descricao")
            parser.add_argument('Data')
            args = parser.parse_args()

            if not args['Title'] in todos:
                return {"Title": args["Title"], "Status": "To-do inexistente."}

            todos[args['Title']] = {
                'Description': args['Description'],
                'Data': args['Data']
            }

            with open('data.json', 'w') as json_file:
                json.dump(todos, json_file)

            return {'Title': args['Title'], 'Description': args['Description'], 'Data': f'''{args['Data']}''', 'Status': 'Editado!'}
        except:
            return {"Status": 'A Operação falhou!'}


api.add_resource(Todo, '/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
