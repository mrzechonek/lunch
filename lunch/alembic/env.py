from alembic import context
from lunch import database
from sqlalchemy import create_engine

engine = create_engine(database.DATABASE)

with engine.connect() as connection:
    context.configure(connection=connection, target_metadata=database.Base.metadata)

    with context.begin_transaction():
        context.run_migrations()
