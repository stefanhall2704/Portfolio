import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()


class Projects(Base):
    __tablename__ = "Projects"
    id = sa.Column(sa.Integer, primary_key=True, index=True, nullable=False, name="ID")
    title = sa.Column(sa.String(100), nullable=False, name="Title")
    link = sa.Column(sa.String(500), nullable=False, name="URL")
    first_name = sa.Column(sa.String(length=50), name="First")
    last_name = sa.Column(sa.String(length=50), name="Last")
    picture = sa.Column(sa.String(5000), name="Image")
