import itertools as it
import more_itertools as mit
import random as r
import string

from sqlalchemy.orm import joinedload
from pprint import pprint, pformat
from datetime import datetime, timedelta
import datetime as dt

from exuniverse.app import flask_app
from exuniverse.db import flask_db, User, Card, TemplateType, TemplateSubtype
from exuniverse.extras import DBConverter 


DO_TESTING_CARDS = True

with flask_app.app_context() as app_context:
    flask_db.drop_all()
    flask_db.create_all()

    ttypes = [
        "monster", 
        "spell", 
        "trap"
    ]

    [flask_db.session.add(TemplateType(ttype=ttype)) for ttype in ttypes]
    flask_db.session.commit()

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
    
    [flask_db.session.add(TemplateSubtype(ttype_id=ttype_id, tsubtype=tsubtype)) for ttype_id, tsubtype in tsubtypes]
    flask_db.session.commit()


if DO_TESTING_CARDS:

    with flask_app.app_context() as app_context:

        for card_num in range(10000):

            a = r.choice(flask_db.session.query(TemplateSubtype).join(TemplateType).options(joinedload(TemplateSubtype.templatetype)).all())
            start_date = datetime(2000, 1, 1)
            end_date = datetime(2020, 1, 1)

            new_card = Card(
                name=f"Testing Card {card_num}",
                treated_as=r.choice([f"Testing Card {card_num}", ""]),
                effect=''.join(r.choice(string.ascii_letters + string.digits) for _ in range(5)),
                ttype_id=a.ttype_id,
                tsubtype_id=a.id,
                attributes=''.join(str(r.choice([0, 1])) for _ in range(6)),
                mon_atk=r.randint(0, 1000),
                mon_def=r.randint(0, 1000),
                mon_level=r.randint(0, 10),
                mon_abilities=''.join(str(r.choice([0, 1])) for _ in range(6)),
                mon_types=''.join(str(r.choice([0, 1])) for _ in range(24)),
                pen_scale=r.randint(0, 10),
                pen_effect=''.join(r.choice(string.ascii_letters + string.digits) for _ in range(5)),
                link_arrows=''.join(str(r.choice([0, 1])) for _ in range(8)),
                ocg=r.choice([0, 1]),
                ocg_date=start_date + timedelta(days=r.randint(0, (end_date - start_date).days)),
                ocg_limit=r.randint(0, 3),
                tcg=r.choice([0, 1]),
                tcg_date=start_date + timedelta(days=r.randint(0, (end_date - start_date).days)),
                tcg_limit=r.randint(0, 3),
                exu_limit=r.randint(0, 3),
                date_deleted=datetime.now(dt.UTC)
            )

            flask_db.session.add(new_card)

        flask_db.session.commit()