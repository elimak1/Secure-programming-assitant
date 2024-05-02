import sqlite3

import click
from flask import current_app, g, Flask


def get_db() -> sqlite3.Connection:
    """
    Get a database connection. If one does not exist, create a new one.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None) -> None:
    """
    Close the database connection if it exists.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db() -> None:
    """
    Initialize the database by creating the schema.
    """
    db = get_db()

    with current_app.open_resource('db/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def clean_db() -> None:
    """
    Clean the database by deleting all chat history.
    Use for testing only
    """
    db = get_db()
    db.execute('DELETE FROM chat_history')
    db.commit()

@click.command('init-db')
def init_db_command()->None:
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app: Flask)->None:
    """
    Register database functions with the Flask app.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)