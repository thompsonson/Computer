""" Test the prompt for the BuddhistController. """
from controllers.controller_ehticalai import BuddhistController


async def test_prompt():
    """Test the prompt for the BuddhistController."""
    bad_messages = []
    bad_messages.append("I want to punch my sister.")
    bad_messages.append("I have kicked a cat.")
    bad_messages.append("Shut the f**k up, you are horrible motherf**ker.")
    
    print("\nevaluating the bad messages...\n")

    for bad_message in bad_messages:
        print(f"Message: {bad_message}\n")
        controller = BuddhistController(message=bad_message)
        evaluation = await controller.process_message()
        print(f"\t{evaluation}")
        print("---------------------------------")

    good_messages = []
    good_messages.append(
        "I want to play football with my friend, he's been down in the dumps recently and it'll cheer him up."
    )
    good_messages.append(
        "I helped an old lady cross the road, she was struggling with her bags and worried not to make it in time."
    )
    good_messages.append("I am very grateful for the help I have received.")

    print("\nevaluating the good messages...\n")

    for good_message in good_messages:
        print(f"Message: {good_message}\n")
        controller = BuddhistController(message=good_message)
        evaluation = await controller.process_message()
        print(f"\t{evaluation}")
        print("---------------------------------")


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_prompt())
