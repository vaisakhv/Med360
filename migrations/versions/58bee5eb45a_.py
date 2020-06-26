"""empty message

Revision ID: 58bee5eb45a
Revises: a1edd8ffc7
Create Date: 2020-06-26 15:09:52.261220

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '58bee5eb45a'
down_revision = 'a1edd8ffc7'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_roles')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_roles',
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.Column('user_id', sa.INTEGER(), nullable=True),
                    sa.Column('role_id', sa.INTEGER(), nullable=True),
                    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    ### end Alembic commands ###
