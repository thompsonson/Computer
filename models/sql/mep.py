from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


# Define a many-to-many association table for MEPs and Committees
mep_committees_association = Table(
    "mep_committees",
    Base.metadata,
    Column("mep_id", Integer, ForeignKey("meps.id")),
    Column("committee_id", Integer, ForeignKey("committees.id")),
)

# Define a many-to-many association table for MEPs and Activitis
mep_activities_association = Table(
    "mep_activities",
    Base.metadata,
    Column("mep_id", Integer, ForeignKey("meps.id")),
    Column("committee_id", Integer, ForeignKey("activities.id")),
)


# Committee data class
class Committee(Base):
    __tablename__ = "committees"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    meps = relationship(
        "MEP", secondary=mep_committees_association, back_populates="committees"
    )

    def __repr__(self):
        return f"<Committee(id={self.id}, name={self.name})>"


# Activity data class
class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)

    meps = relationship(
        "MEP", secondary=mep_activities_association, back_populates="activities"
    )

    def __repr__(self):
        return f"<Activity(id={self.id}, description={self.description})>"


# MEP data class
class MEP(Base):
    __tablename__ = "meps"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    affiliation = Column(String, nullable=True)
    source_url = Column(String, nullable=True)

    activities = relationship(
        "Activity", secondary=mep_activities_association, back_populates="meps"
    )
    committees = relationship(
        "Committee", secondary=mep_committees_association, back_populates="meps"
    )

    def __repr__(self):
        return f"<MEP(id={self.id}, name={self.name}, affiliation={self.affiliation}, source_url={self.source_url})>"
