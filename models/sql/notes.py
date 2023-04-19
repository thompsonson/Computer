from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.orm import declarative_base, relationship

notes_base = declarative_base()


class NoteModel(notes_base):
    """Data class for notes"""

    __tablename__ = "note_base"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True)
    content = Column(Text, nullable=True)
    source = Column(String, nullable=True)
    type = Column(String, nullable=True)
    topics = Column(String, nullable=True)
    summary = Column(Text, nullable=True)
    sentiment = Column(String, nullable=True)
    indexed = Column(Boolean, nullable=True)
    dirty = Column(Boolean, nullable=True)
    index_reference = Column(String, nullable=True)

    voice_note = relationship("VoiceNoteModel", uselist=False, back_populates="note")
    french_note = relationship("FrenchNoteModel", uselist=False, back_populates="note")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id!r}) - {self.name!r}"


class VoiceNoteModel(notes_base):
    """class for voice notes"""

    __tablename__ = "note_voicenote"

    id = Column(Integer, primary_key=True)
    file_location = Column(String, nullable=True)
    file_encoding = Column(String, nullable=True)
    transcribed = Column(Boolean, nullable=True)
    transcription_rating = Column(Integer, nullable=True)
    service_used = Column(String, nullable=True)

    note_id = Column(Integer, ForeignKey("note_base.id"))
    note = relationship("NoteModel", back_populates="voice_note")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id!r})"


class FrenchNoteModel(notes_base):
    """class for French notes"""

    __tablename__ = "note_frenchnote"

    id = Column(Integer, primary_key=True)
    corriger = Column(Text, nullable=True)
    erreurs = Column(Text, nullable=True)
    vocabulaire = Column(Text, nullable=True)
    idiomes = Column(Text, nullable=True)
    conseils = Column(Text, nullable=True)

    note_id = Column(Integer, ForeignKey("note_base.id"))
    note = relationship("NoteModel", back_populates="french_note")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id!r})"
