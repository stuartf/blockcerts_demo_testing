from database_definition import Base, Person
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Open the DB and get access to it.

engine = create_engine('sqlite:///blockchain_cert_demo.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Add in the roster to the table


def add_new_user_to_table(data):

    # Add all the participants one by one
    for i in range(len(data)):
        person = Person()
        person.first_name = data[i]['first_name']
        person.last_name = data[i]['last_name']
        person.email = data[i]['email']
        person.nonce = data[i]['nonce']
        session.add(person)

    # Commit the db additions.
    session.commit()
    return "Added %d participants to the table" % len(data)


if __name__ == '__main__':
    # Read in the roster as a dictionary
    # Column names for entry should be
    # first_name
    # last_name
    # email
    # nonce(unique code)

    with open("participants.csv") as f:
        reader = csv.DictReader(f)
        data = [r for r in reader]

    print(add_new_user_to_table(data))
