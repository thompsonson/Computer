"Controllers for the note service."
import tempfile
import os
import subprocess
import logging
from typing import Optional, Tuple, Union

import settings

from models.model_notes import NoteModel, VoiceNoteModel
import controllers.controller_openai as controller_openai
from exceptions import CommandException

from DBAdapter import DBAdapter

logger = logging.getLogger(__name__)


class NoteController:
    """This class handles manipulation of a note."""

    def __init__(self):
        self._model = None

    def __str__(self) -> str:
        return f"Note ID: {self._model.id!r} Content:\n{self._model.content!r}"

    def save(self):
        """Saves the note to the database"""
        with DBAdapter().managed_session() as session:  # type: ignore
            session.add(self._model)  # type: ignore

    async def generate_additonal_info(self, note_id: int):
        "Calls GPT to generate topics, summary and sentiment"
        with DBAdapter().managed_session() as session:  # type: ignore
            self._model = session.query(NoteModel).filter_by(id=note_id).first()  # type: ignore
            if not self._model:
                raise ValueError("No note with that id")
        await controller_openai.generate_additonal_info(self._model)
        logger.info(self._model)
        logger.info(f"content: {self._model.content}")
        logger.info(f"source: {self._model.source}")
        logger.info(f"type: {self._model.type}")

    def add_to_index(self):
        "adds the note to the index for searching"
        # add_to_index
        self._model.dirty = False
        self._model.indexed = True
        self._model.index_reference = "index reference"

    def update_index(self):
        "updates the note in the index"
        # update_index
        self._model.dirty = False


class VoiceNoteController:
    """class for handling voice notes"""

    # def __init__(self):
    #    self._voice_note_model: VoiceNoteModel
    #    self._note_model: NoteModel

    def __str__(self) -> str:
        return f"Voice Note ID: {self._voice_note_model.id!r} Note:\n{self._voice_note_model.note!r}"

    def __init__(self, source: str, file_location: str, file_encoding: str):
        """sets the model for the controller"""
        self.session = DBAdapter().unmanaged_session()
        self._note_model = NoteModel(source=source)
        self._voice_note_model = VoiceNoteModel(
            file_location=file_location,
            file_encoding=file_encoding,
            transcribed=False,
            note=self._note_model,
        )
        self._transcribe()
        self.session.begin()
        self.session.add_all([self._note_model, self._voice_note_model])
        self.session.commit()
        logger.info(
            "new added the voice note (id: %s) to the database",
            self._voice_note_model.id,
        )
        self.voice_note_id = self._voice_note_model.id
        self._note_id = self._note_model.id

    def fully_load_voicenote(self) -> Optional[int]:
        """gets the id for the controller's voice note model"""
        if self._voice_note_model.id is None:
            raise ValueError("No voice note model loaded within the class")
        if self.session is None:
            self.session = DBAdapter().unmanaged_session()
        self.session.begin()
        self._voice_note_model = (
            self.session.query(VoiceNoteModel)
            .filter_by(id=self._voice_note_model.id)
            .first()
        )
        return self._voice_note_model.id

    def get_voice_note_info(self) -> Optional[Tuple[int, str, int]]:
        """Returns the voice_note_id, note_content, and note_id for the given voice_note_id"""
        if self.session is None:
            self.session = DBAdapter().unmanaged_session()
        # Query for the VoiceNoteModel instance with the given id
        logger.info("voice_note_id: %s", self.voice_note_id)
        voice_note_model = (
            self.session.query(VoiceNoteModel).filter_by(id=self.voice_note_id).first()
        )
        logger.info("voice_note_model: %s", voice_note_model)
        if voice_note_model is None:
            raise ValueError("No voice note model loaded within the class")
        voice_note_id = voice_note_model.id

        # Extract the required values from the VoiceNoteModel and its associated NoteModel
        note_content = (
            voice_note_model.note.content if voice_note_model.note is not None else None
        )
        note_id = (
            voice_note_model.note.id if voice_note_model.note is not None else None
        )
        return voice_note_id, note_content, note_id  # type: ignore

    def save(self):
        """Saves the note to the database"""
        if self.session is None:
            self.session = DBAdapter().unmanaged_session()
        self.session.begin()
        self.session.add_all([self._note_model, self._voice_note_model])
        self.session.commit()
        logger.info("saved the voice note to the database")

    def _transcribe(self, force: bool = False):
        """function to transcibe the audio from a voice message"""
        if force or not self._voice_note_model.transcribed:
            # transcibe
            if self._voice_note_model.file_encoding == "ogg":
                voice_file = self._ogg2mp3(self._voice_note_model.file_location)  # type: ignore
            else:
                voice_file = self._voice_note_model.file_location
            # call openai to transcibe the file
            transcript = controller_openai.transcribe_speech(voice_file)
            self._note_model.content = transcript  # type: ignore
            self._voice_note_model.service_used = f"openai/{settings.T2S_MODEL}"
            self._voice_note_model.transcribed = True  # type: ignore

    def _run_command(self, command: list) -> int:
        """Run a command, given an array of the command and arguments"""
        proc = subprocess.Popen(command)
        ret = proc.wait()
        if ret != 0:
            raise CommandException(" ".join(command))
        return ret

    def _ogg2mp3(self, ogg_file: str) -> str:
        """Convert ogg files to mp3"""
        input_file_dir, input_file_name = os.path.split(ogg_file)
        # Convert to mp3
        mp3_file = os.path.join(tempfile.mkdtemp(), input_file_name + ".mp3")
        commands = [
            "ffmpeg",
            "-i",
            ogg_file,
            "-vn",
            "-ar",
            "44100",
            "-ac",
            "2",
            "-b:a",
            "192k",
            mp3_file,
        ]
        self._run_command(commands)  # type: ignore
        return mp3_file
