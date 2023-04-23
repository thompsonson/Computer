from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Website(Base):
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True)
    html_content = Column(String, nullable=False)

    images = relationship("Image", back_populates="website")
    files = relationship("File", back_populates="website")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    identifier = Column(String, nullable=False)
    url = Column(String, nullable=False)
    description = Column(String, nullable=True)

    website_id = Column(Integer, ForeignKey("websites.id"), nullable=False)
    website = relationship("Website", back_populates="images")


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    identifier = Column(String, nullable=False)
    url = Column(String, nullable=False)
    description = Column(String, nullable=True)

    website_id = Column(Integer, ForeignKey("websites.id"), nullable=False)
    website = relationship("Website", back_populates="files")
