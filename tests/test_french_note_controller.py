import pytest
from unittest.mock import MagicMock

from models.model_notes import NoteModel, FrenchNoteModel
from controllers.controller_notes import FrenchNoteController


@pytest.fixture
def mock_message():
    return {
        "note_id": 1,
        "voice_note_id": 1,
        "message": "Bonjour, je suis ravi de vous rencontrer.",
    }


@pytest.fixture
def mock_session():
    session = MagicMock()
    session.query().filter_by().first.return_value = NoteModel(id=1)
    return session


@pytest.fixture
def mock_llm():
    llm = MagicMock()
    llm.return_value = """
    corriger: Bonjour, je suis ravi de vous rencontrer.
    vocabulaire: heureux, content
    conseils: Votre phrase est bien structurée.
    erreurs: 
    idiomes: 
    """
    return llm


def test_french_note_controller(mock_message, mock_session, mock_llm):
    controller = FrenchNoteController(mock_message, session=mock_session)
    controller._llm = mock_llm

    result = controller.corriger_message()

    assert result.corriger == "Bonjour, je suis ravi de vous rencontrer."
    assert result.vocabulaire == "heureux, content"
    assert result.conseils == "Votre phrase est bien structurée."
    assert result.erreurs == ""
    assert result.idiomes == ""

    mock_session.add.assert_called_with(result)
    mock_session.commit.assert_called_once()
