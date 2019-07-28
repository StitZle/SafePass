from src.entitys.entity import Session, engine, Base
from src.entitys.entity import Entity

#https://auth0.com/blog/using-python-flask-and-angular-to-build-modern-apps-part-1/


# Todo Add Logback 
Base.metadata.create_all(engine)

session = Session()

keys = session.query(Entity).all()
safe_pass = Entity(user_id ="01", name="Test", login="StitZle", password="1234", e_mail="niclas.buerger@web.de", website="niclasbuerger.de", note= "")
session.add(safe_pass)
session.commit()
session.close()

