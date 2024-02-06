import os
import discord
from discord.channel import TextChannel
import openai
from discord import app_commands
from typing import Optional

with open('chat.txt', 'r') as f:
  chat = f.read() 

openai.api_key = os.getenv("OPENAI_API_KEY")
token = os.getenv("dc")

class MyClient(discord.Client):
    async def on_ready(self):
        await tree.sync()
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        global chat
        try:
          if message.content.startswith('$ping'):
            start_time = discord.utils.utcnow()
            message = await message.channel.send('Pong!')
            end_time = discord.utils.utcnow()
            latency = (end_time - start_time).total_seconds() *1000
            await message.edit(content=f"Pong! Latency: {round(latency)} ms")
            return
          if message.content.startswith('$nuke'): #nuke command.
            embed = discord.Embed(title='$Nuke', description='This command is Slash only.', color=0x000100)
            await message.reply(embed=embed)
            return
            
          if message.content.startswith('$help'):
            embed = discord.Embed(title='Help', description='List of available commands:', color=0x00ff00)
            embed.add_field(name='$ping', value='Replies Pong.', inline=False)
            embed.add_field(name='$help', value='Show this help message.', inline=False)
            embed.add_field(name='$purge', value='Delete a specified number of messages.', inline=False)
            await message.channel.send(embed=embed)
            return
          if message.content.startswith('$purge'):
            if message.author.guild_permissions.manage_messages:
                try:
                    num_messages = int(message.content.split(' ')[1])
                    await message.channel.purge(limit=num_messages + 1)
                    await message.channel.send(f'Deleted {num_messages} messages.')
                except Exception as e:
                    await message.channel.send('Please provide a valid number of messages to delete.')
            else:
                await message.channel.send('You do not have permission to use this command.')
            return

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
                  presence_penalty=0,
                  stop=["\n"]
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
client = MyClient(command_prefix='$', intents=intents)
tree = app_commands.CommandTree(client)
#purge command /-based.
@tree.command(
  name="purge",
  description="Delete a specified number of messages.",
)
async def purge(interaction: discord.Interaction, amount: int):
  await interaction.response.defer(ephemeral=True)
  await interaction.channel.purge(limit=amount)
  await interaction.followup.send(f"Deleted {amount} messages.")

@tree.command(
  name="ping",
  description="Check if the bot is online.",
)
async def ping(interaction: discord.Interaction):
  start_time = discord.utils.utcnow()
  message = await interaction.response.send_message("Pong!")
  end_time = discord.utils.utcnow()
  latency = (end_time - start_time).total_seconds() *1000
  await interaction.edit_original_response(content=f"Pong! Latency: {round(latency)} ms")

#nuke command.
@tree.command(
  name="nuke",
  description="Clone and Deletes the channel.",
)
async def nuke(interaction: discord.Interaction, channel: Optional[TextChannel] = None):
  if channel is None:
    channel = interaction.channel
  new_channel = await channel.clone()
  await interaction.response.defer(ephemeral=True)
  await interaction.followup.send(f"Nuke started succesfully")
  await channel.delete()
  await new_channel.send ("Command performed succesfully")

#Roleadd all

client.run(token)
