import uuid
from flask import Flask
from flask import request
from flask import jsonify
from flask import abort
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from flask import make_response

app = Flask(__name__)
#DB_NAME = "pro"


class DBOperation:

    def __init__(self):
        try:
            self.dbclient = MongoClient('localhost', 27017)
            self.db = self.dbclient.pro
        except ServerSelectionTimeoutError as e:
            raise ("ERROR in connect with database: {}".format(e.message))

    def add_user(self, user):
        collection = self.db.users
        collection.insert(user)
        return "User {} created with id {}".format(user.get('username'), user.get('id'))

    def delete_user(self, user):
        collection = self.db.users
        collection.delete_one({'username': user})
        return "User {} deleted successfully".format(user)

    def update_user(self, user):
        collection = self.db.users
        user_id = collection.find({"id": user.get("id")})
        if not user_id:
            abort(404)
        else:
            for i in user_id:
                collection.update({'_id': i.get("_id")}, {"$set": user}, upsert=True)
                return "UPDATED"
            return "Should some issue"

    def get_users(self, user_id=None):
        collection = self.db.users
        if user_id is None:
            user_list = []
            for i in collection.find():
                user_data = dict()
                user_data['email'] = i.get('email')
                user_data['username'] = i.get('username')
                user_data['id'] = i.get('id')
                user_data['name'] = i.get('name')
                user_data['password'] = i.get('password')
                user_list.append(user_data)
            return jsonify({"user_list": user_list})
        else:
            user_data = {}
            for i in collection.find():
                if i.get('id') == user_id:
                    user_data['email'] = i.get('email')
                    user_data['username'] = i.get('username')
                    user_data['id'] = i.get('id')
                    user_data['name'] = i.get('name')
                    user_data['password'] = i.get('password')
                    return jsonify(user_data)
            return make_response(jsonify({'error': 'Resource not found!'}), 404)


operation = DBOperation()

@app.route("/api/v1/info")
def home_index():
    client = MongoClient('localhost', 27017)
    db = client.pro
    collection = db.info
    info_data = ""
    for i in collection.find():
        info_data = i.get('api_vesrion')[0]
    return jsonify({"api_version" : info_data}), 200


@app.route('/api/v1/users', methods=['GET'])
def get_users():
    return operation.get_users()


@app.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    return operation.list_users(user_id)


@app.route('/api/v1/users', methods=['POST'])
def create_user():
    print(request.json)
    if not request.json or not 'username' in request.json or not\
                    'email' in request.json or not 'password' in request.json:
        abort(400)
    user = {
        'id':  uuid.uuid4(),
        'username': request.json['username'],
        'email': request.json['email'],
        'name': request.json.get('name', ""),
        'password': request.json['password']
         }
    return jsonify({'status': operation.add_user(user)}), 201


@app.route('/api/v1/users', methods=['DELETE'])
def remove_user():
    if not request.json or not 'username' in request.json:
        abort(400)
    user = request.json['username']
    return jsonify({'status': operation.delete_user(user)}), 200


@app.route('/api/v1/users/<user_id>', methods=['PUT'])
def modify_user(user_id):
    user = {}
    if not request.json:
        abort(400)
    user['id'] = user_id
    key_list = request.json.keys()
    for i in key_list:
        user[i] = request.json[i]
    return jsonify({'status': operation.update_user(user)}), 200


@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error': 'Resource not found!'}),  404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)