from db import *
from flask import request
def login(name,pwd)->bool:
    res = find_user(name,pwd)
    if res:
        return True
    return False
def loginad(name,pwd)->bool:
    res = find_userad(name,pwd)
    if res:
        return True
    return False
def reg(name,pwd):
    res = insert_user(name,pwd)
    if res:
        return True
    return False
def regad(name,pwd):
    res = insert_userad(name,pwd)
    if res:
        return True
    return False