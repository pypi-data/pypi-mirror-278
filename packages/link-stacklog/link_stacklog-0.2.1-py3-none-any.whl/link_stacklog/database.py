"""Module for initializing and connecting to the SQLite database"""
import datetime
import sqlite_utils
import pathlib
import os

import click

DATABASE_FILE = "linkstacklog.db"

def user_dir():
    link_stacklog_user_path = os.environ.get("LINK_STACKLOG_USER_PATH")
    if link_stacklog_user_path:
        path = pathlib.Path(link_stacklog_user_path)
    else:
        path = pathlib.Path(click.get_app_dir("link_stacklog"))
    path.mkdir(exist_ok=True, parents=True)
    return path

def get_database(init=False) -> sqlite_utils.Database:
    if not init and not (user_dir() / DATABASE_FILE).exists():
        click.echo("Database not found. Run 'link-stacklog init' first.")
        raise click.Abort()
    return sqlite_utils.Database(user_dir() / DATABASE_FILE)

def init_db():
    db = get_database(init=True)

    db["links"].create({
        "id": int,
        "log_name": str,
        "url": str,
        "title": str,
        "description": str,
        "timestamp": str,
    }, pk="id", defaults={"timestamp": datetime.datetime.now().isoformat()})

    return user_dir() / DATABASE_FILE
