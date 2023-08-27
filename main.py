import chainlit as cl
import openai
import os
import json
import time

os.environ["OPENAI_API_KEY"] = 'YOUR_API_KEY'
openai.api_key = 'YOUR_API_KEY'


def get_character_data(file_path, bot_name):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    # Access and use the data
    for entry in data:
        if entry['Name'] == bot_name:
            name = entry['Name']
            characteristic = entry['Characteristic']
            philosophy = entry['Philosophy']
    return name, characteristic, philosophy


@cl.action_callback("Dharma")
async def on_action(action):
    # run the character
    file_path = './character.json'
    global name, characteristic, philosophy
    name, characteristic, philosophy = get_character_data(
        file_path, action.name)
    time.sleep(3)
    await cl.Message(content=f"Begin your chat with {action.name} Bot!").send()

    # # If want remove the action button
    # await action.remove()


@cl.action_callback("Anime")
async def on_action(action):
    # run the character
    file_path = './character.json'
    global name, characteristic, philosophy
    name, characteristic, philosophy = get_character_data(
        file_path, action.name)
    time.sleep(3)
    await cl.Message(content=f"Begin your chat with {action.name} Bot!").send()

    # # If want remove the action button
    # await action.remove()


@cl.on_chat_start
async def start():
    # Sending an action button
    actions = [
        cl.Action(name="Dharma", value="empty",
                  description="Dharma characteristics bot!"),
        cl.Action(name='Anime', value='empty',
                  description='Anime characteristics bot!')
    ]
    await cl.Message(content="Choose the bot characteristic:", actions=actions).send()


@cl.on_message
async def main(message: str):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "system", "content": f"Your name is {name}, you characteristics are {characteristic} and your philosophy are {philosophy}."
             "You are strongly strict with these philosophy and it affect all your behavior and mindset."
             "For each message from user, answer based on your characteristic but not lengthy. "},
            {"role": "user", "content": message}
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    await cl.Message(content=f"{response['choices'][0]['message']['content']}",).send()
