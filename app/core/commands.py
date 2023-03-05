import click

from app.auth.crud import (
    get_scope, create_scope, get_user_by_email, create_user,
    list_scopes, add_scope_to_user
)
from app.auth.schemas import UserCreate
from app.auth.scopes import LIST_USERS, EDIT_USERS
from app.core.config import settings
from app.db.session import SessionLocal


@click.group()
def cli():
    pass


@cli.command()
def create_superuser():
    click.echo("\nINIT create superuser")
    db = SessionLocal()

    user_db = get_user_by_email(db, settings.SUPER_USER_EMAIL)
    if user_db is not None:
        click.echo("superuser already exist")
    else:
        user_in = UserCreate(
            full_name="root user",
            email=settings.SUPER_USER_EMAIL,
            password=settings.SUPER_USER_PASSWORD,
        )
        user = create_user(db, user_in)

        # add scopes
        scopes = list_scopes(db)
        for scope in scopes:
            add_scope_to_user(db, user.id, scope.name)

    db.close()
    click.echo("FINISH create superuser")


@cli.command()
def create_default_scopes():
    db = SessionLocal()

    default_scopes = [
        LIST_USERS,
        EDIT_USERS,
    ]

    for scope in default_scopes:
        if not get_scope(db, scope):
            create_scope(db, scope)

    db.close()
