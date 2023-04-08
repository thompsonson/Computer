"Controllers for the note service."
import tempfile
import os
import subprocess
import logging

import settings

from models.model_notes import NoteModel, VoiceNoteModel
import controllers.controller_openai as controller_openai
from exceptions import CommandException

from DBAdapter import DBAdapter

logger = logging.getLogger(__name__)


class NoteController:
    """This class handles manipulation of a note."""

    def __init__(self):
        self.model = None

    def save(self):
        """Saves the note to the database"""
        with DBAdapter().managed_session() as session:  # type: ignore
            session.add(self.model)  # type: ignore

    async def generate_additonal_info(self, note_id: int):
        "Calls GPT to generate topics, summary and sentiment"
        with DBAdapter().managed_session() as session:  # type: ignore
            self.model = session.query(NoteModel).filter_by(id=note_id).first()  # type: ignore
            if not self.model:
                raise ValueError("No note with that id")
        await controller_openai.generate_additonal_info(self.model)
        logger.info(self.model)
        logger.info(f"content: {self.model.content}")
        logger.info(f"source: {self.model.source}")
        logger.info(f"type: {self.model.type}")

    def add_to_index(self):
        "adds the note to the index for searching"
        # add_to_index
        self.model.dirty = False
        self.model.indexed = True
        self.model.index_reference = "index reference"

    def update_index(self):
        "updates the note in the index"
        # update_index
        self.model.dirty = False


class VoiceNoteController(NoteController):
    """class for handling voice notes"""

    def __init__(self, model: VoiceNoteModel):
        super().__init__()
        self.model = model

    def transcribe(self, force: bool = False):
        """function to transcibe the audio from a voice message"""
        if force or not self.model.transcribed:
            # transcibe
            if self.model.file_encoding == "ogg":
                voice_file = self._ogg2mp3(self.model.file_location)  # type: ignore
            else:
                voice_file = self.model.file_location
            # call openai to transcibe the file
            transcript = controller_openai.transcribe_speech(voice_file)
            self.model.content = transcript  # type: ignore
            self.model.service_used = f"openai/{settings.T2S_MODEL}"
            self.model.transcribed = True  # type: ignore
            with DBAdapter().managed_session() as session:  # type: ignore
                session.add(self.model)  # type: ignore

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
