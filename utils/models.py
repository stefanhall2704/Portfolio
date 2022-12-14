import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()


class Projects(Base):
    __tablename__ = "Projects"
    id = sa.Column(sa.Integer, primary_key=True, index=True, nullable=False, name="ID")
    title = sa.Column(sa.String(100), nullable=False, name="Title")
    link = sa.Column(sa.String(500), nullable=False, name="URL")
    picture = sa.Column(sa.String(5000), name="Image")
    user_id = sa.Column(sa.Integer, sa.ForeignKey("ApplicationUser.ID"), name="UserID")
    user = relationship("ApplicationUser", back_populates="projects")


class ApplicationUser(Base):
    __tablename__ = "ApplicationUser"
    id = sa.Column(sa.Integer, primary_key=True, index=True, nullable=False, name="ID")
    first_name = sa.Column(sa.String(50), nullable=False, name="First")
    last_name = sa.Column(sa.String(50), nullable=False, name="Last")
    email = sa.Column(sa.String(100), nullable=False, name="Email")
    phone_number = sa.Column(sa.String(50), name="PrimaryPhone")
    projects = relationship("Projects", back_populates="user")
