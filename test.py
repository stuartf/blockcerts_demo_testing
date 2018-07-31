from database_definition import Base, Person
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Open the DB and get access to it.

engine = create_engine('sqlite:///blockchain_cert_demo.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


persons = session.query(Person).all()
print [person.serialize for person in persons]

person = session.query(Person).filter_by(nonce=123).one()
person.public_address = '0x23fgb34advcfr56'
session.add(person)
session.commit()

persons = session.query(Person).all()
print [person.serialize for person in persons]
