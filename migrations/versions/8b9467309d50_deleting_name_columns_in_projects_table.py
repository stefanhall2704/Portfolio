"""Deleting name columns in Projects table

Revision ID: 8b9467309d50
Revises: 
Create Date: 2022-08-03 14:34:16.510255

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8b9467309d50"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "ApplicationUser",
        sa.Column("ID", sa.Integer(), nullable=False),
        sa.Column("First", sa.String(length=50), nullable=False),
        sa.Column("Last", sa.String(length=50), nullable=False),
        sa.Column("Email", sa.String(length=100), nullable=False),
        sa.Column("PrimaryPhone", sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint("ID"),
    )
    op.create_index(
        op.f("ix_ApplicationUser_ID"), "ApplicationUser", ["ID"], unique=False
    )
    op.create_table(
        "Projects",
        sa.Column("ID", sa.Integer(), nullable=False),
        sa.Column("Title", sa.String(length=100), nullable=False),
        sa.Column("URL", sa.String(length=500), nullable=False),
        sa.Column("Image", sa.String(length=5000), nullable=True),
        sa.Column("UserID", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["UserID"],
            ["ApplicationUser.ID"],
        ),
        sa.PrimaryKeyConstraint("ID"),
    )
    op.create_index(op.f("ix_Projects_ID"), "Projects", ["ID"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_Projects_ID"), table_name="Projects")
    op.drop_table("Projects")
    op.drop_index(op.f("ix_ApplicationUser_ID"), table_name="ApplicationUser")
    op.drop_table("ApplicationUser")
    # ### end Alembic commands ###
