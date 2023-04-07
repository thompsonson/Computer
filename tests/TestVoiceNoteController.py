"tests, 75% done by ChatGPT (felt like a lot less!!!)"

import pytest
from unittest.mock import Mock, patch
from controllers.controller_notes import VoiceNoteController
from controllers.controller_openai import transcribe_speech
from exceptions import CommandException


class TestVoiceNoteController:
    def test_transcribe_with_force(self):
        mock_model = Mock()
        mock_model.transcribed = True
        mock_model.file_encoding = "ogg"
        mock_model.file_location = "/path/to/voice/file"
        mock_model.content = "some other text"
        mock_controller = Mock()
        mock_controller._ogg2mp3.return_value = "/path/to/mp3/file"
        with patch(
            "controllers.controller_openai.transcribe_speech"
        ) as mock_transcribe:
            mock_transcribe.return_value = "transcripted_text"
            voice_note_controller = VoiceNoteController(mock_model)
            # mock the _ogg2mp3() method
            voice_note_controller._ogg2mp3 = mock_controller._ogg2mp3
            voice_note_controller.transcribe(force=True)
            assert voice_note_controller.model.content == "transcripted_text"
            assert mock_model.content == "transcripted_text"
            assert mock_model.transcribed == True

    def test_transcribe_without_force(self):
        mock_model = Mock()
        mock_model.transcribed = False
        with patch(
            "controllers.controller_openai.transcribe_speech"
        ) as mock_transcribe:
            mock_transcribe.return_value = "transcripted_text"
            voice_note_controller = VoiceNoteController(mock_model)
            voice_note_controller.transcribe()
            assert mock_model.transcribed

    def test_ogg2mp3(self, tmp_path):
        voice_file_path = "tests/41.ogg_test"
        mock_controller = Mock()
        mock_controller._run_command.return_value = 0
        mock_controller._run_command.side_effect = None
        voice_note_controller = VoiceNoteController(Mock())
        mp3_file = voice_note_controller._ogg2mp3(str(voice_file_path))
        assert mp3_file.endswith(".mp3")

    def test_run_command(self):
        voice_note_controller = VoiceNoteController(Mock())
        with pytest.raises(CommandException):
            voice_note_controller._run_command(["false"])
