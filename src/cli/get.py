import click

from click_default_group import DefaultGroup

from .authenticator import pass_mwdb
from .main import main
from .formatters import pass_formatter
from .types import HashFile


@main.group("get", cls=DefaultGroup, default='details', default_if_no_args=True)
def get_command():
    """
    Get information about object
    """
    pass


@get_command.command("details")
@click.argument("file-or-hash", type=HashFile())
@pass_formatter
@pass_mwdb
@click.pass_context
def get_details(ctx, mwdb, formatter, file_or_hash):
    """
    Get detailed information about object
    """
    from ..file import MWDBFile
    from ..config import MWDBConfig
    from ..blob import MWDBBlob
    obj = mwdb.query(file_or_hash)
    if isinstance(obj, MWDBFile):
        output = formatter.format_file_detailed(obj)
    elif isinstance(obj, MWDBConfig):
        output = formatter.format_config_detailed(obj)
    elif isinstance(obj, MWDBBlob):
        output = formatter.format_blob_detailed(obj)
    else:
        output = None  # just to satisfy linter
        ctx.abort(
            f"TODO: Don't know how to represent this object type ({obj.object_type})"
        )

    click.echo(output)


@get_command.command("parents")
@click.argument("file-or-hash", type=HashFile())
@pass_formatter
@pass_mwdb
def get_parents(mwdb, formatter, file_or_hash):
    """
    Get list of parents
    """
    obj = mwdb.query(file_or_hash)
    formatter.print_lines(formatter.format_object_list(obj.parents))


@get_command.command("children")
@click.argument("file-or-hash", type=HashFile())
@pass_formatter
@pass_mwdb
def get_children(mwdb, formatter, file_or_hash):
    """
    Get list of children
    """
    obj = mwdb.query(file_or_hash)
    formatter.print_lines(formatter.format_object_list(obj.children))


@get_command.command("shares")
@click.argument("file-or-hash", type=HashFile())
@pass_formatter
@pass_mwdb
def get_shares(mwdb, formatter, file_or_hash):
    """
    Get list of shares
    """
    obj = mwdb.query(file_or_hash)
    formatter.print_lines(formatter.format_shares_list(obj.shares))


@get_command.command("comments")
@click.argument("file-or-hash", type=HashFile())
@pass_formatter
@pass_mwdb
def get_comments(mwdb, formatter, file_or_hash):
    """
    Get list of comments
    """
    obj = mwdb.query(file_or_hash)
    formatter.print_lines(formatter.format_comments_list(obj.comments))


@get_command.command("metakeys")
@click.argument("file-or-hash", type=HashFile())
@pass_formatter
@pass_mwdb
def get_metakeys(mwdb, formatter, file_or_hash):
    """
    Get list of metakeys
    """
    obj = mwdb.query(file_or_hash)
    click.echo(formatter.format_metakeys_list(obj.metakeys))
