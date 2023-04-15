"""# 1. Start by importing the necessary libraries and setting up the API clients """
import os
import threading
import json
import requests

# OpenAI secret Key
API_KEY = os.getenv("OPENAI_API_KEY")
# Models: text-davinci-003,text-curie-001,text-babbage-001,text-ada-001
MODEL = "text-davinci-003"
# Telegram secret access bot token
BOT_TOKEN = os.getenv("TELEGRAM_MUSIQUEVOYAGEBOT")
# Defining the bot's personality using adjectives
BOT_PERSONALITY = """
Answer in a friendly tone, you are the agent for the aweome Musique Voyage. 
Musique Voyage is a duo of music producer, travelling the South of France in their super sonic music truck. 
They are availble for booking. 
If someone wants to book Musique Voyage ask for the venue, dates and style of music you want.
"""
REQUEST_TIMEOUT = 60


def open_ai_chat(prompt):
    """Function that gets the response from OpenAI's chatbot"""
    # Make the request to the OpenAI API
    response = requests.post(
        "https://api.openai.com/v1/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": MODEL, "prompt": prompt, "temperature": 0.4, "max_tokens": 300},
        timeout=REQUEST_TIMEOUT,
    )

    result = response.json()
    final_result = "".join(choice["text"] for choice in result["choices"])
    return final_result


def open_ai_image(prompt):
    """Function that gets an Image from OpenAI"""
    # Make the request to the OpenAI API
    resp = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"prompt": prompt, "n": 1, "size": "1024x1024"},
        timeout=REQUEST_TIMEOUT,
    )
    response_text = json.loads(resp.text)

    return response_text["data"][0]["url"]


def telegram_bot_sendtext(bot_message, chat_id, msg_id):
    """Function that sends a message to a specific telegram group"""
    data = {"chat_id": chat_id, "text": bot_message, "reply_to_message_id": msg_id}
    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json=data,
        timeout=REQUEST_TIMEOUT,
    )
    return response.json()


def telegram_bot_sendimage(image_url, group_id, msg_id):
    """Function that sends an image to a specific telegram group"""
    data = {"chat_id": group_id, "photo": image_url, "reply_to_message_id": msg_id}
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    response = requests.post(url, data=data, timeout=REQUEST_TIMEOUT)
    return response.json()


def process_chat():
    """
    # Function that retrieves the latest requests from users in a Telegram group,
    # generates a response using OpenAI, and sends the response back to the group.
    """
    # Retrieve last ID message from text file for ChatGPT update
    cwd = os.getcwd()
    filename = cwd + "/chatgpt.txt"
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as file:
            file.write("1")
    # else:
    #    print("File Exists")

    with open(filename, encoding="utf-8") as file:
        last_update = file.read()

    # Check for new messages in Telegram group
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={last_update}"
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    data = json.loads(response.content)

    for result in data["result"]:
        try:
            # Ignore messages old than the last updated time
            if float(result["update_id"]) <= float(last_update):
                continue

            # It is a vlaid message
            last_update = str(int(result["update_id"]))

            # What type of message?
            message_type = "tbd"
            try:
                message = result["message"]
                message_type = "message"
            except KeyError:
                message = result["channel_post"]
                message_type = "channel_post"
            print(message_type)

            # ignore messages from bots
            try:
                if message["from"]["is_bot"]:
                    continue
            except KeyError:
                pass  # not from a bot

            # Retrieving message ID of the sender of the request
            msg_id = str(int(message["message_id"]))

            # Retrieving the chat ID
            chat_id = str(message["chat"]["id"])

            print(message["text"])

            # Checking if user wants an image
            if "/img" in message["text"]:
                prompt = message["text"].replace("/img", "")
                bot_response = open_ai_image(prompt)
                print(telegram_bot_sendimage(bot_response, chat_id, msg_id))
            # Checking that user mentionned chatbot's username in message
            if "@Clementine" in message["text"]:
                prompt = message["text"].replace("@Clementine", "")
                # Calling OpenAI API using the bot's personality
                bot_response = open_ai_chat(f"{BOT_PERSONALITY}{prompt}")
                # Sending back response to telegram group
                print(telegram_bot_sendtext(bot_response, chat_id, msg_id))
            # Verifying that the user is responding to the ChatGPT bot
            if "reply_to_message" in message:
                if message["reply_to_message"]["from"]["is_bot"]:
                    prompt = message["text"]
                    bot_response = open_ai_chat(f"{BOT_PERSONALITY}{prompt}")
                    print(telegram_bot_sendtext(bot_response, chat_id, msg_id))
        except Exception as err:  # pylint: disable=W0703
            print(f"Unexpected {err=}, {type(err)=}")

    # Updating file with last update ID
    with open(filename, "w", encoding="utf-8") as file:
        file.write(last_update)

    return "done"


def main():
    """Running a check every 5 seconds to check for new messages"""
    timertime = 5
    process_chat()
    # 5 sec timer
    threading.Timer(timertime, main).start()


# Run the main function
if __name__ == "__main__":
    main()
