"""Module which defines the link-stacklog command line interface"""
import click
from .database import init_db
from .stack import (
    peak_links,
    pop_link,
    push_link,
)
from .links import fetch_metadata

DEFAULT_LOG_NAME="default"


@click.group()
@click.version_option()
def cli():
    "Link backlog management utility using a stack style interface"


# @cli.command(name="command")
# @click.argument(
#     "example"
# )
# @click.option(
#     "-o",
#     "--option",
#     help="An example option",
# )
# def first_command(example, option):
#     "Command description goes here"
#     click.echo("Here is some output")


@cli.command(name="init")
def init_database_command():
    "Initialize the stacklog database"
    filename = init_db()
    click.echo(f"Initilized database at {filename}")


@cli.command(name="push")
@click.argument(
    "url"
)
def push_link_command(url):
    "Push a link to the stack"
    title, description = fetch_metadata(url)
    if title is None or description is None:
        click.echo(f"Could not fetch metadata for {url}")
        return
    push_link(DEFAULT_LOG_NAME, url, title, description)
    click.echo(f"Pushed {url}: {title}")


@cli.command(name="peak")
@click.option(
    "-n",
    "--number",
    default=1,
    help="Number of links to peak",
)
def peak_links_command(number):
    "Peak at the top of the stack"
    links = peak_links(DEFAULT_LOG_NAME, number)
    for link in links:
        click.echo(f"{link['url']}: {link['title']}")


@cli.command(name="pop")
def pop_link_command():
    "Pop at the top of the stack"
    link = pop_link(DEFAULT_LOG_NAME)
    click.echo(f"{link['url']}: {link['title']}")

