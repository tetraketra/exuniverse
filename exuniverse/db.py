import sqlite3
from typing import Literal
from typing import NewType

import click
from flask import current_app, g, Flask


lastrowid = NewType('lastrowid', int)
def query_db(
    conn: sqlite3.Connection, 
    sql: str, vals: tuple = (None,), 
    method: Literal["fetch", "commit"] = "fetch"
) -> list[dict] | lastrowid | None:
    """
    Run a query and either fetch results as a list of dicts
    or commit the changes.
    """
    
    curs: sqlite3.Cursor = conn.cursor()
    if vals != (None,):
        curs.execute(sql, vals)
    else:
        curs.execute(sql)

    results = curs.fetchall() if method == "fetch" else (conn.commit(), curs.lastrowid)[1]
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
    
    db = g.pop('db', None)

    if db is not None:
        db.close()


def link_to_app(app: Flask):
    """
    Registers `db.py` functions to `app` from `__init__.py`.
    """
    
    app.teardown_appcontext(close_db) # call `close_db()` when app context (request) ends
    app.cli.add_command(init_db_command) # register `init_db_command()`'s `init-db` flask cli command

