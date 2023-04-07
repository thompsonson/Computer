"""data models for notes"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()


class NoteModel(Base):
    """Data class for notes"""

    __tablename__ = "note_base"

    # added from source
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    content: Mapped[str] = mapped_column(nullable=True)
    source: Mapped[str] = mapped_column(nullable=True)
    type: Mapped[str] = mapped_column(nullable=True)
    # generated by AI
    topics: Mapped[str] = mapped_column(nullable=True)  # an array?
    summary: Mapped[str] = mapped_column(nullable=True)
    sentiment: Mapped[str] = mapped_column(nullable=True)
    # index related
    indexed: Mapped[bool] = mapped_column(nullable=True)
    dirty: Mapped[bool] = mapped_column(nullable=True)
    index_reference: Mapped[str] = mapped_column(nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "note",
        "polymorphic_on": "type",
    }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id!r}) - {self.name!r}"


class VoiceNoteModel(NoteModel):
    """class for voice notes"""

    __tablename__ = "note_voicenote"

    id: Mapped[int] = mapped_column(ForeignKey("note_base.id"), primary_key=True)

    # file information
    file_location: Mapped[str] = mapped_column(nullable=True)
    file_encoding: Mapped[str] = mapped_column(nullable=True)
    # processing
    transcribed: Mapped[bool] = mapped_column(nullable=True)
    transcription_rating: Mapped[int] = mapped_column(nullable=True)
    service_used: Mapped[str] = mapped_column(nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "voicenote",
    }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r})"
