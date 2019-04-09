"""key

Revision ID: f117462e9d10
Revises: 05171818d1e3
Create Date: 2019-04-09 01:36:52.575749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f117462e9d10'
down_revision = '05171818d1e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('key', sa.String(length=130), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'key')
    # ### end Alembic commands ###
