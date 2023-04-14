from flask import Flask,request,jsonify
from flask_bcrypt import Bcrypt
from db import *
from auth import *


app = Flask(__name__)
createcon()
bcrypt = Bcrypt()
loggedin = False
# @app.route('/',methods=['GET'])
# def test():
#     return "hello"

@app.route('/login', methods=['POST'])
def log():
    data = request.get_json()
    global loggedin
    loggedin = login(data['name'],data['pwd'])
    if loggedin:
        return "loggedin"
    else:
        return "not logged in"
@app.route('/admin/login', methods=['POST'])
def logad():
    data = request.get_json()
    global loggedin
    loggedin = loginad(data['name'],data['pwd'])
    if loggedin:
        return "loggedin"
    else:
        return "not logged in"
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    global loggedin
    loggedin = reg(data['name'],data['pwd'])
    if loggedin:
        return "registered"
    else:
        return "not registered"
@app.route('/admin/register', methods=['POST'])
def registerad():
    data = request.get_json()
    global loggedin
    loggedin = regad(data['name'],data['pwd'])
    if loggedin:
        return "registered"
    else:
        return "not registered"
@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    if loggedin:
        if creator(data['title'],data['desc'],data['Id'],data['cat']):
            return "added"
        return "not added"
    else:
        return "log in first"
@app.route('/admin/create', methods=['POST'])
def createcat():
    data = request.get_json()
    if loggedin:
        if creatorad(data['cat'],data['desc']):
            return "added"
        return "not added"
    else:
        return "log in first"
@app.route('/edit', methods=['POST'])
def edit():
    data = request.get_json()
    if loggedin:
        if editor(data['Id'],data['key'],data['value']):
            return "edited"
        return "not edited"
    else:
        return "login first"
@app.route('/admin/edit', methods=['POST'])
def editad():
    data = request.get_json()
    if loggedin:
        if editorcat(data['value'],data['key'],data['cat']):
            return "edited"
        return "not edited"
    else:
        return "error"
@app.route('/read/<title>', methods=['GET'])
def read(title):
    blog = pickle.loads(reader(title))
    return blog
@app.route('/admin/read/<cat>', methods=['GET'])
def readad(cat):
    blog = pickle.loads(readercat(cat))
    return blog
@app.route('/admin/del/<cat>', methods=['GET'])
def deletecat(cat):
    if loggedin:
        if deleteca(cat):
            return "deleted"
        return "not deleted"
    return "not logged in"
@app.route('/del/<id>', methods=['GET'])
def delete(id):
    if loggedin:
        if deleter(id):
            return "deleted"
        return "not deleted"
    return "not logged in"
if __name__ == '__main__':
	app.run(debug=True)
