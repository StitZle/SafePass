from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

db_url = "localhost:5432"
db_name = "safepass"
db_user = "postgres"
db_password = "Balou290499"
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_url}/{db_name}')
Session = sessionmaker(bind=engine)

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", String)
    user_name = Column("user_name", String)
    user_pass = Column("user_pass", String)
    created_at = Column("created_at", DateTime)
    updated_at = Column("updated_at", DateTime)

    def __init__(self, user_id, user_name, user_pass):
        self.user_id = user_id
        self.user_name = user_name
        self.user_pass = user_pass
        self.created_at = datetime.now()
        self.updated_at = datetime.now()