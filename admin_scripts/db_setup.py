import datetime as dt
import itertools as it
import random as r
import string
from datetime import datetime, timedelta
from pprint import pformat, pprint

import more_itertools as mit
from sqlalchemy.orm import joinedload
from tqdm import tqdm

from exuniverse.app import flask_app
from exuniverse.db import *
from exuniverse.extras import DBConverter
from exuniverse.reference import *

DO_TESTING_CARDS = True

with flask_app.app_context() as app_context:
    flask_db.drop_all()
    flask_db.create_all()

    [flask_db.session.add(TemplateType(t_type=t_type)) for t_type in tqdm(TTYPES, desc="Adding template types...", total=len(TTYPES))]
    flask_db.session.commit()

    [flask_db.session.add(TemplateSubtype(t_type_id=t_type_id, t_subtype=t_subtype)) for t_type_id, t_subtype in tqdm(TSUBTYPES, desc="Adding template subtypes...", total=len(TSUBTYPES))]
    flask_db.session.commit()

    [flask_db.session.add(Format(name=name)) for name in tqdm(FORMATS, desc="Adding formats...", total=len(FORMATS))]
    flask_db.session.commit()



if DO_TESTING_CARDS:

    with flask_app.app_context() as app_context:

        test_cards_cnt = 10000
        for card_num in tqdm(range(test_cards_cnt), desc="Adding testing cards...", total=test_cards_cnt):

            a = r.choice(flask_db.session.query(TemplateSubtype).all())
            start_date = datetime(2000, 1, 1)
            end_date = datetime(2020, 1, 1)

            new_card = Card(
                name=''.join(r.choice(string.ascii_letters + string.digits) for _ in range(10)) + "."*r.choice([0,1]) + ''.join(r.choice(string.ascii_letters + string.digits) for _ in range(10)),
                treated_as=r.choice([f"Testing Card {card_num+20}", None]),
                effect=''.join(r.choice(string.ascii_letters + string.digits) for _ in range(10)) + "."*r.choice([0,1]) + ''.join(r.choice(string.ascii_letters + string.digits) for _ in range(10)),
                t_type_id=a.t_type_id,
                t_subtype_id=a.id,
                attributes=''.join(mit.padded([str(r.choice([0, 1])) for _ in range(10)], '0', MAX_AT_AB_MT_LENGTH)),
                mon_atk=r.randint(0, 1000),
                mon_def=r.randint(0, 1000),
                mon_level=r.randint(0, 10),
                mon_abilities=''.join(mit.padded([str(r.choice([0, 1])) for _ in range(10)], '0', MAX_AT_AB_MT_LENGTH)),
                mon_types=''.join(mit.padded([str(r.choice([0, 1])) for _ in range(10)], '0', MAX_AT_AB_MT_LENGTH)),
                pen_scale_l=r.randint(0, 10),
                pen_scale_r=r.randint(0, 10),
                pen_effect=''.join(r.choice(string.ascii_letters + string.digits) for _ in range(10)) + "."*r.choice([0,1]) + ''.join(r.choice(string.ascii_letters + string.digits) for _ in range(10)),
                link_arrows=''.join(str(r.choice([0, 1])) for _ in range(8)),
                pen=r.choice([0, 1]),
                rarity=r.randint(1, 5),
            )

            flask_db.session.add(new_card)

        flask_db.session.commit()

        print("Testing version history...")
        a = flask_db.session.get(Card, 1)
        a.name = "OH HEY I CHANGED THIS 0"
        flask_db.session.commit()

        a = flask_db.session.get(Card, 1)
        a.name = "OH HEY I CHANGED THIS AGAIN 0"
        flask_db.session.commit()

        a = flask_db.session.get(Card, 1)
        for chist in list(a.version_history):
            print(pformat(chist.as_dict(True)))