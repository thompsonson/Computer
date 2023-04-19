# GPT4 generated - work in progress!!
from unittest.mock import Mock, patch

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from controllers.controller_notes import FrenchNoteController
from models.sql.notes import FrenchNoteModel, NoteModel, notes_base as Base


# Define some test fixtures


@pytest.fixture(scope="module")
def sample_message():
    return {
        "note_id": 1,
        "voice_note_id": 2,
        "message": "Bonjour, comment vas-tu?",
    }


@pytest.fixture(scope="module")
def sample_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    return Session()


@pytest.fixture(scope="module")
def sample_note_model():
    return NoteModel(1)


@pytest.fixture(scope="module")
def sample_french_note_model():
    return FrenchNoteModel(
        id=1, corriger="", erreurs="", vocabulaire="", idiomes="", conseils=""
    )


# Define a mock OpenAI class


class mock_openai_class(Mock):
    @staticmethod
    def create(**kwargs):
        return mock_openai_class()

    def __call__(self, *args, **kwargs):
        return self

    def __getattr__(self, item):
        return mock_openai_class()

    def __iter__(self):
        return iter([])


# Define some test cases


def test_init(sample_message, sample_session):
    controller = FrenchNoteController(sample_message, sample_session)

    assert controller._message == sample_message
    assert controller._note_id == sample_message["note_id"]
    assert controller._voice_note_id == sample_message["voice_note_id"]
    assert controller._message_text == sample_message["message"]
    assert controller._session == sample_session
    assert controller._note_model is not None


@patch("DBAdapter.DBAdapter")
@patch("langchain.llms.OpenAI", mock_openai_class)
def test_corriger_message(
    mock_db_adapter_class,
    sample_message,
    sample_session,
    sample_note_model,
    sample_french_note_model,
):
    # Create a new mock session and set its query() method to return a mock object
    mock_session = Mock()
    mock_session.query.return_value.filter_by.return_value.first.return_value = (
        sample_note_model
    )

    # Configure the DBAdapter() mock to return the new session
    mock_db_adapter = Mock()
    mock_db_adapter.unmanaged_session.return_value = mock_session
    mock_db_adapter_class.return_value = mock_db_adapter

    controller = FrenchNoteController(sample_message)

    assert controller._note_id == sample_message["note_id"]
    assert controller._voice_note_id == sample_message["voice_note_id"]
    assert controller._message_text == sample_message["message"]
    assert controller._note_model == sample_note_model
    assert controller._session == mock_session
    assert controller._french_note_model == sample_french_note_model

    result = controller.corriger_message()

    assert result == sample_french_note_model
    assert result.corriger == "Bonjour, comment vas-tu?"
    assert result.vocabulaire == "bien, merci"
    assert result.conseils == "Votre grammaire est correcte."
    assert result.erreurs == ""
    assert result.idiomes == ""
    mock_db_adapter_class.assert_called_once()
    mock_db_adapter.unmanaged_session.assert_called_once()
    mock_db_adapter_class.return_value.unmanaged_session.assert_called_once()
    mock_openai_class.assert_called_once_with(
        model_name=settings.GPT_MODEL, openai_api_key=settings.OPENAI_API_KEY
    )
