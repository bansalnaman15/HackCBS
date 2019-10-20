from bson import ObjectId
from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
import json
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


app = Flask(__name__)
app.json_encoder = JSONEncoder
app.config["MONGO_URI"] = "mongodb+srv://bansalnaman:bansal@cluster0-lkibt.gcp.mongodb.net/hackcbs?retryWrites=true&w=majority"
mongo = PyMongo(app)
userCol = mongo.db.users
app.config["JWT_SECRET_KEY"]="hellohellohello"


@app.route('/', methods=["GET"])
def index():
    return render_template("Signup.html"), 200


@app.route('/signup', methods=["POST","GET"])
def signup():
    if request.method=='GET':
        return render_template("signup.html")
    elif request.method == 'POST':
        data = request.form
        if "email" in data.keys():
            print("Hai bhai")
        obj = {}
        obj["email"] = data["email"]
        obj["password"]=generate_password_hash(data["password"])
        userCol.insert_one(obj)
        return jsonify({"ok":True,"msg":"inserted"}),200

@app.route('/userdedo',methods=["GET"])
def userdedo():
    lis = list(userCol.find())
    return jsonify({"data":lis}),200



@app.route('/login', methods=["POST","GET"])
def login():
    if request.method=='GET':
        return render_template("login.html")
    elif request.method == 'POST':
        data = request.form
        if "password" in data.keys() and "email" in data.keys():
            user = userCol.find_one({"email":data["email"]})
            if user:
                if check_password_hash(user["password"],generate_password_hash(data["password"])):
                    
            else: return jsonify({"ok":False,"msg":"Data not complete"})
        else: return jsonify({"ok":False,"msg":"Data not complete"})



if __name__ == '__main__':
    app.run(port=5000)
