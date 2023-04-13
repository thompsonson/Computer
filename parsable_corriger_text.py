""" script to test the parsable_corriger_text function """

import asyncio
from controllers.controller_openai import parsable_corriger_message
from controllers.controller_notes import FrenchNoteController


async def main():
    """main to test parsable_corriger_text"""

    text = """
Je viens de regarder une vidéo sur YouTube qui m'intéresse. 
C'était très intéressant. Ça parle de l'IA qui s'appelle GPT-4. 
C'est n'importe quoi l'advance OpenAI a fait avec GPT-4. 
    """

    response = await parsable_corriger_message(text)

    print(f"Original text: {text}")
    print("----------------------------------------")
    print(f"corriger: {response['corriger']}")
    print("----------------------------------------")
    print(f"conseils: {response['conseils']}")
    print("----------------------------------------")
    print(f"vocabulaire: {response['vocabulaire']}")
    print("----------------------------------------")


def test_french_note_controller():
    """test french note controller"""
    sample_message = {
        "note_id": 1,
        "voice_note_id": 2,
        "message": """
Je viens de regarder une vidéo sur YouTube qui m'intéresse. 
C'était très intéressant. Ça parle de l'IA qui s'appelle GPT-4. 
C'est n'importe quoi l'advance OpenAI a fait avec GPT-4. 
    """,
    }

    test_fnc = FrenchNoteController(sample_message)
    assert test_fnc._note_id == sample_message["note_id"]  # type: ignore
    assert test_fnc._voice_note_id == sample_message["voice_note_id"]  # type: ignore
    assert test_fnc._message_text == sample_message["message"]  # type: ignore

    test_response = test_fnc.corriger_message()
    print(f"test_response: {test_response}")


if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(test_french_note_controller())
    test_french_note_controller()
