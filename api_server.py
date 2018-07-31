#THIS IS A WEBSERVER FOR DEMONSTRATING THE TYPES OF RESPONSES WE SEE FROM AN API ENDPOINT
from flask import Flask
from flask import request
from flask import json,jsonify
from database_definition import Base, Person
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///blockchain_cert_demo.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)

with open('issuer.json') as json_data:
    data = json.load(json_data)


# GET REQUEST from Blockcerts app
@app.route('/', methods=['GET'])
def read_issuer_json():
    return jsonify(data)

# POST Data from Blockcerts app or PUT Data for creating a new user
@app.route('/', methods=['POST','PUT'])
def create_update_user():
    if request.method == 'POST':
        request_data_dict = json.loads(request.data)
        return update_user_address(request_data_dict)

    elif request.method == 'PUT':
        return add_new_user_to_table(request.args)
    

def update_user_address(user_data):
    person = session.query(Person).filter_by(nonce=int(user_data['nonce'])).one()
    person.public_address = user_data['bitcoinAddress']
    session.add(person)
    session.commit()
    return "Updated user address to %s" % person.public_address


def add_new_user_to_table(data):
    person = Person()
    person.first_name = data['first_name']
    person.last_name = data['last_name']
    person.email = data['email']
    person.nonce = data['nonce']
    session.add(person)
    session.commit()
    return "Added a new person to the table with email %s" % person.email


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port="80")
