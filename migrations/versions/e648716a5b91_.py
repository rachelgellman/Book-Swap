"""empty message

Revision ID: e648716a5b91
Revises: 
Create Date: 2021-12-02 16:36:10.406906

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e648716a5b91'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('isbn', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('author', sa.String(length=500), nullable=True),
    sa.Column('description', sa.String(length=5000), nullable=True),
    sa.Column('cover_url', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_books_isbn'), 'books', ['isbn'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('history',
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.Column('bid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bid'], ['books.id'], ),
    sa.ForeignKeyConstraint(['uid'], ['user.id'], )
    )
    op.create_table('listings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.Column('bid', sa.Integer(), nullable=True),
    sa.Column('state', sa.String(length=16), nullable=True),
    sa.ForeignKeyConstraint(['bid'], ['books.id'], ),
    sa.ForeignKeyConstraint(['uid'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('listings')
    op.drop_table('history')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_books_isbn'), table_name='books')
    op.drop_table('books')
    # ### end Alembic commands ###
