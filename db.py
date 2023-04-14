import pymongo
from datetime import datetime
import pickle
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
Database = None
loggername = None
def createcon():
    # Replace you
    connection_url = 'mongodb+srv://root:toor@cluster0.et3fbel.mongodb.net/?retryWrites=true&w=majority'
    
    client = pymongo.MongoClient(connection_url)

    # Database
    global Database 
    Database = client.get_database('blog')
def find_user(name,pwd)->bool:
    user = Database.user
    users = user.find()
    for item in users:
        if name == item['name'] and  bcrypt.check_password_hash(item['pwd'], pwd):
            global loggername 
            loggername = name
            return True
    return False
def find_userad(name,pwd)->bool:
    user = Database.admin
    users = user.find()
    for item in users:
        if name == item['name'] and  bcrypt.check_password_hash(item['pwd'], pwd):
            global loggername 
            loggername = name
            return True
    return False
def insert_user(name,pwd)->bool:
    user = Database.user
    pwd = bcrypt.generate_password_hash(pwd).decode('utf-8')
    users = user.find()
    for item in users:
        if name == item['name']:
            return False
    obj = {
        'name' : name,
        'pwd' : pwd
    }
    final = user.insert_one(obj)
    if final:
        global loggername 
        loggername = name
        return True
    else:
        return False
def insert_userad(name,pwd)->bool:
    user = Database.admin
    pwd = bcrypt.generate_password_hash(pwd).decode('utf-8')
    users = user.find()
    for item in users:
        if name == item['name']:
            return False
    obj = {
        'name' : name,
        'pwd' : pwd
    }
    final = user.insert_one(obj)
    if final:
        global loggername 
        loggername = name
        return True
    else:
        return False
def creatorad(cat,desc):
    can = False
    cate = Database.cat
    ad = Database.admin
    queryad = ad.find()
    query = cate.find()
    for i in queryad:
        if i['name'] == loggername:
            can = True
            break
    if can:
        for i in query:
            if i['cat'] == cat:
                return False
        obj = {
            'cat' : cat,
            'desc' : desc
        }
        submit = cate.insert_one(obj)
        return submit
    return False
def creator(title,desc,Id,cat):
    blogs = Database.blogs
    cate = Database.cat
    querycat = cate.find()
    query = blogs.find()
    for i in query:
        if i['id'] == Id:
            return False
    for i in querycat:
        if i['cat'] == cat:
            obj = {
                'id' : Id,
                'title' : title,
                'author' : loggername,
                'desc' : desc,
                'dt' : datetime.now(),
                'cat' : cat
            }
            submit = blogs.insert_one(obj)
            return submit
    return False
def editorcat(value,key,cat):
    can = False
    ad = Database.admin
    queryad = ad.find()
    cate = Database.cat
    query = cate.find()
    for i in queryad:
        if i['name'] == loggername:
            can = True
            break
    if can:
        for i in query:
            if i['cat'] == cat:
                prev = {key:i[key]}
                new = {"$set":{key:value}}
                final = cate.update_one(prev,new)
                if final.acknowledged:
                    return True
                else:
                    return False
    return False
def editor(id,key,value):
    global loggername
    if loggername != None:
        blogs = Database.blogs
        query = blogs.find()
        print(key)
        for i in query:
            if i['id'] == id and i['author'] == loggername:
                prev = {key:i[key]}
                new = {"$set":{key:value}}
                final = blogs.update_one(prev,new)
                if final.acknowledged:
                    return True
                else:
                    return False
    return False
def readercat(cat):
    cate = Database.cat
    query = cate.find()
    for i in query:
        if i['cat'] == cat:
            i.pop('_id')
            return pickle.dumps(i)
    return None
def reader(title):
    blogs = Database.blogs
    query = blogs.find()
    #x = 0
    for i in query:
        if i['title'] == title:
            i.pop('_id')
            i.pop('id')
            return pickle.dumps(i)
        #x += 1
    return None
def deleteca(cat):
    can = False
    cate = Database.cat
    ad = Database.admin
    queryad = ad.find()
    query = cate.find()
    for i in queryad:
        print(i['name'])
        if loggername == i['name']:
            can == True
            print(loggername)
            break
    print(loggername)
    if can:
        for i in query:
            if i['cat'] == cat:
                cate.delete_one(i)
                return True
    return False
def deleter(id):
    global loggername
    blogs = Database.blogs
    query = blogs.find()
    for i in query:
        if i['id'] == id and loggername == i['author']:
            blogs.delete_one(i)
            return True
    return False
            