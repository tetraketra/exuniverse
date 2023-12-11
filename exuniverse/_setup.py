from app import app
from db import db, User, Card, TemplateType, TemplateSubtype

with app.app_context() as app_context:
    db.drop_all()
    db.create_all()

    ttypes = [
        "monster", 
        "spell", 
        "trap"
    ]

    [db.session.add(TemplateType(ttype=ttype)) for ttype in ttypes]
    db.session.commit()

    tsubtypes = [
        (1, 'normal'), 
        (1, 'effect'),
        (1, 'ritual'),
        (1, 'fusion'),
        (1, 'synchro'),
        (1, 'xyz'),
        (1, 'pendulum'),
        (1, 'link'),
        (1, 'token'),
        (2, 'normal'),
        (2, 'continuous'),
        (2, 'field'),
        (2, 'equip'),
        (2, 'quick-spell'),
        (2, 'ritual'),
        (3, 'normal'),
        (3, 'continuous'),
        (3, 'counter')
    ]
    
    [db.session.add(TemplateSubtype(ttype_id=ttype_id, tsubtype=tsubtype)) for ttype_id, tsubtype in tsubtypes]
    db.session.commit()

    