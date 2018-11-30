# Program : REST API Using Python Flask and SQLAlchemy Using GET, POST, PATCH and DELETE http methods
# Programmed By : Suman Gangopadhyay
# Email ID : linuxgurusuman@gmail.com
# URL : https://www.linkedin.com/in/sumangangopadhyay/
# Date : 30-Nov-2018
# Language : Python3.7
# Framework : Flask
# ORM : Flask SQLAlchemy
# Caveats : Create the Database "api_user" first into the MySQL Database. Also, Kindly use POSTMAN App
# Copyright © 2018 Suman Gangopadhyay

from flask import Flask
from flask import request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:suman@localhost/api_user'
app.config['SECRET_KEY'] = 'i_love_pizza'

db = SQLAlchemy(app)

# CREATE THE TABLE named "mysql_api_user" IN THE DATABASE
class APiUserModel(db.Model):
    __tablename__ = 'mysql_api_user'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))

#DISPLAY ALL DATA FROM DATABASE AS JSON 
@app.route('/', methods = ['GET'])
def show_all():
    data = APiUserModel.query.all()
    data_all = []
    for data in data:
        data_all.append({"id":data.id, "name":data.name, "email":data.email})
    return jsonify(data_all)

# DISPLAY ALL DATA FROM DATABASE USING THERE ID IN JSON FORMAT
@app.route('/userbyid/<int:id>', methods = ['GET'])
def show_by_id(id):
    try:
        data = APiUserModel.query.filter_by(id = id).first()
        return jsonify({"id":data.id, "name":data.name, "email":data.email})
    except:
        return jsonify({"message":"ID does not exist"})

# CREATE NEW DATA INTO DATABASE AND DISPLAY THE NEW DATA IN JSON FORMAT USING THE POSTMAN API PROGRAM
@app.route('/write', methods = ['POST'])
def write_to_db():
    name = request.get_json()["name"]
    email = request.get_json()["email"]
    api_user_model =  APiUserModel(name = name, email = email)
    save_to_database = db.session
    try:
        save_to_database.add(api_user_model)
        save_to_database.commit()
    except:
        save_to_database.rollback()
        save_to_database.flush()
    id = api_user_model.id
    data = APiUserModel.query.filter_by(id = id).first()
    return jsonify({"id":data.id, "name":data.name, "email":data.email})

# UPDATE THE EXISTING DATA INTO THE DATABASE USING THE PATCH METHOD
@app.route('/edit/<int:id>', methods = ['PATCH'])
def update_by_id(id):
    # id = request.get_json["id"]
    name = request.get_json()["name"]
    email = request.get_json()["email"]
    save_to_database = db.session
    try:
        api_user_model = APiUserModel.query.filter_by(id = id).first()
        api_user_model.name = name
        api_user_model.email = email
        save_to_database.commit()
    except:
        return jsonify({"message":"ID does not exist"})
        save_to_database.rollback()
        save_to_database.flush()
    id = api_user_model.id
    data = APiUserModel.query.filter_by(id = id).first()
    return jsonify({"id":data.id, "name":data.name, "email":data.email})

# DELETE USING DELETE METHOD
@app.route('/delete/<int:id>', methods = ['DELETE'])
def delete(id):
    try:
        save_to_database = db.session
        APiUserModel.query.filter_by(id = id).delete() 
        save_to_database.commit()
        return show_all()
    except:
        return jsonify({"message":"ID does not exist"})       

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)