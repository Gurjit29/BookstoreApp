"""new column

Revision ID: 05171818d1e3
Revises: 1e14ae22fd7b
Create Date: 2019-04-05 02:33:38.953690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05171818d1e3'
down_revision = '1e14ae22fd7b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('writer', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('book', 'writer')
    # ### end Alembic commands ###
