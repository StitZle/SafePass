from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from marshmallow import Schema, fields

db_url = "localhost:5432"
db_name = "safepass"
db_user = "postgres"
db_password = "Balou290499"
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_url}/{db_name}')
Session = sessionmaker(bind=engine)

Base = declarative_base()


class Entity(Base):
    __tablename__ = "keyhold"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer)
    safe_pass_id = Column("safe_pass_id", Integer)
    name = Column("name", String)
    login = Column("login", String)
    password = Column("password", String)
    e_mail = Column("e_mail", String)
    website = Column("website", String)
    note = Column("note", String)
    created_at = Column("created_at", DateTime)
    updated_at = Column("updated_at", DateTime)

    def __init__(self, user_id, safe_pass_id, name, login, password, e_mail, website, note):
        self.user_id = user_id
        self.safe_pass_id = safe_pass_id
        self.name = name
        self.login = login
        self.password = password
        self.e_mail = e_mail
        self.website = website
        self.note = note
        self.created_at = datetime.now()
        self.updated_at = datetime.now()



class EntitySchema(Schema):
    id = fields.Number()
    user_id = fields.Number()
    safe_pass_id = fields.Number()
    name = fields.Str()
    login = fields.Str()
    password = fields.Str()
    e_mail = fields.Str()
    website = fields.Str()
    note = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
