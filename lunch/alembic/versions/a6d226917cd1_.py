"""empty message

Revision ID: a6d226917cd1
Revises: bf0960b4f7fb
Create Date: 2022-07-01 11:35:48.482277

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6d226917cd1'
down_revision = 'bf0960b4f7fb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('topic',
    sa.Column('title', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('title')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('topic')
    # ### end Alembic commands ###
