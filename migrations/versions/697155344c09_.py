"""empty message

Revision ID: 697155344c09
Revises: eb805c2527fd
Create Date: 2019-03-04 16:30:11.391511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '697155344c09'
down_revision = 'eb805c2527fd'
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