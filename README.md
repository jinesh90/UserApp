# UserApp
  Simple App that provides RESTAPI for user operations.
  
# CRUD Operation
  This repository describes how to Implement CRUD(Create,Read,Update,Delete) Operation in REST API with useing python flask and 
 mongodb

# MongoDB
  MongoDB stores data in flexible, JSON-like documents, meaning fields can vary from document to document and data structure can be changed over time.MongoDB is free and open-source, published under the GNU Affero General Public License. To install mongodb to your system please follow this page: https://docs.mongodb.com/manual/installation/

# Flask
  Flask is a microframework for Python based on Werkzeug, Jinja 2 and good intentions. And before you ask: It's BSD licensed!!.

# UserApp
This is Standard App that required basic user operatoions, most of the web applications are required to create user accounts with username, email, password etc info. This App provides user related functionalities like 
- Add User API
- Read User/Users API
- Remove User
- Modify Users

# Implemented REST API

| RESTAPI | ENDPOINT | METHOD |
| ------ | ------ | ------ |
| Info | "/api/v1/info" | GET |
| Create User|"/api/v1/users"| POST |
| Get User| "/api/v1/users/<user_id>"|GET|
| Get all User| "/api/v1/users" | GET|
| Delete User | "/api/v1/users/<user_id>"| DELETE|
| Modify User | "/api/v1/users/<user_id>"|PUT|


