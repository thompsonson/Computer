from controllers.controller_ehticalai import BuddhistController


async def test_prompt():
    # Mock input message
    bad_messages = []
    bad_messages.append("I want to punch my sister.")
    bad_messages.append("I have kicked a cat.")
    bad_messages.append("Shut the fuck up, you are horrible.")

    for bad_message in bad_messages:
        print(f"Message: {bad_message}")
        controller = BuddhistController(message=bad_message)
        evaluation = await controller.process_message()
        print(evaluation)

    good_messages = []
    good_messages.append("I want to play football with my firend.")
    good_messages.append("I helped an old lady cross the road.")
    good_messages.append("I am very grateful for the help I have received.")

    for good_message in good_messages:
        print(f"Message: {good_message}")
        controller = BuddhistController(message=good_message)
        evaluation = await controller.process_message()
        print(evaluation)


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_prompt())
