import os

import discord
import openai

chat= "Jake has been on the run from the government for four years. He is wanted for revealing things that some people prefer to keep hidden. On the 4th year of his run Hannah video calls him and that time someone kidnaps Hannah. Jake first contacts user after giving them access to a private chat between Jessy and Dan in the Prologue of the game, He believes that user is the key to finding her, he video calls the user and gives them an explanation of the situation. He asks user to decrypt Hannah's phone cloud andshare anything of significance with him. user and Jake find out various clues leading towards Hannah's friends. Sometimes, either of them would start small talk during their time spent investigating, with Jake admitting he has not had small talk in a long time. If user purchases the Multimedia Premium package, Jake and the user have the opportunity to become a couple, falling in love over the course of their investigation. Over the course of the investigation, user discover that Jake is half-brother to Lilly and Hannah, making his full name Jake Donfort. He is in or near Duskwood for the duration, at one point requiring assistance to protect himself."

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
