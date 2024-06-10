"""Module for stack operations"""
import random
from typing import Optional, List

from .database import get_database

def push_link(log_name, url, title, description) -> None:
    """
    Add a new link to the database.

    Parameters:
    log_name (str): The name of the log.
    url (str): The URL of the link.
    title (str): The title of the link.
    description (str): The description of the link.
    """
    db = get_database()
    db["links"].insert({"log_name": log_name, "url": url, "title": title, "description": description})


def pop_link(log_name) -> Optional[dict]:
    """
    Remove and return the most recently added link from the database.

    Parameters:
    log_name (str): The name of the log.

    Returns:
    dict or None: A dictionary containing the id, url, title, description, and timestamp of the link,
                   or None if the log is empty.
    """
    db = get_database()
    links = db["links"].rows_where("log_name = ?", [log_name], order_by="id DESC", limit=1)
    link = next(links, None)
    if link:
        db["links"].delete(link["id"])
        db.conn.commit()
        return {
            "id": link["id"],
            "url": link["url"],
            "title": link["title"],
            "description": link["description"],
            "timestamp": link["timestamp"]
        }
    else:
        return None


def view_links(log_name, num_elements) -> List[dict]:
    """
    Retrieve a specified number of links from the database for a specific log.

    Parameters:
    log_name (str): The name of the log.
    num_elements (int): The number of links to retrieve. Default is 5.

    Returns:
    list: A list of tuples containing the url, title, description, and timestamp of each link.
    list: A list of dictionaries containing the url, title, description, and timestamp of each link.
    """
    db = get_database()
    links = db["links"].rows_where("log_name = ?", [log_name], order_by="id DESC", limit=num_elements)
    return [{"url": link["url"], "title": link["title"], "description": link["description"], "timestamp": link["timestamp"]} for link in links]


def peak_links(log_name, num_elements=1):
    """
    Retrieve the most recent links from the database for a specific log.

    Parameters:
    log_name (str): The name of the log.
    num_elements (int): The number of links to retrieve.

    Returns:
    list: A list of tuples containing the url, title, description, and timestamp of each link.
    """
    return view_links(log_name, num_elements)


def head_links(log_name, num_elements=5):
    """
    Retrieve the most recent links from the database for a specific log.

    Parameters:
    log_name (str): The name of the log.
    num_elements (int): The number of links to retrieve.

    Returns:
    list: A list of tuples containing the url, title, description, and timestamp of each link.
    """
    return view_links(log_name, num_elements)


def tail_links(log_name, num_elements=5):
    """
    Retrieve the least recent links from the database for a specific log.

    Parameters:
    log_name (str): The name of the log.
    num_elements (int): The number of links to retrieve.

    Returns:
    list: A list of dictionaries containing the url, title, description, and timestamp of each link.
    """
    db = get_database()
    links = db["links"].rows_where("log_name = ?", [log_name], order_by="id ASC", limit=num_elements)
    return [{"url": link["url"], "title": link["title"], "description": link["description"], "timestamp": link["timestamp"]} for link in links]


def clear_links(log_name):
    """
    Remove all links from the database for a specific log.

    Parameters:
    log_name (str): The name of the log.
    """
    db = get_database()
    db["links"].delete_where("log_name = ?", [log_name])
    db.conn.commit()


def search_links(log_name, query):
    """
    Search for links in the database for a specific log that match a query in the title or description.

    Parameters:
    log_name (str): The name of the log.
    query (str): The search query.

    Returns:
    list: A list of dictionaries containing the url, title, description, and timestamp of each matching link.
    """
    db = get_database()
    links = db["links"].rows_where(
        "log_name = ? AND (title LIKE ? OR description LIKE ?)",
        [log_name, f'%{query}%', f'%{query}%'],
        order_by="id DESC"
    )
    return [{"url": link["url"], "title": link["title"], "description": link["description"], "timestamp": link["timestamp"]} for link in links]


def get_link_count(log_name) -> int:
    """
    Retrieve the number of links in the database for a specific log.

    Parameters:
    log_name (str): The name of the log.

    Returns:
    int: The number of links in the database for the specified log.
    """
    db = get_database()
    return db["links"].count_where("log_name = ?", [log_name])


def get_link_by_id(log_name, link_id):
    """
    Retrieve a link from the database for a specific log by its id.

    Parameters:
    log_name (str): The name of the log.
    link_id (int): The id of the link.

    Returns:
    dict or None: A dictionary containing the url, title, description, and timestamp of the link,
                   or None if the link is not found.
    """
    db = get_database()
    link = db["links"].get(link_id)
    if link and link["log_name"] == log_name:
        return {
            "url": link["url"],
            "title": link["title"],
            "description": link["description"],
            "timestamp": link["timestamp"]
        }
    else:
        return None


def get_random_link(log_name):
    """
    Retrieve a random link from the database for a specific log.

    Parameters:
    log_name (str): The name of the log.

    Returns:
    dict or None: A dictionary containing the url, title, description, and timestamp of a random link,
                   or None if the log is empty.
    """
    db = get_database()
    count = db["links"].count_where("log_name = ?", [log_name])
    if count > 0:
        random_id = random.randint(1, count)
        link = db["links"].rows_where("log_name = ?", [log_name], order_by="id", limit=1, offset=random_id - 1)
        link = next(link, None)
        if link:
            return {
                "url": link["url"],
                "title": link["title"],
                "description": link["description"],
                "timestamp": link["timestamp"]
            }
    return None
