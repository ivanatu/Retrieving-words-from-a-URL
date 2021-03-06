"""empty message

Revision ID: 9428482bfcf8
Revises: ccbba61570b6
Create Date: 2019-03-04 16:57:26.086010

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9428482bfcf8'
down_revision = 'ccbba61570b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('url',
    sa.Column('id', sa.String(length=128), nullable=False),
    sa.Column('username', sa.String(length=1200), nullable=True),
    sa.Column('word_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('url')
    # ### end Alembic commands ###
