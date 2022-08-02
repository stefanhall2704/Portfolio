"""add image column

Revision ID: a2c0111f6c5b
Revises: bb3fd19ac45a
Create Date: 2022-08-01 21:53:36.542048

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a2c0111f6c5b"
down_revision = "bb3fd19ac45a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("Projects", sa.Column("Image", sa.String(length=5000), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("Projects", "Image")
    # ### end Alembic commands ###
