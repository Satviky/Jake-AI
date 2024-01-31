import os

import discord
import openai


with open('chat.txt', 'r') as f:
  chat = f.read() 

openai.api_key = os.getenv("OPENAI_API_KEY")
token = os.getenv("dc")

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        # guild_ids = [1162965749061664819] # Put your server ID in this array.

    async def on_message(self, message):
        global chat
        try:
          chat += f"{message.author}: {message.content}\n"
          print(f'Message from {message.author}: {message.content}')
          if self.user!= message.author:
              if self.user in message.mentions:
                response = openai.Completion.create(
                  model="gpt-3.5-turbo-instruct-0914",
                  prompt = f"{chat}\n Jake_duskwood#2263:",
                  temperature=0.2,
                  max_tokens=100,
                  top_p=1,
                  frequency_penalty=0,
                  presence_penalty=0
                )
                channel = message.channel
                messageToSend = response.choices[0].text.strip()
                await channel.send(messageToSend)    
        except Exception as e:
          print(e)
          await message.channel.send("Sorry, I couldn't process your request.")
          chat = ""


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)
