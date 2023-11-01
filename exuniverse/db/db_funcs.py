import sqlite3
from typing import Literal, NewType

import click
from flask import current_app, g, Flask


last_inserted_rowid = NewType('last_inserted_rowid', int)
rows_affected = NewType('rows_affected', int)
def query_db(
    conn: sqlite3.Connection, 
    sql: str, 
    vals: tuple = (None,), 
    method: Literal["select", "insert", "update"] = "select"
) -> list[dict] | last_inserted_rowid | rows_affected:
    """
    Run a query and either fetch results as a list of dicts
    or commit the changes. `vals` automatically quotes.
    """
    
    curs: sqlite3.Cursor = conn.cursor()
    if vals != (None,):
        curs.execute(sql, vals)
    else:
        curs.execute(sql)

    match (method):
        case "insert":
            conn.commit()
            results = curs.lastrowid
            curs.close()
        case "update":
            conn.commit()
            results = curs.rowcount
            curs.close()
        case _: # select is default
            results = [{**row} for row in curs.fetchall()]
            curs.close()

    return results

def get_db() -> sqlite3.Connection:
    """
    Load the database connection into the global 
    namespace `g` and return as `g.db`. 
    """
    
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def init_db() -> None:
    """
    [Re]init database using `schema.sql`.
    """

    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """
    Init flask command-line command `init-db` for `init_db()`.
    """
    
    init_db()
    click.echo('[Re]initialized the database.')


def close_db(e=None): # not sure if `e` is required, but it's there in the docs ^^;
    """
    Close the database connection at the end of a request.
    """
    
    db: sqlite3.Connection = g.pop('db', None)

    if db is not None:
        db.close()


def link_db_to_app(app: Flask):
    """
    Registers `db.py` functions to `app` from `__init__.py`.
    """
    
    app.teardown_appcontext(close_db) # call `close_db()` when app context (request) ends
    app.cli.add_command(init_db_command) # register `init_db_command()`'s `init-db` flask cli command