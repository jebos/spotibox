from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def reset_database():
    from box_rest_api.database.models import RFID_Uri_Mapping
    db.drop_all()
    db.create_all()

    db.session.commit()

