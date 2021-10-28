from flask_restful import Resource, Api, reqparse
from datetime import datetime
from flask_cors import CORS
from flask import Flask
import json


app = Flask(__name__)
api = Api(app)
CORS(app)


with open('data.json', 'r', encoding='UTF-8') as json_file:
    try:
        todos = json.load(json_file)
    except:
        todos = {}


class Todo(Resource):
    def get(self):
        with open('data.json', 'r', encoding='UTF-8') as json_file:
            try:
                self.todos = json.load(json_file)
            except:
                self.todos = {}
        return self.todos

    def post(self):
        try:
            with open('data.json', 'r', encoding='UTF-8') as json_file:
                try:
                    self.todos = json.load(json_file)
                except:
                    self.todos = {}
            parser = reqparse.RequestParser()
            parser.add_argument('Title', required=True,
                                help="Obrigatório definir um título")
            parser.add_argument('Description', required=True,
                                help="Obrigatorio definir uma descricao")
            parser.add_argument('Data')
            args = parser.parse_args()

            id = len(self.todos)

            if id in self.todos:
                id += 1

            self.todos[id] = {
                'Title': args['Title'],
                'Description': args['Description'],
                'Data': args['Data']
            }

            test = []
            todo = {}
            for item in self.todos:
                test.append(self.todos[item])
            for i in test:
                todo[test.index(i)+1] = i

            self.todos = todo

            with open('data.json', 'w', encoding='UTF-8') as json_file:
                json.dump(self.todos, json_file)

            return {'Title': args['Title'], 'Description': args['Description'], 'Data': f'''{args['Data']}''', 'Status': 'Adicionado!'}
        except:
            pass

    def delete(self):
        with open('data.json', 'r', encoding='UTF-8') as json_file:
            try:
                self.todos = json.load(json_file)
            except:
                self.todos = {}
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True,
                            help="Obrigatório definir um título")
        args = parser.parse_args()

        del self.todos[args['id']]

        print(self.todos)

        test = []
        todo = {}
        for item in self.todos:
            test.append(self.todos[item])
        for i in test:
            todo[test.index(i)+1] = i

        print(todo)
        self.todos = todo
        with open('data.json', 'w') as json_file:
            json.dump(self.todos, json_file)
        return {'Removido': f"{args['id']}", 'Status': 'Deletado!'}

    def put(self):
        with open('data.json', 'r', encoding='UTF-8') as json_file:
            try:
                self.todos = json.load(json_file)
            except:
                self.todos = {}
        try:
            parser = reqparse.RequestParser()

            parser.add_argument('id', required=True,
                                help="O id é obrigatório")
            parser.add_argument('Title')
            parser.add_argument('Description')
            parser.add_argument('Data')
            args = parser.parse_args()

            if not args['id'] in self.todos:
                return {"id": args['id'], "Title": args["Title"], "Status": "To-do inexistente."}

            self.todos[args['id']] = {
                'Title': args['Title'],
                'Description': args['Description'],
                'Data': args['Data']
            }

            with open('data.json', 'w') as json_file:
                json.dump(self.todos, json_file)

            return {'Title': args['Title'], 'Description': args['Description'], 'Data': f'''{args['Data']}''', 'Status': 'Editado!'}
        except:
            return {"Status": 'A Operação falhou!'}


api.add_resource(Todo, '/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
