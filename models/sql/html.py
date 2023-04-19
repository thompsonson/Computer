""" sqlalchemy classes for the html controller """

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


class Image(Base):
    """Represents an image with its name and associated prompt."""

    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    image_name = Column(String, nullable=False)
    image_prompt = Column(String, nullable=False)
    html_id = Column(Integer, ForeignKey("html_files.id"))

    def __repr__(self):
        return f"<Image(image_name='{self.image_name}', image_prompt='{self.image_prompt}')>"


class HtmlFile(Base):
    """Represents an HTML file with its content, filename, and related images."""

    __tablename__ = "html_files"
    id = Column(Integer, primary_key=True)
    html = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    images = relationship("Image", backref="html_file")

    def __repr__(self):
        return f"<HtmlFile(filename='{self.filename}', html='{self.html[:50]}...')>"  # type: ignore
